from colorama import Fore, Back, Style
import time
import random
import math


class Brick:
    def __init__(self, posX, posY):
        self._posX = posX
        self._posY = posY
        self._removed = 0
        self._brokenAtLife = 0
        self._brokenAtTime = 0
        self._subtype = 1  # 0 for breakable,1 for unbreakable
        self._rainbow = 0

    def disp_brick(self, area):
        a = int(self._posX)
        b = int(self._posY)
        if self._removed == 1:
            for i in range(a, a+6):
                for j in range(b, b+2):
                    area._gameArea[j][i] = Back.BLACK+' '

    def get_rainbow(self):
        return self._rainbow

    def get_posX(self):
        return self._posX

    def get_posY(self):
        return self._posY

    def get_removed(self):
        return self._removed

    def set_removed(self, val):
        self._removed = val

    def get_brokenAtLife(self):
        return self._brokenAtLife

    def set_brokenAtLife(self, val):
        self._brokenAtLife = val

    def get_brokenAtTime(self):
        return self._brokenAtTime

    def get_subtype(self):
        return self._subtype

    def shiftDown(self, val):
        self._posY = self._posY + 1
        return self._posY


class BreakableBrick(Brick):
    def __init__(self, posX, posY, brickType):
        super().__init__(posX, posY)
        self.__brickType = brickType  # 4,3,2,1 ;  implies trength as well ;  4 means max strength
        self._subtype = 0

    def get_brickType(self):
        return self.__brickType

    def set_brickType(self, val):
        self.__brickType = val

    def disp_brick(self, area):
        super().disp_brick(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._removed == 0:
            if self.__brickType == 1:
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.MAGENTA + Fore.BLACK + '@'
            elif self.__brickType == 2:
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.YELLOW + Fore.BLACK + '#'
            elif self.__brickType == 3:
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.BLUE + Fore.BLACK + '$'
            elif self.__brickType == 4:  # max strength
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.GREEN + Fore.BLACK + '%'


class UnbreakableBrick(Brick):
    def disp_brick(self, area):
        super().disp_brick(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._removed == 0:
            for i in range(a, a+6):
                for j in range(b, b+2):
                    area._gameArea[j][i] = Back.CYAN + Fore.BLACK + 'U'


class ExplodingBrick(Brick):
    def __init__(self, posX, posY):
        super().__init__(posX, posY)
        self._subtype = 2

    def disp_brick(self, area):
        super().disp_brick(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._removed == 0:
            for i in range(a, a+6):
                for j in range(b, b+2):
                    area._gameArea[j][i] = Back.LIGHTYELLOW_EX + Fore.BLACK + '?'


class RainbowBrick(Brick):
    def __init__(self, posX, posY, brickType):
        super().__init__(posX, posY)
        self.__brickType = random.randint(1, 4)  # 4,3,2,1 ;  implies trength as well ;  4 means max strength
        self._subtype = 3
        self._rainbow = 1

    def get_brickType(self):
        return self.__brickType

    def set_rainbow(self, val):
        self._rainbow = val

    def set_brickType(self, val):
        self.__brickType = val

    def disp_brick(self, area):
        super().disp_brick(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._removed == 0:
            if self.__brickType == 1:
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.MAGENTA + Fore.BLACK + '@'
            elif self.__brickType == 2:
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.YELLOW + Fore.BLACK + '#'
            elif self.__brickType == 3:
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.BLUE + Fore.BLACK + '$'
            elif self.__brickType == 4:  # max strength
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.GREEN + Fore.BLACK + '%'


class BreakableBrickNoPowerup(Brick):
    def __init__(self, posX, posY, brickType):
        super().__init__(posX, posY)
        self.__brickType = brickType  # 4,3,2,1 ;  implies trength as well ;  4 means max strength
        self._subtype = 4

    def get_brickType(self):
        return self.__brickType

    def set_brickType(self, val):
        self.__brickType = val

    def disp_brick(self, area):
        super().disp_brick(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._removed == 0:
            if self.__brickType == 1:
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.MAGENTA + Fore.BLACK + '@'
            elif self.__brickType == 2:
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.YELLOW + Fore.BLACK + '#'
            elif self.__brickType == 3:
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.BLUE + Fore.BLACK + '$'
            elif self.__brickType == 4:  # max strength
                for i in range(a, a+6):
                    for j in range(b, b+2):
                        area._gameArea[j][i] = Back.GREEN + Fore.BLACK + '%'
