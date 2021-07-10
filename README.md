# Brick Breaker Game

### Pranshul Chawla
### 2019101057
---

## Introduction
This is a terminal based arcade game written in Python 3 inspired from
the old classic brick breaker . The player will be using a paddle with a bouncing ball to smash 
bricks and make high scores! The objective of the game is to break all the bricks as fast as possible and
beat the highest score! You lose a life when the ball touches the ground below the paddle. Several powerups may appear randomly
on breaking a brick .

## Requirements
```
colorama
numpy
```

## Install mentioned requirements
```
$ pip3 install -r requirements.txt
```

## Running
```
$ python3 main.py
```


## Rules

- Score is based on lives remaining and time as well but higher priority is given to lives remaining . So better save your lives and then try to break bricks as fast as possible .

- Bricks are of three types exploding , breakable and unbreakable bricks . Try breaking maximum bricks . Each brick yields same points . Exploding bricks show chain reaction and break all surrounding bricks .

- Powerups deactivate after certain time .



## Quick Game Guide :

- **a** : move left
- **d** : move right
- **space** : release ball grabbed on paddle
- **q**: quit game
- **n**: switch to next level

## OOPS concepts used :

1. **Polymorphism** - Both powerups *Thru ball* and *Paddle grab* have `ExecuteBallPowerup` method showing different functionality (have been overriden in the child classes for each powerup). Similarly `disp_brick` and `disp_powerup` represent polymorphism .
2. **Inheritance** - `BreakableBrick`,`UnbreakableBrick` and `ExplodingBrick` classes inherit the methods and attributes of `Brick` class .
3. **Encapsulation** - game has been encapsulated by using classes and object approach . Along with this most attributes are private and protected type to further encapsulate to higher degree .
4. **Abstraction** - methods like `moveBall` ,`shrinkPaddle` ,`check_paddle_collision` hide the inner details and implementation from the end user .
