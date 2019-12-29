import pygame
import time
import random

pygame.init()

win = pygame.display.set_mode((608, 608))

pygame.display.set_caption("Bomberman")

GroundBlock = pygame.image.load("images/ground.png")
Wall = pygame.image.load("images/WALL.png")
BreakableWall = pygame.image.load("images/Breakable-Wall.png")
Bomberman1 = [pygame.image.load("images/bomber-down.png"), pygame.image.load("images/bomber-up.png"),
              pygame.image.load("images/bomber-right.png"), pygame.image.load("images/bomber-left.png")]
Bomb = pygame.image.load("images/bomb.png")
Explosion = pygame.image.load("images/explosion.png")
BonusDistanceUpgrade = pygame.image.load("images/distanceupgrade.png")

run = True
_BombDown = False
Exploding = False
Bricks_Printed = False
PassableRight = True
PassableLeft = True
PassableUp = True
PassableDown = True

BombRange = 3
BombAmmount = 0

initialX = 0
initialY = 0
_initialX = 0
_initialY = 0
velocity = 32
way = 0
posX = 32
posY = 32

clock = pygame.time.Clock()

Not_Allowed_Pos = [[64, 64],
[64, 128],
[64, 192],
[64, 256],
[64, 320],
[64, 384],
[64, 448],
[64, 512],
[128, 64],
[128, 128],
[128, 192],
[128, 256],
[128, 320],
[128, 384],
[128, 448],
[128, 512],
[192, 64],
[192, 128],
[192, 192],
[192, 256],
[192, 320],
[192, 384],
[192, 448],
[192, 512],
[256, 64],
[256, 128],
[256, 192],
[256, 256],
[256, 320],
[256, 384],
[256, 448],
[256, 512],
[320, 64],
[320, 128],
[320, 192],
[320, 256],
[320, 320],
[320, 384],
[320, 448],
[320, 512],
[384, 64],
[384, 128],
[384, 192],
[384, 256],
[384, 320],
[384, 384],
[384, 448],
[384, 512],
[448, 64],
[448, 128],
[448, 192],
[448, 256],
[448, 320],
[448, 384],
[448, 448],
[448, 512],
[512, 64],
[512, 128],
[512, 192],
[512, 256],
[512, 320],
[512, 384],
[512, 448],
[512, 512],
[0, 0],
[0, 576],
[32, 0],
[32, 576],
[64, 0],
[64, 576],
[96, 0],
[96, 576],
[128, 0],
[128, 576],
[160, 0],
[160, 576],
[192, 0],
[192, 576],
[224, 0],
[224, 576],
[256, 0],
[256, 576],
[288, 0],
[288, 576],
[320, 0],
[320, 576],
[352, 0],
[352, 576],
[384, 0],
[384, 576],
[416, 0],
[416, 576],
[448, 0],
[448, 576],
[480, 0],
[480, 576],
[512, 0],
[512, 576],
[544, 0],
[544, 576],
[576, 0],
[576 ,576],
[0, 0],
[576, 0],
[0, 32],
[576, 32],
[0, 64],
[576, 64],
[0, 96],
[576, 96],
[0, 128],
[576, 128],
[0, 160],
[576, 160],
[0, 192],
[576, 192],
[0, 224],
[576, 224],
[0, 256],
[576, 256],
[0, 288],
[576, 288],
[0, 320],
[576, 320],
[0, 352],
[576, 352],
[0, 384],
[576, 384],
[0, 416],
[576, 416],
[0, 448],
[576, 448],
[0, 480],
[576, 480],
[0, 512],
[576, 512],
[0, 544],
[576, 544],
[0, 576],
[576, 576]]
Not_Allowed_Walls =[
[0, 0],
[0, 576],
[32, 0],
[32, 576],
[64, 0],
[64, 32],
[64, 576],
[96, 0],
[96, 576],
[128, 0],
[128, 576],
[160, 0],
[160, 576],
[192, 0],
[192, 576],
[224, 0],
[224, 576],
[256, 0],
[256, 576],
[288, 0],
[288, 576],
[320, 0],
[320, 576],
[352, 0],
[352, 576],
[384, 0],
[384, 576],
[416, 0],
[416, 576],
[448, 0],
[448, 576],
[480, 0],
[480, 576],
[512, 0],
[512, 576],
[544, 0],
[544, 576],
[576, 0],
[576, 576],
[0, 0],
[576, 0],
[0, 32],
[576, 32],
[0, 64],
[576, 64],
[0, 96],
[576, 96],
[0, 128],
[576, 128],
[0, 160],
[576, 160],
[0, 192],
[576, 192],
[0, 224],
[576, 224],
[0, 256],
[576, 256],
[0, 288],
[576, 288],
[0, 320],
[576, 320],
[0, 352],
[576, 352],
[0, 384],
[576, 384],
[0, 416],
[576, 416],
[0, 448],
[576, 448],
[0, 480],
[576, 480],
[0, 512],
[576, 512],
[0, 544],
[576, 544],
[0, 576],
[576, 576],
[32, 32],
[32, 64],
[64, 64],
[512,544],
[544, 544],
[541, 512],
[512, 512],
[544, 512],
[64,64],
[64, 128],
[64, 192],
[64, 256],
[64, 320],
[64, 384],
[64, 448],
[64, 512],
[128, 64],
[128, 128],
[128, 192],
[128, 256],
[128, 320],
[128, 384],
[128, 448],
[128, 512],
[192, 64],
[192, 128],
[192, 192],
[192, 256],
[192, 320],
[192, 384],
[192, 448],
[192, 512],
[256, 64],
[256, 128],
[256, 192],
[256, 256],
[256, 320],
[256, 384],
[256, 448],
[256, 512],
[320, 64],
[320, 128],
[320, 192],
[320, 256],
[320, 320],
[320, 384],
[320, 448],
[320, 512],
[384, 64],
[384, 128],
[384, 192],
[384, 256],
[384, 320],
[384, 384],
[384, 448],
[384, 512],
[448, 64],
[448, 128],
[448, 192],
[448, 256],
[448, 320],
[448, 384],
[448, 448],
[448, 512],
[512, 64],
[512, 128],
[512, 192],
[512, 256],
[512, 320],
[512, 384],
[512, 448],
[512, 512]]
BrickWallList = []
BonusList = []

