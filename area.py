import os
import numpy as np
from colorama import Fore, Back, Style
import random
import time
from paddle import Paddle
from Ball import Ball

# -> columns
# |
# V
# rows


class Area:

    cursorStart = "\033[0;0H"

    def __init__(self, height, width):
        self._height = height
        self._width = width

        self._gameArea = np.array(
            [[' ' for j in range(self._width)] for i in range(self._height)], dtype='object')

        for i in range(0, self._height):
            for j in range(0, self._width):
                self._gameArea[i][j] = Back.BLACK+' '

        for i in range(0, self._width):
            self._gameArea[0][i] = Back.GREEN + Fore.MAGENTA + Style.DIM + '='
            self._gameArea[self._height -
                           1][i] = Back.LIGHTYELLOW_EX + Fore.BLUE + '='
        for i in range(1, self._height-1):
            self._gameArea[i][0] = Back.GREEN + Fore.MAGENTA + '['
            self._gameArea[i][1] = Back.GREEN + Fore.MAGENTA + ']'
            self._gameArea[i][self._width -
                              1] = Back.GREEN + Fore.MAGENTA + ']'
            self._gameArea[i][self._width-2] = Back.GREEN + Fore.MAGENTA+'['

    def print_lifeLost(self, color):
        for i in range(1, self._height-1):
            for j in range(2, self._width-2):
                if color == 1:
                    self._gameArea[i][j] = Back.BLUE+' '

                else:
                    self._gameArea[i][j] = Back.RED+' '
        string = self.cursorStart
        for i in range(self._height):
            for j in range(self._width):
                string += self._gameArea[i][j]
            string += "\n"
        print(string, end='')

    def healthBar(self, left):
        total = 100
        length = 10
        if left >= total:
            return Back.RED + (' ' * length)
        if left <= 0:
            return Back.GREEN + (' ' * length)
        perc = int(round((left / total) * length))
        s = Back.RED + (' ' * perc)
        s += Back.GREEN + (' ' * (length - perc))

        return s

    def print_board(self, paddle, balls, bricks, powerups, lasers, lives, score, time, enemy, bombs, health, laserTime):
        for i in range(1, self._height-1):
            for j in range(2, self._width-2):
                self._gameArea[i][j] = Back.BLACK+' '

        if enemy != 0:
            enemy.disp_enemy(self)
        for brick in bricks:
            if brick.get_posY() <= self._height-5:
                brick.disp_brick(self)
        for ball in balls:
            ball.disp_ball(self)
        for powerup in powerups:
            powerup.disp_powerup(self)

        for laser in lasers:
            laser.disp_laser(self)

        for bombs in bombs:
            bombs.disp_bomb(self)
        paddle.disp_paddle(self)

        string = self.cursorStart
        for i in range(self._height):
            for j in range(self._width):
                string += self._gameArea[i][j]
            string += "\n"
        print(string, end='')
        print(Style.RESET_ALL, end='')
        string2 = "    Lives Left : "
        string2 += str(lives) + "      Score : " + str(score) + "      Time : " + str(time) + "   "
        if laserTime > 0:
            string2 += "  Laser time remaining : "
            string2 += str(int(laserTime/10))

        if health > 0:
            string2 += "   Health : "
            string2 += self.healthBar(health)
            string2 += Style.RESET_ALL
            # string2 += '\t'

        if len(string2) < self._width:
            for val in range(self._width-len(string2)):
                string2 += " "

        print(string2)
