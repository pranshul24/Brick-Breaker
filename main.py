import os
import numpy as np
from colorama import init as coloramaInit

from game import Game

coloramaInit()
os.system('clear')  # clear screen
game = Game()
game.playBrickBreaker()
