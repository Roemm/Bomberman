# walls 6*4, surrounding: 15*11, 960*704


import time
import os
import random
path = os.getcwd()
neighbours = [[0,-1],[-1,0],[1,0],[0,1]]

# needed if we need to add sound
add_library('minim')
player = Minim(this)


class Creature:

    def __init__(self, x, y, r, imgFolder, w, h, F):
        self.x = x
        self.y = y
        self.r = r
        self.w = w
        self.h = h
        self.f = 0
        self.F = F
        self.vx = 0
        self.vy = 0
        self.dir = "up"  # the default direction would be facing up
        self.imgL = loadImage(
            path + "/assets/images/" + imgFolder + "/left.png")
        self.imgR = loadImage(
            path + "/assets/images/" + imgFolder + "/right.png")

    def update(self):

        self.x += self.vx
        self.y += self.vy

    def display(self):
        self.update()

        # add up and down display only for bomberman
        if isinstance(self, Man):
            if self.dir == "up":
                image(self.imgU, self.x - self.w // 2, self.y - self.h // 2, self.w,
                      self.h, int(self.f) * self.w, 0, (int(self.f) + 1) * self.w, self.h)
            elif self.dir == "down":
                image(self.imgD, self.x - self.w // 2, self.y - self.h // 2, self.w,
                      self.h, int(self.f) * self.w, 0, (int(self.f) + 1) * self.w, self.h)

        # left right display
        if self.dir == "right":
            image(self.imgR, self.x - self.w // 2, self.y - self.h // 2, self.w,
                  self.h, int(self.f) * self.w, 0, (int(self.f) + 1) * self.w, self.h)

        elif self.dir == "left":
            image(self.imgL, self.x - self.w // 2, self.y - self.h // 2, self.w,
                  self.h, int(self.f) * self.w, 0, (int(self.f) + 1) * self.w, self.h)

        if self.vx != 0 or self.vy != 0:
            self.f = (self.f + 0.2) % self.F
            
        #draw circles around creature for debugging
        # stroke(0)
        # strokeWeight(3)
        # noFill()
        # ellipse(self.x, self.y, self.w, self.h)

    #translate the coordinate into grid(r,c)
    def getPos(self, dir):
        
        #depending on  its direction, the corresponding points need to be changed
        self.dir = dir
        if self.dir == "up":
            pos = [(self.y + 28) // 64, (self.x - 28) // 64]
        elif self.dir == "right":
            pos = [(self.y - 28) // 64, (self.x - 28) // 64]
        elif self.dir == "down":
            pos = [(self.y - 28) // 64, (self.x - 28) // 64]
        elif self.dir == "left":
            pos = [(self.y - 28) // 64, (self.x + 28) // 64]

        return pos
    
    
    #check whether the creature can move or not
    def boundary(self, dir):
        self.dir = dir

        if dir == "up":
            self.r = self.getPos(dir)[0]
            self.c = self.getPos(dir)[1]
            self.b = g.getBlock(self.r - 1, self.c)
            print(self.r, self.c)
            return self.b
        elif dir == "right":
            self.r = self.getPos(dir)[0]
            self.c = self.getPos(dir)[1]
            self.b = g.getBlock(self.r, self.c + 1)
            print(self.r, self.c)
            return self.b

        elif dir == "down":
            self.r = self.getPos(dir)[0]
            self.c = self.getPos(dir)[1]
            self.b = g.getBlock(self.r + 1, self.c)
            print(self.r, self.c)
            return self.b
        elif dir == "left":
            self.r = self.getPos(dir)[0]
            self.c = self.getPos(dir)[1]
            self.b = g.getBlock(self.r, self.c - 1)
            print(self.r, self.c)
            return self.b


class Man(Creature):

    def __init__(self, x, y, r, imgFolder, w, h, F):
        Creature.__init__(self, x, y, r, imgFolder, w, h, F)
        self.keyHandler = {LEFT: False, RIGHT: False, UP: False, DOWN: False}
        self.imgU = loadImage(path + "/assets/images/" + imgFolder + "/up.png")
        self.imgD = loadImage(
            path + "/assets/images/" + imgFolder + "/down.png")
        

    def update(self):

        #check whether there are boundaries
        #if self.boundary == None, it means that it's free for the creature to move
        
        
        # moving upwards
        if self.keyHandler[UP]:
            # self.vy = -1
            self.dir = "up"
            if self.boundary(self.dir) == None:
                self.vy = -1
            else:
                self.vx = 0
                self.vy = 0
                
        # moving to the right
        elif self.keyHandler[RIGHT]:
            # self.vx = 1
            self.dir = "right"
            if self.boundary(self.dir) == None:
                self.vx = 1
            else:
                self.vx = 0
                self.vy = 0

        # moving downwards
        elif self.keyHandler[DOWN]:
            # self.vy = 1
            self.dir = "down"
            if self.boundary(self.dir) == None:
                self.vy = 1
            else:
                self.vx = 0
                self.vy = 0

        # moving to the left
        elif self.keyHandler[LEFT]:
            # self.vx = -1
            self.dir = "left"
            if self.boundary(self.dir) == None:
                self.vx = -1
            else:
                self.vx = 0
                self.vy = 0

        else:
            self.vx = 0
            self.vy = 0

        self.x += self.vx
        self.y += self.vy
        
        #detect the distance between bomberman and monsters to see whether the game loses
        for e in g.enemies:
            if self.distance(e) <= 50:
                g.gameOver.play()
                g.music.pause()
                
                time.sleep(5)
                g.music.rewind()
                
                g.__init__(960, 704)

        
    def distance(self, e):
        return ((self.x - e.x) ** 2 + (self.y - e.y) ** 2) ** 0.5


class Monster(Creature):

    def __init__(self, x, y, r, imgFolder, w, h, F, x1, x2):
        Creature.__init__(self, x, y, r, imgFolder, w, h, F)
        self.x1 = x1
        self.x2 = x2
        self.vx = random.randint(2, 4)
        self.dir = random.choice(["left", "right"])
    
    #the creature moves automatically and bouncing between boundaries
    def update(self):

        if self.dir == "left":
            if self.boundary(self.dir) == None:
                self.vx = -1
            else:                
                self.dir = "right"
                self.vx *= -1

        elif self.dir == "right":
            if self.boundary(self.dir) == None:
                self.vx = 1
            else:
                self.dir = "left"
                self.vx *= -1
                
        else:
            self.vx = 0

        self.x += self.vx
        self.y += self.vy
        


    def boundary(self, dir):
        self.dir = dir
                  
        if self.dir == "right":
            self.r = self.getPos(self.dir)[0]
            self.c = self.getPos(self.dir)[1]
            self.b = g.getBlock(self.r, self.c + 1)
            
            return self.b

        elif dir == "left":
            self.r = self.getPos(self.dir)[0]
            self.c = self.getPos(self.dir)[1]
            self.b = g.getBlock(self.r, self.c - 1)
            
            return self.b


class Block:

    def __init__(self, r, c, w):
        self.r = r
        self.c = c
        self.w = w
        self.concrete = loadImage(path + "/assets/images/concrete.png")
        self.destroyed = False    # whether it is static or can be destroyed
        self.brick = loadImage(path + "/assets/images/brick.png")
        self.filled = False

    def display(self):

        if (self.destroyed == True):
            image(self.brick, self.c * self.w, self.r * self.w, self.w, self.w)
        else:
            image(self.concrete, self.c * self.w,
                  self.r * self.w, self.w, self.w)

class Bomb(Block):
    def __init__(self,r,c,w):
        Block.__init__(self,r,c,w)
        self.bomb1 = loadImage(path + "/assets/images/bomb.png")
        self.bomb2 = loadImage(path + "/assets/images/explosion.png")
        self.time = 400
        self.start = time.time()
        self.explode = False
    
    #explode after 3 seconds        
    def display(self):
        if (time.time() < self.start + 0.1):
            image(self.bomb1, self.c*self.w, self.r*self.w, self.w, self.w)   
        elif (time.time() > self.start + 0.1) and (time.time() < self.start + 0.2):
            self.explode = True
            g.bombSound.play()
            image(self.bomb2, self.c*self.w-96, self.r*self.w-96, self.w*4, self.w*4)
            g.bombSound.rewind()


class Game:

    def __init__(self, w, h):
        self.x = 0
        self.w = w
        self.h = h
        self.weight = 64
        self.numBrick = 20
        self.numEnemy = 6
        self.brickX = 0
        self.brickY = 0
        self.music = player.loadFile(path + "/assets/sounds/08-Witchs_Hut.wav")
        self.gameOver = player.loadFile(path + "/assets/sounds/gameOver.wav")
        self.music.loop()
        self.winSound = player.loadFile(path + "/assets/sounds/win.wav")
        self.bombSound = player.loadFile(path + "/assets/sounds/explosion1.wav")
        # Making the arena
        self.blocks = []
        self.isWin = False

        # First and large row
        for c in range(15):
            self.block1 = Block(0, c, 64)
            self.blocks.append(self.block1)
            self.block2 = Block(10, c, 64)
            self.blocks.append(self.block2)
        
        self.blocks.pop(24)

        # Middle rows
        for r in range(1, 10):
            if r % 2 == 1:
                self.blocks.append(Block(r, 0, 64))
                self.blocks.append(Block(r, 14, 64))
            else:
                for c in range(15):
                    if c % 2 == 0:
                        self.blocks.append(Block(r, c, 64))

        # Randomly generate the brick
        i = 0
        while i < self.numBrick:
            self.br = random.randint(1, 9)
            self.bc = random.randint(1, 13)
            self.b = self.getBlock(self.br, self.bc)
            if not ((self.bc == 1 and self.br == 8) or (self.bc == 1 and self.br == 9) or (self.bc == 2 and self.br == 9)):
                if self.b == None:
                    i += 1
                    self.block = Block(self.br, self.bc, 64)
                    self.block.destroyed = True
                    self.blocks.append(self.block)
                    # print(self.br,self.bc)

        #Create bomberman
        self.man = Man(
            self.weight + 32, self.h - self.weight - 32, 64, "man", 64, 64, 3)
        
        #Randomly generated enemies
        j = 0
        self.enemies = []
        while j < self.numEnemy:
            self.er = random.randint(1, 9)
            self.ec = random.randint(1, 13)
            self.b = self.getBlock(self.er, self.ec)
            if not ((self.ec == 1 and self.er == 8) or (self.ec == 1 and self.er == 9) or (self.ec == 2 and self.er == 9) or (self.er%2 == 0)):
                if self.b == None:
                    j += 1
                    self.enemies.append(Monster(
                        self.ec * 64, self.er * 64 + 32, 64, "enemy", 64, 64, 1, self.weight + 32, self.w - self.weight - 32))

    def getBlock(self, r, c):
        for b in self.blocks:
            if b.r == r and b.c == c:
                return b
    
    #is called when space bar is pressed
    bombs = []
    def placeBomb(self,r,c):
        self.b = Bomb(r,c,64)
        self.bombs.append(self.b)
        self.checkNeighbours(self.b)
        
    #remove the bricks around the bomb
    def checkNeighbours(self,b):
        for n in neighbours:
            br = b.r+n[0]
            bc = b.c+n[1]
            nb = self.getBlock(br,bc)
            if nb!= None:
                #If tile doesn't contain a mine or a number, keep sweeping around
                if nb.destroyed == True:
                        self.blocks.remove(nb)

    def display(self):
        self.man.display()

        for block in self.blocks:
            block.display()
        
        for bomb in self.bombs:
            bomb.display()


        for enemy in self.enemies:
            enemy.display()
            
    def win(self):
        if self.man.getPos(self.man.dir) == [1,12]:
            self.isWin = True
            g.winSound.play()
            g.music.pause()
            
            
            time.sleep(5)
            g.music.rewind()
            g.__init__(960,704)
    

g = Game(960, 704)

def setup():
    size(g.w, g.h)

def draw():
    background(34, 119, 0)
    g.display()
    g.win()


# control the object movement
def keyPressed():
    if keyCode == LEFT:
        g.man.keyHandler[LEFT] = True
    elif keyCode == RIGHT:
        g.man.keyHandler[RIGHT] = True
    elif keyCode == UP:
        g.man.keyHandler[UP] = True
    elif keyCode == DOWN:
        g.man.keyHandler[DOWN] = True
    
    if key == " ":
        n = g.man.getPos(g.man.dir)
        print(n)
        g.placeBomb(n[0],n[1])
        
def keyReleased():
    if keyCode == LEFT:
        g.man.keyHandler[LEFT] = False
    elif keyCode == RIGHT:
        g.man.keyHandler[RIGHT] = False
    elif keyCode == UP:
        g.man.keyHandler[UP] = False
    elif keyCode == DOWN:
        g.man.keyHandler[DOWN] = False
