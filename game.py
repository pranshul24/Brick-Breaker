import os
import numpy as np
from colorama import Fore, Back, Style
import random
import time
from paddle import Paddle
from Ball import Ball
from input import *
from area import Area
from brick import BreakableBrick, UnbreakableBrick, ExplodingBrick, RainbowBrick, BreakableBrickNoPowerup
from powerup import PowerUp
from laser import Laser
from enemy import Enemy
from bomb import Bomb
rBuf = 41
dBuf = 4
minHeight = 20
minWidth = 60


class Game:

    def __init__(self):
        rows, columns = os.popen('stty size', 'r').read().split()
        rows = int(rows)
        columns = int(columns)
        self._height = rows - dBuf
        self._width = columns - rBuf
        if self._height < minHeight or self._width < minWidth:
            print(
                Fore.LIGHTMAGENTA_EX + 'Less space for playing !')
            raise SystemExit
        self._area = Area(self._height, self._width)
        self.__gameSpeed = 0.1
        self.__loops = 1
        self.__explodeBricks = []
        self.__lives = 3
        self.__next = 0
        self.__score = 0
        self.__spawnBricks = 0
        self.__spawned = 0
        self.__totScorePrevLevels = 0
        self.__time = 0
        self.__nextLevel = 0
        self._balls = []
        self._bombs = []
        self._lasers = []
        self._bricks = []
        self._enemy = 0
        self._bricksTouchedDown = 0
        self._bricksTouchedDownBall = 0
        self._powerups = []
        self.__prevStateTime = 0
        self.__prevLevelEndTime = 0
        self.__getInput = KBHit()
        self.__completed = 0
        self.__quit = 0
        self.__levelNum = 1
        self.__dispLaserTime = 0
        self.__dispHealth = 0
        self.__healthZero = 0
        self._paddle = Paddle(int(9), self._width/2-3,
                              self._height-3, int(2), self._width)
        self.__initialBricks = 0

    def createLayoutLevel1(self):
        self._bricks.clear()
        for i in range(3):
            for j in range(7+2*i):
                if i == 0:
                    if j == 2 or j == 6:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    elif j == 4:
                        self._bricks.append(ExplodingBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    elif j == 1 or j == 5:
                        self._bricks.append(RainbowBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))
                if i == 1:
                    if j == 0 or j == 5:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    elif j == 2 or j == 6:
                        pass
                    elif j == 1 or j == 3:
                        self._bricks.append(RainbowBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))
                    elif j == 4 or j == 8:
                        self._bricks.append(ExplodingBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))
                if i == 2:
                    if j == 10:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    elif j == 4 or j == 8:
                        self._bricks.append(ExplodingBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    elif j == 1 or j == 3 or j == 9 or j == 6:
                        self._bricks.append(RainbowBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))

        for j in range(9):
            i = 1
            if j == 1 or j == 5:
                self._bricks.append(UnbreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (12)))
            elif j == 2 or j == 6:
                self._bricks.append(ExplodingBrick(((self._width-6*(7+2*i)-2)/2+6*j), (12)))
            else:
                self._bricks.append(BreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (12), random.randint(1, 4)))

        for i in range(3):
            for j in range(11-2*i):
                if i == 0:
                    if j == 11:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    elif j == 2 or j == 6:
                        self._bricks.append(ExplodingBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    elif j == 5 or j == 8:
                        self._bricks.append(RainbowBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))
                if i == 1:
                    if j == 7:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    elif j == 2 or j == 6:
                        pass
                    elif j == 8 or j == 0:
                        self._bricks.append(RainbowBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))
                    elif j == 0 or j == 4 or j == 7:
                        self._bricks.append(ExplodingBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))
                if i == 2:
                    if j == 3:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    elif j == 2:
                        self._bricks.append(ExplodingBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    elif j == 0 or j == 4:
                        self._bricks.append(RainbowBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))

    def createLayoutLevel2(self):
        self._bricks.clear()
        for i in range(3):
            for j in range(7+2*i):
                if i == 0:
                    if j == 2:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    elif j == 0 or j == 1 or j == 6:
                        pass
                    elif j == 4:
                        self._bricks.append(ExplodingBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    elif j == 5:
                        self._bricks.append(RainbowBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))
                if i == 1:
                    if j == 5:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    elif j == 2 or j == 7 or j == 0:
                        pass
                    elif j == 1 or j == 3:
                        self._bricks.append(RainbowBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))
                    elif j == 4 or j == 8:
                        self._bricks.append(ExplodingBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))
                if i == 2:
                    if j == 10:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    elif j == 0 or j == 6 or j == 5:
                        pass
                    elif j == 8 or j == 4:
                        self._bricks.append(ExplodingBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2)))
                    elif j == 1 or j == 3 or j == 9 or j == 6:
                        self._bricks.append(RainbowBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (6+i*2), random.randint(1, 4)))

        for j in range(10):
            i = 1
            if j == 1:
                self._bricks.append(UnbreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (12)))
            elif j == 4 or j == 5:
                pass
            elif j == 2 or j == 6:
                self._bricks.append(ExplodingBrick(((self._width-6*(7+2*i)-2)/2+6*j), (12)))
            else:
                self._bricks.append(BreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (12), random.randint(1, 4)))

        for i in range(3):
            for j in range(11-2*i):
                if i == 0:
                    if j == 11:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    elif j == 0:
                        pass
                    elif j == 2 or j == 6:
                        self._bricks.append(ExplodingBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    elif j == 5 or j == 8:
                        self._bricks.append(RainbowBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))
                if i == 1:
                    if j == 8:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    elif j == 2 or j == 7 or j == 0:
                        pass
                    elif j == 8:
                        self._bricks.append(RainbowBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))
                    elif j == 4:
                        self._bricks.append(ExplodingBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))
                if i == 2:
                    if j == 3:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    elif j == 0 or j == 1 or j == 6:
                        pass
                    elif j == 2:
                        self._bricks.append(ExplodingBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2)))
                    elif j == 4:
                        self._bricks.append(RainbowBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))
                    else:
                        self._bricks.append(BreakableBrick(((self._width-6*(11-2*i)-2)/2+6*j), (14+i*2), random.randint(1, 4)))

    def createLayoutLevel3(self):
        self._bricks.clear()
        self._enemy = Enemy(int(9), self._width/2-16,
                            int(3), int(2), self._width)

        for j in range(9):
            i = 1
            if j == 1 or j == 5:
                self._bricks.append(UnbreakableBrick(((self._width-6*(7+2*i)-2)/2+6*j), (12)))

        for i in range(3):
            for j in range(13-2*i):
                if i == 0:
                    if j == 0 or j == 12:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(13-2*i)-2)/2+6*j), (14+i*2)))
                if i == 1:
                    if j == 7:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(13-2*i)-2)/2+6*j), (14+i*2)))
                if i == 2:
                    if j == 3 or j == 0 or j == 8:
                        self._bricks.append(UnbreakableBrick(((self._width-6*(13-2*i)-2)/2+6*j), (14+i*2)))

    def FastBall(self):
        self.__loops = 2

    def gameOver(self):
        print(Style.RESET_ALL)
        os.system("killall aplay -q")
        os.system("aplay sounds/explosion.wav -q &")

        if self.__completed == 1:
            time.sleep(1)
        os.system('clear')
        os.system("stty -echo")
        arr = []
        file = "over.txt"
        if self.__quit == 1:
            file = "quit.txt"
        elif self.__completed == 1:
            file = "completed.txt"
        with open(file, 'r') as lines:
            for line in lines:
                arr.append(list(line.strip('\n')))
        over = np.array(arr, dtype='object')
        time.sleep(0.1)

        for i in range(0, over.shape[0]):
            for j in range(0, over.shape[1]):
                print(over[i][j], end='')
            print('')
        print("-----------------------------------------------------------------")
        print(Fore.RED+"Score : ", self.__score)
        print("Time Played : ", self.__time)
        if self.__completed == 1:
            print("Game Status : Completed")
            time.sleep(1)
        elif self.__quit == 1:
            print("Game Status : Exitted")
        else:
            print("Game Status : Not Completed")
            time.sleep(1)

    def flashLifeLost(self):
        self._area.print_lifeLost(1)
        time.sleep(0.1)
        self._area.print_lifeLost(0)
        time.sleep(0.1)
        self._area.print_lifeLost(1)
        self.__getInput.flush()

    def playBrickBreaker(self):
        while self.__levelNum < 4:
            if self.__levelNum == 3:
                os.system("aplay sounds/rasputin.wav -q &")
            if self.__lives == 0:
                break
            self.__next = 0
            self.__completed = 0
            self._balls.clear()
            self._bombs.clear()
            self._lasers.clear()
            self._powerups.clear()
            self._paddle.set_grabbed(0)
            self.__loops = 1
            self._paddle = Paddle(int(9), self._width/2-3,
                                  self._height-3, int(2), self._width)
            self._area.print_board(self._paddle, self._balls, self._bricks, self._powerups,
                                   self._lasers, self.__lives, self.__score, self.__time, self._enemy, self._bombs, self.__dispHealth, self.__dispLaserTime)
            curLevel = self.__levelNum
            if self.__levelNum == 1:
                self.createLayoutLevel1()
            elif self.__levelNum == 2:
                self.createLayoutLevel2()
            else:
                self.createLayoutLevel3()

            self.__initialBricks = 0
            for brick in self._bricks:
                if brick.get_subtype() == 0:
                    self.__initialBricks += 1
            self._balls.append(Ball(int(self._width/2)+1,
                                    self._height-4, int(2), self._width-3, int(1), self._height-4, 1, 0, 1))
            self._paddle = Paddle(int(9), self._width/2-3,
                                  self._height-3, int(2), self._width)
            self._area.print_board(self._paddle, self._balls, self._bricks, self._powerups,
                                   self._lasers, self.__lives, self.__score, self.__time, self._enemy, self._bombs, self.__dispHealth, self.__dispLaserTime)

            while self.__lives > 0:
                self.play()
                # if self.__levelNum == 3:
                #     self._enemy.set_posX(self._width/2-16)
                #     self._enemy.set_posY(int(1))
                if self._bricksTouchedDown == 1:
                    for brick in self._bricks:
                        lowpos = brick.shiftDown(1)
                    self._balls[0].set_posY(self._height-4)
                    self._area.print_board(self._paddle, self._balls, self._bricks, self._powerups,
                                           self._lasers, self.__lives, self.__score, self.__time, self._enemy, self._bombs, self.__dispHealth, self.__dispLaserTime)
                    time.sleep(1)
                    self.__levelNum = 4
                    break
                if self.__healthZero == 1:
                    break
                elif self.__nextLevel == 1:
                    self.__nextLevel = 0
                    break
                elif self.__completed == 1:
                    break
                elif self.__quit == 0:
                    os.system("aplay sounds/explosion.wav -q &")
                    self.flashLifeLost()
                    self.__next = 0
                    self._balls.clear()
                    self._lasers.clear()
                    self._powerups.clear()
                    self._bombs.clear()
                    self._paddle.set_grabbed(0)
                    self.__loops = 1
                    self._balls.append(Ball(int(self._width/2)+1,
                                            self._height-4, int(2), self._width-3, int(1), self._height-4, 1, 0, 1))
                    self._paddle = Paddle(int(9), self._width/2-3,
                                          self._height-3, int(2), self._width)

                    self._area.print_board(self._paddle, self._balls, self._bricks, self._powerups,
                                           self._lasers, self.__lives, self.__score, self.__time, self._enemy, self._bombs, self.__dispHealth, self.__dispLaserTime)
                    if self.__levelNum == 3:
                        self._enemy.set_posX(self._width/2-16)
                        self._enemy.set_posY(int(1))

            os.system("aplay sounds/explosion.wav -q &")
            self.__levelNum += 1
            self.__next = 0
            if self.__levelNum <= 3:
                self.__completed = 0
            self.flashLifeLost()
        self.gameOver()

    def play(self):
        self.__dispLaserTime = 0
        self.__getInput.flush()
        prevTime = time.time()
        inTime = time.time()
        while True:
            # val = (time.time()-inTime)
            self.__time = self.__prevStateTime + int(time.time()-inTime)
            curTime = time.time()
            if curTime-prevTime > self.__gameSpeed:
                for x in range(self.__loops):

                    if self.__time-self.__prevLevelEndTime >= 200:
                        self._paddle.set_bricksDown(1)

                    if self.__spawnBricks == 1 and self._balls[0].get_posY() > 10 and self.__spawned < 2:
                        remBrickList = []
                        self.__spawned += 1
                        for i in range(len(self._bricks)):
                            if self._bricks[i].get_subtype() == 4 and self._bricks[i].get_posY() < 11:
                                remBrickList.append(i)
                        for i in sorted(remBrickList, reverse=True):
                            del self._bricks[i]

                        for j in range(16):
                            i = 4
                            self._bricks.append(BreakableBrickNoPowerup(((self._width-6*(7+2*i)-2)/2+6*j)-2, (9), random.randint(1, 4)))
                        self.__spawnBricks = 0

                    totB = 0
                    remCnt = 0
                    for temv in self._bricks:
                        if temv.get_removed() == 1:
                            if temv.get_subtype() == 0:
                                remCnt += 1
                            if temv.get_brokenAtLife() == 1:
                                if temv.get_brokenAtTime()-self.__prevLevelEndTime > 15:
                                    totB += 17
                                else:
                                    totB += 20
                            elif temv.get_brokenAtLife() == 2:
                                if temv.get_brokenAtTime()-self.__prevLevelEndTime > 25:
                                    totB += 12
                                else:
                                    totB += 15
                            elif temv.get_brokenAtLife() == 3:
                                if temv.get_brokenAtTime()-self.__prevLevelEndTime > 35:
                                    totB += 7
                                else:
                                    totB += 10
                    if self.__levelNum == 3:
                        totB += (100-self.__dispHealth)*10
                    self.__score = self.__totScorePrevLevels + totB
                    if remCnt == self.__initialBricks and self.__levelNum < 3:
                        self.__completed = 1
                        self.__prevStateTime = self.__time
                        self.__prevLevelEndTime = self.__time
                        self.__totScorePrevLevels = self.__score
                        break

                    # find health at present
                    if self.__levelNum == 3:
                        if self.__completed == 0:
                            self.__dispHealth = self._enemy.get_enemyStrength()
                            if self.__dispHealth == 0:
                                self.__levelNum = 4
                                self.__healthZero = 1
                                self.__score += 100
                                break

                    # change rainbow bricks color
                    for i in range(len(self._bricks)):
                        if self._bricks[i].get_removed() == 1:
                            continue
                        if self._bricks[i].get_rainbow() == 1:
                            hardness_type = self._bricks[i].get_brickType()
                            self._bricks[i].set_brickType(random.choice([hardVal for hardVal in range(1, 5) if hardVal not in [hardness_type]]))

                    totExplodeBrick = len(self.__explodeBricks)
                    for temp in range(len(self.__explodeBricks)):
                        brick = self._bricks[self.__explodeBricks[temp]]
                        for temv in range(len(self._bricks)):
                            if abs(self._bricks[temv].get_posX()-brick.get_posX()) <= 6 and abs(self._bricks[temv].get_posY()-brick.get_posY()) <= 2:
                                if self._bricks[temv].get_subtype() == 2 and self._bricks[temv].get_removed() == 0 and temv != self.__explodeBricks[temp]:
                                    self.__explodeBricks.append(temv)
                                self._bricks[temv].set_removed(1)
                                self._bricks[temv].set_brokenAtLife(4-self.__lives)
                        os.system("aplay sounds/explosion.wav -q &")

                    del self.__explodeBricks[:totExplodeBrick]  # from start till totExplodeBrick
                    val = len(self._balls)

                    remBallList = []
                    enemyStrengthBeforeBallMove = 0
                    if self.__levelNum == 3:
                        enemyStrengthBeforeBallMove = self._enemy.get_enemyStrength()
                    for i in range(len(self._balls)):
                        retv = self._balls[i].moveBall(self._paddle.get_posX(), self._paddle.get_len(), self._paddle.get_grabbed(),
                                                       self._bricks, self._powerups, val, (4-self.__lives), self.__time, self._enemy, start=int(0))
                        if retv >= 3:
                            brick = self._bricks[retv-3]
                            for temv in range(len(self._bricks)):
                                if abs(self._bricks[temv].get_posX()-brick.get_posX()) <= 6 and abs(self._bricks[temv].get_posY()-brick.get_posY()) <= 2:
                                    if self._bricks[temv].get_subtype() == 2 and temv != retv-3:
                                        self.__explodeBricks.append(temv)
                                    self._bricks[temv].set_removed(1)
                                    self._bricks[temv].set_brokenAtLife(4-self.__lives)
                            os.system("aplay sounds/explosion.wav -q &")

                            # if self._bricks[temv].get_subtype() == 2 and temv == retv-2:
                            #     self._balls[i].launch_powerup(self._bricks[temv], self._powerups,
                            #                                   self._paddle.get_posX(), self._paddle.get_len(), val)

                        # brickdown feature
                        if retv == 1:
                            if self._paddle.get_bricksDown() == 1:
                                lowpos = 0
                                for brick in self._bricks:
                                    tempos = brick.shiftDown(1)
                                    if brick.get_removed() == 0:
                                        lowpos = max(tempos, lowpos)

                                if lowpos == self._height-6:
                                    self._bricksTouchedDown = 1

                        # ball hit enemy
                        if retv == 2 and self.__levelNum == 3 and self._enemy.get_enemyStrength() < enemyStrengthBeforeBallMove:
                            if self._enemy.get_enemyStrength() == 50:
                                # spawn bricks
                                self.__spawnBricks = 1
                            elif self._enemy.get_enemyStrength() == 20:
                                self.__spawnBricks = 1

                    if self._bricksTouchedDown == 1:
                        break

                    for i in range(len(self._balls)):
                        if self._balls[i].get_removed() == 1:
                            remBallList.append(i)
                    for i in sorted(remBallList, reverse=True):
                        del self._balls[i]
                    if len(self._balls) == 0:
                        self.__lives -= 1
                        self.__prevStateTime = self.__time
                        self.__next = 1
                        break

                    remLaserList = []
                    val2 = len(self._lasers)
                    for i in range(len(self._lasers)):
                        retv = self._lasers[i].moveLaser(self._paddle.get_posX(), self._paddle.get_len(),
                                                         self._bricks, self._powerups, val2, (4-self.__lives), self.__time, start=int(0))
                        if retv >= 2:
                            brick = self._bricks[retv-2]
                            for temv in range(len(self._bricks)):
                                if abs(self._bricks[temv].get_posX()-brick.get_posX()) <= 6 and abs(self._bricks[temv].get_posY()-brick.get_posY()) <= 2:
                                    if self._bricks[temv].get_subtype() == 2 and temv != retv-2:
                                        self.__explodeBricks.append(temv)
                                    self._bricks[temv].set_removed(1)
                                    self._bricks[temv].set_brokenAtLife(4-self.__lives)
                                    if self._bricks[temv].get_subtype() == 2 and temv == retv-2:
                                        self._lasers[i].launch_powerup(self._bricks[temv], self._powerups,
                                                                       self._paddle.get_posX(), self._paddle.get_len(), val)

                    for i in range(len(self._lasers)):
                        if self._lasers[i].get_removed() == 1:
                            remLaserList.append(i)
                    for i in sorted(remLaserList, reverse=True):
                        del self._lasers[i]

                    remCompletedPowerupList = []
                    for i in range(len(self._powerups)):
                        if self._powerups[i].get_taken() == 1:
                            retv = self._powerups[i].incTime()
                            if retv == 1:  # if powerup of type 2 has been added then of type 1 will not be present (and vice versa)
                                self._paddle.unshrinkPaddle()
                                remCompletedPowerupList.append(i)
                            if retv == 2:
                                if len(self._balls) == 1:
                                    self._paddle.unexpandPaddle(self._balls[0].get_posX(), self._balls[0].get_grabbed())
                                else:
                                    self._paddle.unexpandPaddle(0, 0)  # 0,0 means ignore
                                remCompletedPowerupList.append(i)
                            if retv == 3:
                                remCompletedPowerupList.append(i)
                            if retv == 4:
                                self.__loops = 1
                                remCompletedPowerupList.append(i)
                            if retv == 5:
                                for ball in self._balls:
                                    ball.set_thru(0)
                                remCompletedPowerupList.append(i)
                            if retv == 6:
                                remCompletedPowerupList.append(i)
                                self._paddle.set_grabbed(0)
                                self._grabbedPowerup = 0
                            if retv == 7:
                                remCompletedPowerupList.append(i)
                                self._paddle.set_shoot(0)
                                self.__dispLaserTime = 0

                            if retv == 8:
                                remCompletedPowerupList.append(i)
                                for ball in self._balls:
                                    ball.set_fireball(0)
                            if retv == 0:
                                if self._powerups[i].get_powerupType() == 7:
                                    if self._paddle.get_afterLastShoot() == 10:
                                        # release laser create laser class
                                        leftLaserX = self._paddle.get_posX()
                                        rightLaserX = leftLaserX+self._paddle.get_len()-1
                                        self._lasers.append(Laser(leftLaserX, self._paddle.get_posY()-1, self._height-4,  int(1), int(2), self._width-3))
                                        self._lasers.append(Laser(rightLaserX, self._paddle.get_posY()-1, self._height-4,  int(1), int(2), self._width-3))
                                        os.system("aplay sounds/laser.wav -q &")
                                        self._paddle.set_afterLastShoot(0)
                                    else:
                                        self._paddle.set_afterLastShoot(self._paddle.get_afterLastShoot()+1)
                                    self.__dispLaserTime = self._powerups[i].get_timeLeftAfterTaken()

                    for i in sorted(remCompletedPowerupList, reverse=True):
                        del self._powerups[i]

                    remLostOrRepeatPowerupList = []  # lost or when already same is there before
                    for i in range(len(self._powerups)):
                        retv = self._powerups[i].movePowerup(self._paddle.get_posX(), self._paddle.get_len())  # 1 to 6 if we take a powerup
                        if retv == 1:  # new shrink paddle powerup (old will have retv as 0)
                            k = 0
                            for powerup in self._powerups:
                                if powerup._powerupType == self._powerups[i]._powerupType and powerup._timeDone > 0:
                                    extend_time = random.randint(70, 120)  # change it based on testing
                                    powerup.extendMaxTime(extend_time)
                                    remLostOrRepeatPowerupList.append(i)
                                    k = 1
                            if k == 0:
                                for m in range(len(self._powerups)):
                                    if self._powerups[m]._powerupType == 2 and self._powerups[m]._taken == 1:
                                        remLostOrRepeatPowerupList.append(m)
                                if len(self._balls) == 1:
                                    self._paddle.shrinkPaddle(self._balls[0].get_posX(), self._balls[0].get_grabbed())
                                else:
                                    self._paddle.shrinkPaddle(0, 0)  # 0,0 means ignore

                        if retv == 2:
                            k = 0
                            for powerup in self._powerups:
                                if powerup._powerupType == self._powerups[i]._powerupType and powerup._timeDone > 0:
                                    extend_time = random.randint(70, 120)  # change it based on testing
                                    powerup.extendMaxTime(extend_time)
                                    remLostOrRepeatPowerupList.append(i)
                                    k = 1
                            if k == 0:
                                for m in range(len(self._powerups)):
                                    if self._powerups[m]._powerupType == 1 and self._powerups[m]._taken == 1:
                                        remLostOrRepeatPowerupList.append(m)
                                self._paddle.expandPaddle()

                        if retv == 3:  # multiball
                            k = len(self._balls)
                            if k <= 4:
                                for ind in range(k):
                                    ranv = random.randint(70, 120)
                                    self._balls.append(Ball(self._balls[ind].get_posX(),
                                                            self._balls[ind].get_posY(), int(2), self._width-3, int(1), self._height-4, 0, ranv, 0))
                            self._powerups[i].ExecuteBallPowerup(self._balls)

                        if retv == 4:
                            k = 0
                            for powerup in self._powerups:
                                if powerup._powerupType == self._powerups[i]._powerupType and powerup._timeDone > 0:
                                    extend_time = random.randint(40, 60)  # change it based on testing
                                    powerup.extendMaxTime(extend_time)
                                    remLostOrRepeatPowerupList.append(i)
                                    k = 1
                            if k == 0:
                                self.FastBall()

                        if retv == 5:  # thru ball
                            k = 0
                            for powerup in self._powerups:
                                if powerup._powerupType == self._powerups[i]._powerupType and powerup._timeDone > 0:
                                    extend_time = random.randint(70, 120)  # change it based on testing
                                    powerup.extendMaxTime(extend_time)
                                    remLostOrRepeatPowerupList.append(i)
                                    k = 1
                            if k == 0:
                                self._powerups[i].ExecuteBallPowerup(self._balls)

                        if retv == 6:
                            k = 0
                            for powerup in self._powerups:
                                if powerup._powerupType == self._powerups[i]._powerupType and powerup._timeDone > 0:
                                    extend_time = random.randint(70, 120)  # change it based on testing
                                    powerup.extendMaxTime(extend_time)
                                    remLostOrRepeatPowerupList.append(i)
                                    k = 1
                            if k == 0:
                                self._paddle.set_grabbed(1)
                                self._grabbedPowerup = 1

                        if retv == 7:
                            k = 0
                            for powerup in self._powerups:
                                if powerup._powerupType == self._powerups[i]._powerupType and powerup._timeDone > 0:
                                    extend_time = random.randint(70, 120)  # change it based on testing
                                    powerup.extendMaxTime(extend_time)
                                    remLostOrRepeatPowerupList.append(i)
                                    k = 1
                            if k == 0:
                                self._paddle.shootLasers()

                        if retv == 8:
                            k = 0
                            for powerup in self._powerups:
                                if powerup._powerupType == self._powerups[i]._powerupType and powerup._timeDone > 0:
                                    extend_time = random.randint(70, 120)  # change it based on testing
                                    powerup.extendMaxTime(extend_time)
                                    remLostOrRepeatPowerupList.append(i)
                                    k = 1
                            if k == 0:
                                self._powerups[i].ExecuteBallPowerup(self._balls)

                        if retv == 10:
                            remLostOrRepeatPowerupList.append(i)

                    for i in sorted(remLostOrRepeatPowerupList, reverse=True):
                        del self._powerups[i]

                    remLostBombs = []
                    if self.__levelNum == 3:
                        for i in range(len(self._bombs)):
                            retv = self._bombs[i].moveBomb(self._paddle.get_posX(), self._paddle.get_len())
                            if retv == 1:
                                self.__lives -= 1
                                self.__prevStateTime = self.__time
                                self.__next = 1
                                break
                            if retv == 10:
                                remLostBombs.append(i)

                        for i in sorted(remLostBombs, reverse=True):
                            del self._bombs[i]

                        if self._enemy.get_afterLastThrow() == 16:
                            self._bombs.append(Bomb(self._enemy.get_posX()+17, self._enemy.get_posY()+8, self._height-4))
                            os.system("aplay sounds/dropBomb.wav -q &")
                            self._enemy.reset_afterLastThrow()
                        else:
                            self._enemy.set_afterLastThrow(1)

                    self._area.print_board(self._paddle, self._balls, self._bricks, self._powerups,
                                           self._lasers, self.__lives, self.__score, self.__time, self._enemy, self._bombs, self.__dispHealth, self.__dispLaserTime)

                prevTime = curTime
            if self.__healthZero == 1:
                break
            if self.__completed == 1:
                break
            if self.__next == 1:
                break
            if self._bricksTouchedDown == 1:
                break
            if self.__getInput.kbhit():
                input_char = self.__getInput.getch()

                if input_char == 'a':
                    k = self._paddle.left()
                    if self.__levelNum == 3:
                        rr = self._enemy.left(self._paddle.get_posX())
                    if k == 1:
                        for i in range(len(self._balls)):
                            if self._balls[i].get_grabbed() == 1:
                                self._balls[i].left()
                elif input_char == 'd':
                    k = self._paddle.right()
                    if self.__levelNum == 3:
                        rr = self._enemy.right(self._paddle.get_posX())
                    if k == 1:
                        for i in range(len(self._balls)):
                            if self._balls[i].get_grabbed() == 1:
                                self._balls[i].right()
                elif input_char == 'q':
                    self.__lives = 0
                    self.__quit = 1
                    break
                elif input_char == 'n':
                    self.__nextLevel = 1
                    self.__prevStateTime = self.__time
                    self.__prevLevelEndTime = self.__time
                    self.__totScorePrevLevels = self.__score
                    break

                elif input_char == ' ':
                    val = len(self._balls)
                    for i in range(len(self._balls)):
                        if self._balls[i].get_grabbed() == 1:
                            self._balls[i].start_move(self._paddle.get_posX(), self._paddle.get_len(), self._paddle.get_grabbed(),
                                                      self._bricks, self._powerups, val, (4-self.__lives), self.__time, self._enemy)

                self._area.print_board(self._paddle, self._balls, self._bricks, self._powerups,
                                       self._lasers, self.__lives, self.__score, self.__time, self._enemy, self._bombs, self.__dispHealth, self.__dispLaserTime)
                self.__getInput.flush()
