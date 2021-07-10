from colorama import Fore, Back, Style
import time
import random
import math
import os


class PowerUp:
    def __init__(self, posX, posY, powerupType, max_time, downRange, paddle_posX, paddle_len, speedY, speedX, leftRange, rightRange, upRange):
        self._posX = posX
        self._posY = posY
        self._removed = 0
        self._speedY = speedY
        self._speedX = speedX
        self._taken = 0  # tells ever taken
        self._maxTime = max_time
        self._timeDone = 0
        self._completed = 0  # tells if completed
        self._downRange = downRange
        self._upRange = upRange
        self._leftRange = leftRange
        self._rightRange = rightRange-1
        self._powerupType = powerupType  # 1->shrink paddle ; 2->expand paddle ; 3->ball multiplier ; 4->fast ball ; 5-> thru ball ; 6-> paddle grab ;7 -> paddle shoot lasers

    def get_taken(self):
        return self._taken

    def get_powerupType(self):
        return self._powerupType

    def get_timeLeftAfterTaken(self):
        return self._maxTime-self._timeDone

    def disp_powerup(self, area):
        a = int(self._posX)
        b = int(self._posY)
        if self._taken == 1:
            return

    def ExecuteBallPowerup(self, balls):
        pass

    def movePowerup(self, paddle_posX, paddle_len):
        if self._taken == 1:
            return 0
        m = self.check_wall_collisionY(paddle_posX, paddle_len)
        k = self.check_wall_collisionX()
        if k == 0:
            self._posX += self._speedX
        elif k == 1:
            self._posX = self._leftRange + (-1*self._speedX-(self._posX-self._leftRange))
            self._speedX = -1*self._speedX
            os.system("aplay sounds/ballHitWallBrick.wav -q &")

        elif k == 2:
            self._posX = self._rightRange - (self._speedX-(self._rightRange-self._posX))
            self._speedX = -1*self._speedX
            os.system("aplay sounds/ballHitWallBrick.wav -q &")

        retv = 0
        if m == 0:
            self._posY += self._speedY
            if self._speedY < 0:
                self._speedY = self._speedY+0.08
            else:
                self._speedY = self._speedY+0.093

        elif m == 1:
            self.takenPowerup()
            retv = self._powerupType
            os.system("aplay sounds/powerup.wav -q &")

        elif m == 2:
            self._removed = 1
            retv = 10
        elif m == 3:
            # upper wall collision
            self._posY = self._upRange + (-1*self._speedY-(self._posY-self._upRange))
            self._speedY = -1*self._speedY
            os.system("aplay sounds/ballHitWallBrick.wav -q &")

        return retv  # 0 when already taken before or powerup moving in area

    def check_wall_collisionX(self):
        k = 0
        if self._posX+self._speedX < self._leftRange:
            k = 1
        elif self._posX+self._speedX > self._rightRange:
            k = 2
        return k

    def check_wall_collisionY(self, paddle_posX, paddle_len):
        k = 0
        if self._posY+self._speedY < self._upRange:
            k = 3
        elif self._posY + self._speedY > self._downRange:
            k = self.check_paddle_collision(paddle_posX, paddle_len)
        return k

    def check_paddle_collision(self, paddle_posX, paddle_len):
        k = 0
        if self._posY+self._speedY > self._downRange:
            k = self.check_paddle_collisionX(paddle_posX, paddle_len)  # 1 for taken 2 for powerup lost
        return k

    def check_paddle_collisionX(self, paddle_posX, paddle_len):
        k = 2
        if self._posX >= paddle_posX-1 and self._posX <= (paddle_posX+paddle_len-1):
            k = 1
        return k

    def takenPowerup(self):
        self._taken = 1

    def incTime(self):
        retv = 0
        self._timeDone += 1
        if self._timeDone >= self._maxTime:
            self._completed = 1
            retv = self._powerupType
        return retv

    def extendMaxTime(self, extendTime):
        self._maxTime += extendTime


class ThruBallPowerup(PowerUp):
    def disp_powerup(self, area):
        super().disp_powerup(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._taken == 0:
            for i in range(a, a+2):
                for j in range(b, b+1):
                    area._gameArea[j][i] = Back.LIGHTYELLOW_EX + Fore.BLACK + 'T'

    def ExecuteBallPowerup(self, balls):
        k = len(balls)
        for ind in range(k):
            balls[ind].set_thru(1)


class GrabPowerup(PowerUp):
    def disp_powerup(self, area):
        super().disp_powerup(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._taken == 0:
            for i in range(a, a+2):
                for j in range(b, b+1):
                    area._gameArea[j][i] = Back.CYAN + Fore.BLACK + 'G'


class ExpandPaddlePowerup(PowerUp):
    def disp_powerup(self, area):
        super().disp_powerup(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._taken == 0:
            for i in range(a, a+2):
                for j in range(b, b+1):
                    area._gameArea[j][i] = Back.YELLOW + Fore.BLACK + 'E'


class ShrinkPaddlePowerup(PowerUp):
    def disp_powerup(self, area):
        super().disp_powerup(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._taken == 0:
            for i in range(a, a+2):
                for j in range(b, b+1):
                    area._gameArea[j][i] = Back.MAGENTA + Fore.BLACK + 'S'


class FastBallPowerup(PowerUp):
    def disp_powerup(self, area):
        super().disp_powerup(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._taken == 0:
            for i in range(a, a+2):
                for j in range(b, b+1):
                    area._gameArea[j][i] = Back.GREEN + Fore.BLACK + 'F'


class MultipleBallsPowerup(PowerUp):
    def disp_powerup(self, area):
        super().disp_powerup(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._taken == 0:
            for i in range(a, a+2):
                for j in range(b, b+1):
                    area._gameArea[j][i] = Back.BLUE + Fore.BLACK + 'B'

    def ExecuteBallPowerup(self, balls):
        k = int(len(balls)/2)
        for ind in range(0, k):
            balls[k+ind].setSpeed(-1*balls[ind].get_speedX(), -1*balls[ind].get_speedY())


class PaddleShootLaserPowerup(PowerUp):
    def disp_powerup(self, area):
        super().disp_powerup(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._taken == 0:
            for i in range(a, a+2):
                for j in range(b, b+1):
                    area._gameArea[j][i] = Back.LIGHTBLUE_EX + Fore.BLACK + 'L'


class FireballPowerup(PowerUp):
    def disp_powerup(self, area):
        super().disp_powerup(area)
        a = int(self._posX)
        b = int(self._posY)
        if self._taken == 0:
            for i in range(a, a+2):
                for j in range(b, b+1):
                    area._gameArea[j][i] = Back.LIGHTMAGENTA_EX + Fore.BLACK + 'D'

    def ExecuteBallPowerup(self, balls):
        k = len(balls)
        for ind in range(k):
            balls[ind].set_fireball(1)
