from colorama import Fore, Back, Style
import time


class Paddle:
    def __init__(self, len_paddle, posX, posY, leftRange, rightRange):
        self.__len = len_paddle
        self.__posX = posX
        self.__posY = posY
        self.__leftRange = leftRange
        self.__rightRange = rightRange
        self.__grabbed = 0  # paddle can grab
        self.__shoot = 0
        self.__afterLastShoot = 0
        self.__bricksDown = 0

    def set_grabbed(self, val):
        self.__grabbed = val

    def set_bricksDown(self, val):
        self.__bricksDown = val

    def get_bricksDown(self):
        return self.__bricksDown

    def set_shoot(self, val):
        self.__shoot = val

    def set_afterLastShoot(self, val):
        self.__afterLastShoot = val

    def get_afterLastShoot(self):
        return self.__afterLastShoot

    def get_posX(self):
        return self.__posX

    def get_posY(self):
        return self.__posY

    def get_len(self):
        return self.__len

    def get_grabbed(self):
        return self.__grabbed

    def disp_paddle(self, area):
        a = int(self.__posX)
        b = int(self.__posY)
        if self.__shoot == 0:
            for i in range(a, a+self.__len):
                for j in range(b, b+1):
                    area._gameArea[j][i] = Back.MAGENTA + Fore.BLACK + '#'
        else:
            for i in range(a, a+self.__len):
                for j in range(b, b+1):
                    area._gameArea[j][i] = Back.LIGHTYELLOW_EX + Fore.BLACK + '^'
                if i == a or i == a+self.__len-1:
                    area._gameArea[j][i] = Back.LIGHTRED_EX + Fore.BLACK + 'O'

    def right(self):
        if self.__posX+self.__len-1 < self.__rightRange-3:
            self.__posX += 1
            return 1
        return 0

    def left(self):
        if self.__posX > self.__leftRange:
            self.__posX -= 1
            return 1
        return 0

    def release_ball(self):
        self.__grabbed = 0

    def shrinkPaddle(self, BallPosX, Ballgrabbed):  # take care when grabbed
        if Ballgrabbed == 0:
            if self.__len == 9:
                self.__len = 5
                self.__posX += 2
            elif self.__len == 13:
                self.__len = 5
                self.__posX += 4
        else:
            if self.__len == 9:
                if BallPosX < self.__posX+self.__len/2:  # left half
                    self.__len = 5
                else:  # right half
                    self.__len = 5
                    self.__posX += self.__len/2

            elif self.__len == 13:
                if BallPosX < self.__posX+5:  # left
                    self.__len = 5
                elif BallPosX > self.__posX+7:  # right
                    self.__len = 5
                    self.__posX += 7
                else:  # mid
                    self.__len = 5
                    self.__posX += 4

    def expandPaddle(self):
        if self.__len == 9:
            self.__posX -= 2
            self.__len = 13
        elif self.__len == 5:
            self.__posX -= 4
            self.__len = 13

    def unshrinkPaddle(self):
        if self.__posX <= self.__leftRange+1:
            self.__posX = self.__leftRange
            self.__len = 9
        elif self.__posX+self.__len >= self.__rightRange-3:
            self.__len = 9
            self.__posX = self.__rightRange-self.__len-2
        else:
            self.__posX -= 2
            self.__len = 9

    def unexpandPaddle(self, BallPosX, Ballgrabbed):  # take care when grabbed
        if Ballgrabbed == 0:
            self.__posX += 2
            self.__len = 9
        else:
            if BallPosX <= self.__posX+8:
                self.__len = 9
            else:
                self.__posX += 2
                self.__len = 9

    def shootLasers(self):
        self.__shoot = 1
        self.__afterLastShoot = 10
