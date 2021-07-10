from colorama import Fore, Back, Style
import time
import random
import math
from powerup import PowerUp, ShrinkPaddlePowerup, ExpandPaddlePowerup, ThruBallPowerup, GrabPowerup, FastBallPowerup, MultipleBallsPowerup, PaddleShootLaserPowerup, FireballPowerup
import os


class Ball:
    def __init__(self, posX, posY, leftRange, rightRange, upRange, downRange, mainBall, maxTime, grabbed):
        self.__posX = random.randint(posX+1, posX+1)  # change to -3 to +3
        self.__posY = posY
        self.__startSpeedX = int(self.__posX-posX)
        self.__startSpeedY = int(-1)
        self.__leftRange = leftRange
        self.__rightRange = rightRange
        self.__upRange = upRange
        self.__downRange = downRange
        self.__speedX = 0
        self.__speedY = 0
        self.__removed = 0
        self.__mainBall = mainBall
        self.__timeDone = 0
        self.__maxTime = maxTime
        self.__thru = 0
        self.__grabbed = grabbed  # ball is grabbed or not
        self.__revX = 0
        self.__revY = 0
        self.__fireball = 0

    def get_removed(self):
        return self.__removed

    def get_posX(self):
        return self.__posX

    def get_posY(self):
        return self.__posY

    def set_posY(self, val):
        self.__posY = val

    def get_speedX(self):
        return self.__speedX

    def get_speedY(self):
        return self.__speedY

    def get_grabbed(self):
        return self.__grabbed

    def set_thru(self, val):
        self.__thru = val

    def set_fireball(self, val):
        self.__fireball = val

    def get_rightRange(self):
        return self.__rightRange

    def get_downRange(self):
        return self.__downRange

    def disp_ball(self, area):
        if self.__removed == 1:
            return
        a = int(self.__posX)
        b = int(self.__posY)
        area._gameArea[b][a] = Back.RED + Fore.BLACK + 'O'

    def right(self):
        self.__posX += 1

    def left(self):
        self.__posX -= 1

    def setSpeed(self, startSpeedX, startSpeedY):
        self.__startSpeedY = startSpeedY
        self.__startSpeedX = startSpeedX
        self.__speedY = startSpeedY
        self.__speedX = startSpeedX

    def start_move(self, paddle_posX, paddle_len, bricks, paddle_grabbed, powerups, totBalls, lifeNum, curSeconds, enemy):
        self.__speedY = -1
        self.__speedX = self.__startSpeedX
        self.__grabbed = 0
        self.moveBall(paddle_posX, paddle_len, bricks, paddle_grabbed, powerups, totBalls, lifeNum, curSeconds, enemy,
                      start=int(1))  # 1 implies started otherwise fixed on paddle

    def moveBall(self, paddle_posX, paddle_len, paddle_grabbed,  bricks, powerups, totBalls, lifeNum, curSeconds, enemy, start):
        retv = 0

        if self.__speedY == 0 or self.__removed == 1:
            return 0
        c = 0
        if enemy != 0:
            c = self.check_enemy_collision(enemy)
        if c == 2:
            return 2
        p = self.check_bricks_collision(bricks, powerups, paddle_posX, paddle_len, totBalls, lifeNum, curSeconds)
        if p == 1:
            return 0
        elif p >= 3:
            return p
        m = self.check_wall_collisionY(paddle_posX, paddle_len, paddle_grabbed, start)
        k = self.check_wall_collisionX()
        if k == 0:
            if self.__grabbed == 0:
                self.__posX += self.__speedX
        elif k == 1:
            self.__posX = self.__leftRange + (-1*self.__speedX-(self.__posX-self.__leftRange))
            self.__speedX = -1*self.__speedX
        elif k == 2:
            self.__posX = self.__rightRange - (self.__speedX-(self.__rightRange-self.__posX))
            self.__speedX = -1*self.__speedX

        if m == 0:
            if self.__grabbed == 0:  # this change
                self.__posY += self.__speedY
        elif m == 1:
            self.__posY = self.__upRange + (-1*self.__speedY-(self.__posY-self.__upRange))
            self.__speedY = -1*self.__speedY
        elif m == 2:
            if start == 0:
                if self.__grabbed == 0:
                    self.__posY = self.__downRange-1
                    self.__speedY = -1*self.__speedY
            else:
                self.__posY = self.__downRange-1

            return 1  # now will check if bricks down feature is trigerred or not

        elif m == 3:
            self.__removed = 1

        return 0

    def check_wall_collisionX(self):
        k = 0
        if self.__posX+self.__speedX <= self.__leftRange:
            k = 1
            os.system("aplay sounds/ballHitWallBrick.wav -q &")
        elif self.__posX+self.__speedX >= self.__rightRange:
            k = 2
            os.system("aplay sounds/ballHitWallBrick.wav -q &")

        return k

    def check_wall_collisionY(self, paddle_posX, paddle_len, paddle_grabbed, start):
        k = 0
        if self.__posY+self.__speedY <= self.__upRange:
            k = 1
            os.system("aplay sounds/ballHitWallBrick.wav -q &")
        elif self.__posY == self.__downRange:
            k = self.check_paddle_collision(paddle_posX, paddle_len, paddle_grabbed, start)  # 2 for rebound 3 for ball lost
        return k

    def check_paddle_collision(self, paddle_posX, paddle_len, paddle_grabbed, start):
        k = 3
        if self.__posX >= paddle_posX and self.__posX <= (paddle_posX+paddle_len-1):
            k = 2
            if start == 0 and paddle_grabbed == 1:
                self.__grabbed = 1
                # follow expected trajectory when released
                self.__startSpeedX = self.__speedX + (self.__posX-(paddle_posX+math.floor(paddle_len/2)))
                if self.__startSpeedX > 4:
                    self.__startSpeedX = 4
                elif self.__startSpeedX < -4:
                    self.__startSpeedX = -4
                self.__speedY = 0
                self.__speedX = 0
            elif start == 0:
                self.__speedX += (self.__posX-(paddle_posX+math.floor(paddle_len/2)))
                if self.__speedX > 4:
                    self.__speedX = 4
                elif self.__speedX < -4:
                    self.__speedX = -4
            os.system("aplay sounds/ballHitPaddle.wav -q &")

        return k

    def check_enemy_collision(self, enemy):
        tem = 0
        if self.__posX >= (enemy.get_posX()) and self.__posY == enemy.get_posY()-1 and self.__posX <= (enemy.get_posX()+34) and self.__speedY > 0 and self.inside_enemy(enemy) == 0:
            # collision with upper side
            tem = 1
            self.__posY = self.__posY-1
            self.__posX = self.__posX+self.__speedX
            self.__speedY = -1*self.__speedY

        elif self.__posX >= (enemy.get_posX()) and self.__posY == enemy.get_posY()+8 and self.__posX <= (enemy.get_posX()+34) and self.__speedY < 0 and self.inside_enemy(enemy) == 0:
            # collision with lower side
            tem = 1
            self.__posY = self.__posY+1
            self.__posX = self.__posX+self.__speedX
            self.__speedY = -1*self.__speedY

        elif self.__posX >= enemy.get_posX() and self.__posY <= (enemy.get_posY()+7) and self.__posY >= enemy.get_posY() and self.__posX <= (enemy.get_posX()+17) and self.__speedX > 0:
            # collision with left side
            tem = 1
            self.__posX = enemy.get_posX()-1
            self.__speedX = -1*self.__speedX

        elif self.__posX >= enemy.get_posX() and self.__posY <= (enemy.get_posY()+7) and self.__posY >= enemy.get_posY() and self.__posX <= (enemy.get_posX()+17) and self.__speedX <= 0:
            # collision with left side when paddle is moving left continuously
            tem = 1
            if self.__posX > self.__leftRange:
                self.__posX = enemy.get_posX()-1
            if self.__speedX == 0:
                self.__speedX = -2

        elif self.__posX >= enemy.get_posX()+17 and self.__posY <= (enemy.get_posY()+7) and self.__posY >= enemy.get_posY() and self.__posX <= (enemy.get_posX()+35) and self.__speedX < 0:
            # collision with right side
            tem = 1
            self.__posX = enemy.get_posX()+35
            self.__speedX = -1*self.__speedX

        elif self.__posX >= enemy.get_posX()+17 and self.__posY <= (enemy.get_posY()+7) and self.__posY >= enemy.get_posY() and self.__posX <= (enemy.get_posX()+34) and self.__speedX >= 0:
            # collision with right side when paddle is moving right continuously
            tem = 1
            self.__posX = enemy.get_posX()+35
            if self.__speedX == 0:
                self.__speedX = 1

        if tem == 1:
            enemy.enemyHitByBall()
            os.system("aplay sounds/ballHitEnemy.wav -q &")
            return 2
        return 0

    def check_bricks_collision(self, bricks, powerups, paddle_posX, paddle_len, totBalls, lifeNum, curSeconds):
        tem = 0
        explode = 0

        for i in range(len(bricks)):
            if bricks[i].get_removed() == 1:
                continue
            if self.__posX >= (bricks[i].get_posX()) and self.__posY == bricks[i].get_posY()-1 and self.__posX <= (bricks[i].get_posX()+5) and self.__speedY > 0 and self.inside_brick(bricks) == 0:
                # collision with upper side
                tem = 1
                if self.__thru == 0:
                    self.__posY = self.__posY-1
                    self.__posX = self.__posX+self.__speedX
                    self.__speedY = -1*self.__speedY
                    self.__revY = 1
                else:
                    self.__posY = self.__posY+1
                    bricks[i].set_removed(1)
            elif self.__posX >= (bricks[i].get_posX()) and self.__posY == bricks[i].get_posY()+2 and self.__posX <= (bricks[i].get_posX()+5) and self.__speedY < 0 and self.inside_brick(bricks) == 0:
                # collision with lower side
                tem = 1
                if self.__thru == 0:
                    self.__posY = self.__posY+1
                    self.__posX = self.__posX+self.__speedX
                    self.__speedY = -1*self.__speedY
                    self.__revY = 1

                else:
                    self.__posY = self.__posY-1
                    bricks[i].set_removed(1)
            elif self.__posX >= bricks[i].get_posX()-1 and self.__posY <= (bricks[i].get_posY()+1) and self.__posY >= bricks[i].get_posY() and self.__posX <= (bricks[i].get_posX()+5) and self.__speedX > 0:
                # collision with left side
                tem = 1
                if self.__thru == 0:
                    self.__posX = bricks[i]._posX-1
                    self.__speedX = -1*self.__speedX
                    self.__revX = 1

                else:
                    self.__posX = bricks[i]._posX-1
                    bricks[i].set_removed(1)

            elif self.__posX >= bricks[i]._posX and self.__posY <= (bricks[i]._posY+1) and self.__posY >= bricks[i]._posY and self.__posX <= (bricks[i]._posX+6) and self.__speedX < 0:
                # collision with right side
                tem = 1
                if self.__thru == 0:
                    self.__posX = bricks[i]._posX+6
                    self.__speedX = -1*self.__speedX
                    self.__revX = 1

                else:
                    self.__posX = bricks[i]._posX+6
                    bricks[i].set_removed(1)

            if tem == 1:
                bricks[i]._brokenAtLife = lifeNum
                bricks[i]._brokenAtTime = curSeconds
                if self.__fireball == 1:
                    os.system("aplay sounds/explosion.wav -q &")
                    return 3+i

                if bricks[i]._subtype == 0:
                    if bricks[i].get_brickType() == 1 or self.__thru == 1:
                        bricks[i]._removed = 1
                        self.launch_powerup(bricks[i], powerups, paddle_posX, paddle_len, totBalls)
                        os.system("aplay sounds/brickBreak.wav -q &")

                    else:
                        val = bricks[i].get_brickType()
                        bricks[i].set_brickType(val-1)
                        os.system("aplay sounds/ballHitWallBrick.wav -q &")

                elif bricks[i]._subtype == 2:
                    explode = 1
                    self.launch_powerup(bricks[i], powerups, paddle_posX, paddle_len, totBalls)
                elif bricks[i]._subtype == 3:
                    if bricks[i].get_rainbow() == 1:
                        if self.__thru == 1:
                            bricks[i]._removed = 1
                            self.launch_powerup(bricks[i], powerups, paddle_posX, paddle_len, totBalls)
                            os.system("aplay sounds/brickBreak.wav -q &")
                        else:
                            os.system("aplay sounds/ballHitWallBrick.wav -q &")
                        bricks[i].set_rainbow(0)

                    else:
                        if bricks[i].get_brickType() == 1 or self.__thru == 1:
                            bricks[i]._removed = 1
                            self.launch_powerup(bricks[i], powerups, paddle_posX, paddle_len, totBalls)
                            os.system("aplay sounds/brickBreak.wav -q &")

                        else:
                            val = bricks[i].get_brickType()
                            bricks[i].set_brickType(val-1)
                            os.system("aplay sounds/ballHitWallBrick.wav -q &")

                elif bricks[i]._subtype == 4:
                    val = bricks[i].get_brickType()
                    bricks[i].set_brickType(val-1)
                    if val == 1:
                        bricks[i].set_removed(1)
                        os.system("aplay sounds/brickBreak.wav -q &")
                    else:
                        os.system("aplay sounds/ballHitWallBrick.wav -q &")

                elif bricks[i]._subtype == 1:
                    os.system("aplay sounds/ballHitWallBrick.wav -q &")
                    if self.__thru == 1:
                        self.launch_powerup(bricks[i], powerups, paddle_posX, paddle_len, totBalls)

                break

        self.__revX = 0
        self.__revY = 0

        if explode == 1:
            tem = 3+i
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
            b = random.randint(1, 8)
            if mult == 1 and b == 6:
                b = random.randint(1, 2)
            elif grab == 1 and b == 3:
                b = random.randint(1, 2)
            max_time = random.randint(70, 120)  # change it based on testing

            if b == 4:
                max_time = random.randint(40, 60)
            if b == 1:
                if self.__revX == 1:
                    powerups.append(ShrinkPaddlePowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, -1*self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                elif self.__revY == 1:
                    powerups.append(ShrinkPaddlePowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, -1*self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                else:
                    powerups.append(ShrinkPaddlePowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))

            elif b == 2:
                if self.__revX == 1:
                    powerups.append(ExpandPaddlePowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, -1*self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                elif self.__revY == 1:
                    powerups.append(ExpandPaddlePowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, -1*self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                else:
                    powerups.append(ExpandPaddlePowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))

            elif b == 3:
                if self.__revX == 1:
                    powerups.append(MultipleBallsPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, -1*self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                elif self.__revY == 1:
                    powerups.append(MultipleBallsPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, -1*self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                else:
                    powerups.append(MultipleBallsPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 4:
                if self.__revX == 1:
                    powerups.append(FastBallPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, -1*self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                elif self.__revY == 1:
                    powerups.append(FastBallPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, -1*self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                else:
                    powerups.append(FastBallPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 5:
                if self.__revX == 1:
                    powerups.append(ThruBallPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, -1*self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                elif self.__revY == 1:
                    powerups.append(ThruBallPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, -1*self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                else:
                    powerups.append(ThruBallPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 6:
                if self.__revX == 1:
                    powerups.append(GrabPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, -1*self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                elif self.__revY == 1:
                    powerups.append(GrabPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, -1*self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                else:
                    powerups.append(GrabPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 7:
                if self.__revX == 1:
                    powerups.append(PaddleShootLaserPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, -1*self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                elif self.__revY == 1:
                    powerups.append(PaddleShootLaserPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, -1*self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                else:
                    powerups.append(PaddleShootLaserPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
            elif b == 8:
                if self.__revX == 1:
                    powerups.append(FireballPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, self.__speedY, -1*self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                elif self.__revY == 1:
                    powerups.append(FireballPowerup(brick._posX+2, brick._posY+2, b, max_time, self.__downRange, paddle_posX, paddle_len, -1*self.__speedY, self.__speedX, self.__leftRange, self.__rightRange, self.__upRange))
                else:
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

    def inside_enemy(self, enemy):
        tem = 0
        if self.__posX >= enemy.get_posX() and self.__posY <= (enemy.get_posY()+7) and self.__posY >= enemy.get_posY() and self.__posX <= (enemy.get_posX()+34):
            tem = 1
        return tem