def Bomber():
    CreateBackground()
    win.blit(Bomberman1[way], (posX, posY))


def CreateBackground():
    global Bricks_Printed
    for initialX in range(0, 608, 32):
        for initialY in range(0, 608, 32):
            win.blit(GroundBlock, (initialX, initialY))

    for borderpos in range(0, 608, 32):
        for edgepos in [0, 576]:
            win.blit(Wall, (borderpos, edgepos))
            win.blit(Wall, (edgepos, borderpos))

    for break1 in range(64, 576, 64):
        for break2 in range(64, 576, 64):
                win.blit(Wall, (break1, break2))

    if Bricks_Printed == False:
        for brickwall in range(0, 608, 32):
            for brickwall1 in range(0, 608, 32):
                if not [brickwall, brickwall1] in Not_Allowed_Walls:
                    if random.randint(0, 1) == 1:
                        BrickWallList.append([brickwall, brickwall1])

    Bricks_Printed = True

    for x in BonusList:
        win.blit(BonusDistanceUpgrade, x)

    for brickwalll in BrickWallList:
        win.blit(BreakableWall, brickwalll)



def BombDown():
    global bombtime, _BombDown, BombAmmount, ExplosionTime, Exploding
    if _BombDown == True:
        if bombtimer + 3000 > Time1:
            win.blit(Bomb, (BombPosX, BombPosY))
        else:
            Exploding = True
            _BombDown = False
            BombAmmount -= 1
            ExplosionTime = Time1
            Explode()

