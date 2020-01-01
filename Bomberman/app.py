import pygame
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
Logo = pygame.image.load("images/IntroLogo.png")
StartButton = pygame.image.load("images/startbutton1.png")
QuitButton = pygame.image.load("images/quit1.png")
Selector = pygame.image.load("images/selectoricon.png")
BallonImage = [pygame.image.load("images/ballonleft.png"), pygame.image.load("images/ballonright.png")]

Icon = pygame.image.load("images/icon.png")
music = pygame.mixer.music.load("sounds/Intro.mp3")
BombSound = pygame.mixer.Sound("sounds/bomb-sound.wav")
UpgradeSound = pygame.mixer.Sound("sounds/upgrade.wav")
ChooseSound = pygame.mixer.Sound("sounds/choose.wav")

pygame.display.set_icon(Icon)

run = True
_BombDown = False
Exploding = False

Bricks_Generated = False
BorderGenerated = False
HardWallsGenerated = False
ExplodedSound = False
BallonPosGenerated = False

intro = True
PassableRight = True
PassableLeft = True
PassableUp = True
PassableDown = True
BallonDead= False


black = 0, 0, 0
BombRange = 2
BombAmmount = 0
ExplosionDuration = 1000  # miliseconds
BombDuration = 3000  # miliseconds

SelectorPosition = 0

way = 0
ballonway = 0
velocity = 32
posX = 32
posY = 32
BallonTime = 0
clock = pygame.time.Clock()

Time1 = pygame.time.get_ticks()

Not_Allowed_Pos = []
Not_Allowed_Walls = [[32, 32], [64, 32], [32, 64]]
BrickWallList = []
BonusList = []
BorderPos = []
HardWalls = []
ExplosionPos = []
BombPos = []


BallonTime = 0


