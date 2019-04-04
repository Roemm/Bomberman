![alt text](https://github.abudhabi.nyu.edu/yc2548/ICS_Bomberman/blob/master/screenshot.png)

# Bomberman

Yiqi Chang, Ying Wang

Fall 2018, Intro to Computer Science

## How to Play

The player's goal is to get out by clearing the bricks while not being killed by the ballon monsters.

- Walk around using UP, DOWN, LEFT, RIGHT key
- Explode yourlself using SPACE

Have fun!

## Documentation

### The Block Class: Making the Arena
We used the block class to create two types of block: 

- Concretes: can't be destroyed is formed with a pattern

- Bricks: can be destroyed by explosion of the bomb and is randomly generated

### The Creature Class: The Player and the Enemies
One challenege we ran into is how to let the player and enemies become aware of the blocks and turn around or stop moving. We converted the x,y coordinates to r,c coordinates so we can detect if there is a block on the moving direction. Only move when it is clear.

### The Bomb Class
Everytime the bomb is triggered, it checks neighbours and remove any block that can be destroyed. We were able to create the explosion effect by displaying two images one after another using time.time() inside the bomb class. However, we have difficulties to delay the removal of the bricks. To synchrinize, we ended up making the explosion very immediate so now it is a real bomber man.