def Explode():
    global ExplosionTime, Exploding, PassableUp, PassableDown, PassableLeft, PassableRight, i

    if ExplosionTime + 3000 > Time1 and Exploding == True:
        for distance in range(0, BombRange, 1):
            if not [BombPosX+32*distance, BombPosY] in Not_Allowed_Pos and PassableRight == True:
                for row in BrickWallList.copy():
                    if row == [BombPosX+32*distance, BombPosY]:
                        BrickWallList.remove(row)
                        PassableRight = False
                        if random.randint(0, 2) == 1:
                            BonusList.append(row)
                win.blit(Explosion, (BombPosX +32*distance, BombPosY))
            else:
                PassableRight = False

            if not [BombPosX-32*distance, BombPosY] in Not_Allowed_Pos and PassableLeft == True:
                for row in BrickWallList.copy():
                    if row == [BombPosX-32*distance, BombPosY]:
                        BrickWallList.remove(row)
                        PassableLeft = False
                        if random.randint(0, 2) == 1:
                            BonusList.append(row)
                win.blit(Explosion, (BombPosX-32*distance, BombPosY))
            else:
                PassableLeft = False

            if not [BombPosX, BombPosY-32*distance] in Not_Allowed_Pos and PassableDown == True:
                for row in BrickWallList.copy():
                    if row == [BombPosX, BombPosY-32*distance]:
                        BrickWallList.remove(row)
                        PassableDown = False
                        if random.randint(0, 2) == 1:
                            BonusList.append(row)
                win.blit(Explosion, (BombPosX, BombPosY-32*distance))
            else:
                PassableDown = False

            if not [BombPosX, BombPosY+32*distance] in Not_Allowed_Pos and PassableUp == True:
                for row in BrickWallList.copy():
                    if row == [BombPosX, BombPosY+32*distance]:
                        BrickWallList.remove(row)
                        PassableUp = False
                        if random.randint(0, 2) == 1:
                            BonusList.append(row)
                win.blit(Explosion, (BombPosX, BombPosY+32*distance))
            else:
                PassableUp = False

    else:
        ExplosionTime = Time1
        Exploding = False
        PassableUp= True
        PassableDown= True
        PassableRight = True
        PassableLeft = True

Time1 = pygame.time.get_ticks()
ExplosionTime = Time1

while run:
    clock.tick(30)
    Time1 = pygame.time.get_ticks()
    bombpos = posX, posY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                way = 3
                if not [posX - 32, posY] in Not_Allowed_Pos:
                    if not [posX - 32, posY] in BrickWallList:
                        posX -= 32
                        print(posX, posY)
                        if [posX, posY] in BonusList:
                            BombRange += 1
                            BonusList.remove([posX, posY])

            if event.key == pygame.K_RIGHT:
                way = 2
                if not [posX + 32, posY] in Not_Allowed_Pos:
                    if not [posX + 32, posY] in BrickWallList:
                        posX += 32
                        print(posX, posY)
                        if [posX, posY] in BonusList:
                            BombRange += 1
                            BonusList.remove([posX, posY])

            if event.key == pygame.K_UP:
                way = 1
                if not [posX, posY - 32] in Not_Allowed_Pos:
                    if not [posX, posY-32] in BrickWallList:
                        posY -= 32
                        print(posX, posY)
                        if [posX, posY] in BonusList:
                            BombRange += 1
                            BonusList.remove([posX, posY])
            if event.key == pygame.K_DOWN:
                way = 0
                if not [posX, posY + 32] in Not_Allowed_Pos:
                    if not [posX, posY+32] in BrickWallList:
                        posY += 32
                        print(posX, posY)
                        if [posX, posY] in BonusList:
                            BombRange += 1
                            BonusList.remove([posX, posY])

            if event.key == pygame.K_k:
                if _BombDown == False and BombAmmount == 0 and Exploding == False:
                    BombPosX, BombPosY = posX, posY
                    _BombDown = True
                    bombtimer = Time1
                    BombAmmount += 1

    CreateBackground()
    Bomber()
    BombDown()
    Explode()
    pygame.display.update()

pygame.quit()