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

way = 0
posX = 32
posY = 32

clock = pygame.time.Clock()

Not_Allowed_Pos = []
Not_Allowed_Walls = [[32, 32], [64, 32], [32, 64]]
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
            Not_Allowed_Pos.append([borderpos, edgepos])
            Not_Allowed_Pos.append([edgepos, borderpos])
            Not_Allowed_Walls.append([borderpos, edgepos])
            Not_Allowed_Walls.append([edgepos, borderpos])
            win.blit(Wall, (borderpos, edgepos))
            win.blit(Wall, (edgepos, borderpos))

    for break1 in range(64, 576, 64):
        for break2 in range(64, 576, 64):
                Not_Allowed_Pos.append([break1, break2])
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
    global ExplosionTime, Exploding, PassableUp, PassableDown, PassableLeft, PassableRight

    if ExplosionTime + 2000 > Time1 and Exploding == True:
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