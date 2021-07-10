from colorama import Fore, Back, Style
import time


class Enemy:
    def __init__(self, len_paddle, posX, posY, leftRange, rightRange):
        self.__len = 35
        self.__paddleLen = 9
        self.__posX = posX
        self.__posY = posY-2
        self.__leftRange = leftRange
        self.__rightRange = rightRange
        self.__afterLastThrow = 0
        self.__enemyBody = []
        self.__strength = 100
        file = "ufo.txt"
        with open(file, 'r') as lines:
            for line in lines:
                self.__enemyBody.append(list(line.strip('\n')))

    def get_posX(self):
        return self.__posX

    def get_posY(self):
        return self.__posY

    def set_posX(self, val):
        self.__posX = val

    def set_posY(self, val):
        self.__posY = val

    def get_afterLastThrow(self):
        return self.__afterLastThrow

    def set_afterLastThrow(self, val):
        self.__afterLastThrow += val

    def reset_afterLastThrow(self):
        self.__afterLastThrow = 0
#   x,y is row,col

    def disp_enemy(self, area):
        b = int(self.__posX)
        a = int(self.__posY)
        for i in range(a, a+len(self.__enemyBody)):
            for j in range(b, b+35):
                # if self.__enemyBody[i-a][j-b] != " ":
                area._gameArea[i][j] = Back.LIGHTYELLOW_EX + Fore.BLACK + self.__enemyBody[i-a][j-b]

    def right(self, paddle_posX):
        if self.__posX+self.__len-1 < self.__rightRange-3:
            if self.__posX+self.__len/2 < self.__paddleLen/2+paddle_posX:
                self.__posX = self.__paddleLen/2+paddle_posX-self.__len/2
            return 1
        return 0

    def left(self, paddle_posX):
        if self.__posX > self.__leftRange:
            if self.__posX+self.__len/2 > self.__paddleLen/2+paddle_posX:
                self.__posX = self.__paddleLen/2+paddle_posX-self.__len/2
            return 1
        return 0

    def enemyHitByBall(self):
        self.__strength -= 10

    def get_enemyStrength(self):
        return self.__strength
