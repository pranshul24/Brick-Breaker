from colorama import Fore, Back, Style
import time
import random
import math
from powerup import PowerUp, ShrinkPaddlePowerup, ExpandPaddlePowerup, ThruBallPowerup, GrabPowerup, FastBallPowerup, MultipleBallsPowerup, PaddleShootLaserPowerup, FireballPowerup
import os


class Laser():
    def __init__(self, posX, posY, downRange, upRange, leftRange, rightRange):
        self.__posX = posX
        self.__posY = posY
        self.__startSpeedY = int(-1)
        self.__upRange = upRange
        self.__downRange = downRange
        self.__leftRange = leftRange
        self.__rightRange = rightRange
        self.__speedY = int(-1)
        self.__removed = 0
        self.__speedX = 0

    def get_removed(self):
        return self.__removed

    def get_posY(self):
        return self.__posY

    def get_posX(self):
        return self.__posX

    def get_speedY(self):
        return self.__speedY

    def disp_laser(self, area):
        if self.__removed == 1:
            return
        a = int(self.__posX)
        b = int(self.__posY)
        area._gameArea[b][a] = Back.LIGHTBLUE_EX + Fore.BLACK + '|'

    def moveLaser(self, paddle_posX, paddle_len, bricks, powerups, totBalls, lifeNum, curSeconds, start):
        retv = 0

        if self.__speedY == 0 or self.__removed == 1:
            return 0
        p = self.check_bricks_collision(bricks, powerups, paddle_posX, paddle_len, totBalls, lifeNum, curSeconds)
        if p == 1:
            self.__removed = 1
            return 0
        elif p >= 2:
            return p
        m = self.check_wall_collisionY(paddle_len,  start)

        if m == 0:
            self.__posY += self.__speedY
        elif m == 1:
            self.__removed = 1
        return 0

    def check_wall_collisionY(self, paddle_len, start):
        k = 0
        if self.__posY+self.__speedY < self.__upRange:
            k = 1
        return k

    def check_bricks_collision(self, bricks, powerups, paddle_posX, paddle_len, totBalls, lifeNum, curSeconds):
        tem = 0
        explode = 0
        for i in range(len(bricks)):
            if bricks[i].get_removed() == 1:
                continue
            if self.__posX >= (bricks[i].get_posX()) and self.__posY == bricks[i].get_posY()+2 and self.__posX <= (bricks[i].get_posX()+5) and self.__speedY < 0 and self.inside_brick(bricks) == 0:
                # collision with lower side
                tem = 1

            if tem == 1:
                bricks[i]._brokenAtLife = lifeNum
                bricks[i]._brokenAtTime = curSeconds
                if bricks[i]._subtype == 0:
                    if bricks[i].get_brickType() == 1:
                        bricks[i]._removed = 1
                        self.launch_powerup(bricks[i], powerups, paddle_posX, paddle_len, totBalls)
                        os.system("aplay sounds/brickBreak.wav -q &")

                    else:
                        val = bricks[i].get_brickType()
                        bricks[i].set_brickType(val-1)
                        os.system("aplay sounds/ballHitWallBrick.wav -q &")

                elif bricks[i]._subtype == 2:
                    explode = 1
                elif bricks[i]._subtype == 3:
                    if bricks[i].get_rainbow() == 1:
                        bricks[i].set_rainbow(0)
                        os.system("aplay sounds/ballHitWallBrick.wav -q &")
                    else:
                        if bricks[i].get_brickType() == 1:
                            bricks[i]._removed = 1
                            self.launch_powerup(bricks[i], powerups, paddle_posX, paddle_len, totBalls)
                            os.system("aplay sounds/brickBreak.wav -q &")
                        else:
                            val = bricks[i].get_brickType()
                            bricks[i].set_brickType(val-1)
                            os.system("aplay sounds/ballHitWallBrick.wav -q &")

                break

        if explode == 1:
            tem = 2+i
        return tem

    def launch_powerup(self, brick, powerups, paddle_posX, paddle_len, totBalls):
        a = random.randint(1, 10)
        if a >= 3:  # then only launch powerup (kept 80% chance of launch)
            mult = 0
            grab = 0
            for i in range(len(powerups)):
                if totBalls > 1:
                    mult = 1
                if powerups[i]._powerupType == 6:
                    grab = 1
            b = random.randint(7, 7)
            if mult == 1 and b == 6:
                b = random.randint(1, 2)
            elif grab == 1 and b == 3:
                b = random.randint(1, 2)
            max_time = random.randint(70, 120)  # change it based on testing

            if b == 4:
                max_time = random.randint(40, 60)
            if b == 1:
                powerups.append(ShrinkPaddlePowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 2:
                powerups.append(ExpandPaddlePowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 3:
                powerups.append(MultipleBallsPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 4:
                powerups.append(FastBallPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 5:
                powerups.append(ThruBallPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 6:
                powerups.append(GrabPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 7:
                powerups.append(PaddleShootLaserPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 8:
                powerups.append(FireballPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))

    def inside_brick(self, bricks):
        tem = 0
        for brick in bricks:
            if brick._subtype == 1 and brick._removed == 0 and self.__posX >= brick._posX and self.__posY <= (brick._posY+1) and self.__posY >= brick._posY and self.__posX <= (brick._posX+5):
                tem = 1
                break
            elif brick._subtype == 0 and brick._removed == 0 and self.__posX >= brick._posX and self.__posY <= (brick._posY+1) and self.__posY >= brick._posY and self.__posX <= (brick._posX+5):
                tem = 1
                break
            elif brick._subtype == 4 and brick._removed == 0 and self.__posX >= brick._posX and self.__posY <= (brick._posY+1) and self.__posY >= brick._posY and self.__posX <= (brick._posX+5):
                tem = 1
                break
        return tem