def fade(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        win.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(5)


def GameIntro():
    global SelectorPosition, intro

    while intro:
        win.fill(black)
        win.blit(Logo, (153, 50))
        win.blit(StartButton, (260, 300))
        win.blit(QuitButton, (270, 350))
        if SelectorPosition == 0:
            win.blit(Selector, (230, 305))
        elif SelectorPosition == 1:
            win.blit(Selector, (230, 355))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if not SelectorPosition == 0:
                        SelectorPosition -= 1
                if event.key == pygame.K_DOWN:
                    if not SelectorPosition == 1:
                        SelectorPosition += 1
                if event.key == pygame.K_RETURN:
                    if SelectorPosition == 1:
                        pygame.mixer.music.stop()
                        ChooseSound.play()
                        quit()
                    elif SelectorPosition == 0:
                        pygame.mixer.music.stop()
                        ChooseSound.play()
                        intro = False
                        fade(608, 608)

        pygame.display.update()


def Bomber():
    win.blit(Bomberman1[way], (posX, posY))


def CreateBackground():
    global Bricks_Generated, BorderGenerated, HardWallsGenerated
    for initialX in range(0, 608, 32):
        for initialY in range(0, 608, 32):
            win.blit(GroundBlock, (initialX, initialY))

    if BorderGenerated == False:
        for borderpos in range(0, 608, 32):
            for edgepos in [0, 576]:
                Not_Allowed_Pos.append([borderpos, edgepos])
                Not_Allowed_Pos.append([edgepos, borderpos])
                Not_Allowed_Walls.append([borderpos, edgepos])
                Not_Allowed_Walls.append([edgepos, borderpos])
                BorderPos.append([edgepos, borderpos])
                BorderPos.append([borderpos, edgepos])

    if HardWallsGenerated == False:
        for HardWalli in range(64, 576, 64):
            for HardWallj in range(64, 576, 64):
                HardWalls.append([HardWalli, HardWallj])
                Not_Allowed_Pos.append([HardWalli, HardWallj])

    if Bricks_Generated == False:
        for brickwall in range(0, 608, 32):
            for brickwall1 in range(0, 608, 32):
                if not [brickwall, brickwall1] in Not_Allowed_Walls:
                    if random.randint(0, 1) == 1:
                        BrickWallList.append([brickwall, brickwall1])

    Bricks_Generated = True
    BorderGenerated = True
    HardWallsGenerated = True

    for x in BonusList:
        win.blit(BonusDistanceUpgrade, x)

    for Border in BorderPos:
        win.blit(Wall, Border)

    for brickwalll in BrickWallList:
        win.blit(BreakableWall, brickwalll)

    for HardWall in HardWalls:
        win.blit(Wall, HardWall)


def BombDown():
    global bombtime, _BombDown, BombAmmount, ExplosionTime, Exploding
    if _BombDown == True:
        if bombtimer + BombDuration > Time1:
            BombPos.append([BombPosX, BombPosY])
            win.blit(Bomb, (BombPosX, BombPosY))
        else:
            Exploding = True
            _BombDown = False
            BombAmmount -= 1
            ExplosionTime = Time1
            Explode()


def BallonEnemy():
    global BallonPosGenerated, BallonPosX, BallonPosY, ballonway, BallonTime, BallonPos
    if BallonPosGenerated == False:
        BallonPosX = random.randrange(0, 608, 32)
        BallonPosY = random.randrange(0, 608, 32)
        BallonPos = [BallonPosX, BallonPosY]

        for BalPos in Not_Allowed_Pos:
            if not BalPos in BallonPos:
                if not BalPos in BorderPos:
                    BallonPosGenerated = True

    if BallonPosGenerated == True and BallonTime + 2000 < Time1 and BallonDead == False:
        direction = random.randint(0, 3)
        if direction == 1:
            if not [BallonPosX + velocity, BallonPosY] in HardWalls:
                if not [BallonPosX + velocity, BallonPosY] in BorderPos:
                    ballonway = 1
                    BallonPosX += velocity
                    BallonTime = Time1

        elif direction == 0:
            if not [BallonPosX - velocity, BallonPosY] in HardWalls:
                if not [BallonPosX - velocity, BallonPosY] in BorderPos:
                    ballonway = 0
                    BallonPosX -= velocity
                    BallonTime = Time1
        elif direction == 2:
            if not [BallonPosX, BallonPosY + velocity] in HardWalls:
                if not [BallonPosX, BallonPosY + velocity] in BorderPos:
                    BallonPosY += velocity
                    BallonTime = Time1
        elif direction == 3:
            if not [BallonPosX, BallonPosY - velocity] in HardWalls:
                if not [BallonPosX, BallonPosY - velocity] in BorderPos:
                    BallonPosY -= velocity
                    BallonTime = Time1

    if BallonDead == False:
        win.blit(BallonImage[ballonway], [BallonPosX, BallonPosY])

    if BallonPos == [posX, posY]:
        quit()


def Explode():
    global ExplosionTime, Exploding, PassableUp, PassableDown, PassableLeft, PassableRight, ExplodedSound, BallonPosX, BallPosY, BallonDead
    if Exploding == True:
        BombPos.clear()
        for distance in range(0, BombRange, 1):
            if not [BombPosX + velocity * distance, BombPosY] in Not_Allowed_Pos and PassableRight:
                for row in BrickWallList.copy():
                    if row == [BombPosX + velocity * distance, BombPosY]:
                        BrickWallList.remove(row)
                        PassableRight = False
                        if random.randint(0, 2) == 1:
                            BonusList.append(row)

                if not [BombPosX + velocity * distance, BombPosY] in BonusList:
                    ExplosionPos.append([BombPosX + velocity * distance, BombPosY])

                if [BombPosX + velocity * distance, BombPosY] == [BallonPosX, BallonPosY]:
                    PassableRight = False
                    BallonDead = True

            else:
                PassableRight = False

            if not [BombPosX - velocity * distance, BombPosY] in Not_Allowed_Pos and PassableLeft:
                for row in BrickWallList.copy():
                    if row == [BombPosX - velocity * distance, BombPosY]:
                        BrickWallList.remove(row)
                        PassableLeft = False
                        if random.randint(0, 2) == 1:
                            BonusList.append(row)

                if not [BombPosX - velocity * distance, BombPosY] in BonusList:
                    ExplosionPos.append([BombPosX - velocity * distance, BombPosY])

                if [BombPosX - velocity * distance, BombPosY] == [BallonPosX, BallonPosY]:
                    PassableRight = False
                    BallonDead = True

            else:
                PassableLeft = False

            if not [BombPosX, BombPosY + velocity * distance] in Not_Allowed_Pos and PassableDown:
                for row in BrickWallList.copy():
                    if row == [BombPosX, BombPosY + velocity * distance]:
                        PassableDown = False
                        BrickWallList.remove(row)
                        if random.randint(0, 2) == 1:
                            BonusList.append(row)

                if not [BombPosX, BombPosY + velocity * distance] in BonusList:
                    ExplosionPos.append([BombPosX, BombPosY + velocity * distance])

                if [BombPosX, BombPosY + velocity * distance] == [BallonPosX, BallonPosY]:
                    PassableRight = False
                    BallonDead = True

            else:
                PassableDown = False

            if not [BombPosX, BombPosY - velocity * distance] in Not_Allowed_Pos and PassableUp:
                for row in BrickWallList.copy():
                    if row == [BombPosX, BombPosY - velocity * distance]:
                        BrickWallList.remove(row)
                        PassableUp = False
                        if random.randint(0, 2) == 1:
                            BonusList.append(row)

                if not [BombPosX, BombPosY - velocity * distance] in BonusList:
                    ExplosionPos.append([BombPosX, BombPosY - velocity * distance])

                if [BombPosX, BombPosY - velocity * distance] == [BallonPosX, BallonPosY]:
                    PassableRight = False
                    BallonDead = True
            else:
                PassableUp = False

    if ExplosionTime + ExplosionDuration > Time1:
        for Y in ExplosionPos:
            if not Y in Not_Allowed_Pos:
                win.blit(Explosion, Y)
            if ExplodedSound == False:
                BombSound.play()
                ExplodedSound = True
    else:
        ExplosionPos.clear()
        ExplodedSound = False
        Exploding = False
        PassableUp = True
        PassableDown = True
        PassableRight = True
        PassableLeft = True


def CheckIfDead():
    if Exploding == True and [posX, posY] in ExplosionPos:
        quit()


Time1 = pygame.time.get_ticks()

ExplosionTime = Time1

pygame.mixer.music.play(-1)

music = pygame.mixer.music.load("sounds/Gameplay.mp3")
pygame.mixer.music.play(-1)

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
                if not [posX - velocity, posY] in Not_Allowed_Pos:
                    if not [posX - velocity, posY] in BrickWallList:
                        if not [posX - velocity, posY] in BombPos:
                            posX -= velocity
                            if [posX, posY] in BonusList:
                                UpgradeSound.play()
                                BombRange += 1
                                BonusList.remove([posX, posY])

            if event.key == pygame.K_RIGHT:
                way = 2
                if not [posX + velocity, posY] in Not_Allowed_Pos:
                    if not [posX + velocity, posY] in BrickWallList:
                        if not [posX + velocity, posY] in BombPos:
                            posX += velocity
                            if [posX, posY] in BonusList:
                                UpgradeSound.play()
                                BombRange += 1
                                BonusList.remove([posX, posY])

            if event.key == pygame.K_UP:
                way = 1
                if not [posX, posY - velocity] in Not_Allowed_Pos:
                    if not [posX, posY - velocity] in BrickWallList:
                        if not [posX, posY - velocity] in BombPos:
                            posY -= velocity
                            if [posX, posY] in BonusList:
                                UpgradeSound.play()
                                BombRange += 1
                                BonusList.remove([posX, posY])

            if event.key == pygame.K_DOWN:
                way = 0
                if not [posX, posY + velocity] in Not_Allowed_Pos:
                    if not [posX, posY + velocity] in BrickWallList:
                        if not [posX, posY + velocity] in BombPos:
                            posY += velocity
                            if [posX, posY] in BonusList:
                                UpgradeSound.play()
                                BombRange += 1
                                BonusList.remove([posX, posY])

            if event.key == pygame.K_k:
                if _BombDown == False and BombAmmount == 0 and Exploding == False:
                    BombPosX, BombPosY = posX, posY
                    _BombDown = True
                    bombtimer = Time1
                    BombAmmount += 1
    GameIntro()
    CreateBackground()
    Bomber()
    BombDown()
    Explode()
    CheckIfDead()
    BallonEnemy()
    pygame.display.update()

pygame.quit()