from colorama import Fore, Back, Style
import time
import random
import math
import os


class Bomb:
    def __init__(self, posX, posY, downRange):
        self.__posX = posX
        self.__posY = posY
        self.__removed = 0
        self.__speedY = int(1)
        self.__hit = 0  # tells ever taken
        self.__downRange = downRange

    def get_hit(self):
        return self.__hit

    def disp_bomb(self, area):
        a = int(self.__posX)
        b = int(self.__posY)
        if self.__hit == 0:
            for i in range(a, a+2):
                for j in range(b, b+1):
                    area._gameArea[j][i] = Back.YELLOW + Fore.BLACK + 'B'

    def moveBomb(self, paddle_posX, paddle_len):
        if self.__hit == 1:
            return 0
        m = self.check_paddle_collision(paddle_posX, paddle_len)
        retv = 0
        if m == 0:
            self.__posY += self.__speedY
        elif m == 1:
            self.bombHitPaddle()
            os.system("aplay sounds/bombHitPaddle.wav -q &")
            retv = 1
        elif m == 2:
            self.__removed = 1
            retv = 10
        return retv  # 0 when already taken before or powerup moving in area

    def check_paddle_collision(self, paddle_posX, paddle_len):
        k = 0
        if self.__posY == self.__downRange:
            k = self.check_paddle_collisionX(paddle_posX, paddle_len)  # 1 for taken 2 for powerup lost
        return k

    def check_paddle_collisionX(self, paddle_posX, paddle_len):
        k = 2
        if self.__posX >= paddle_posX-1 and self.__posX <= (paddle_posX+paddle_len-1):
            k = 1
        return k

    def bombHitPaddle(self):
        self.__hit = 1
