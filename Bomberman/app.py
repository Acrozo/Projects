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
intro = True

Bricks_Generated = False
BorderGenerated = False
HardWallsGenerated = False
ExplodedSound = False

PassableRight = True
PassableLeft = True
PassableUp = True
PassableDown = True

BallonDead = False
_BombDown = False
Exploding = False
BallonPosGenerated = False
GameplaySound = False

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
bombtimer = 0

clock = pygame.time.Clock()

Time1 = pygame.time.get_ticks()

Not_Allowed_Pos = []
Not_Allowed_Walls = [[32, 32], [64, 32], [32, 64], [544, 544], [512, 544], [544, 512]]
BrickWallList = []
BonusList = []
BorderPos = []
HardWalls = []
ExplosionPos1 = []
ExplosionPos2 = []
BombPos = []

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


class Bomber():

    def __init__(self, posX, posY, Bombrange):
        self.posX = posX
        self.posY = posY
        self.BombRange = Bombrange
        self.PassableRight = PassableRight
        self.PassableLeft = PassableLeft
        self.PassableUp = PassableUp
        self.PassableDown = PassableDown
        self.BallonDead = BallonDead
        self._BombDown = _BombDown
        self.Exploding = Exploding
        self.BallonPosGenerated = BallonPosGenerated
        self.BombPos = BombPos
        self.BonusList = BonusList
        self.BombPosX = posX
        self.BombPosY = posY
        self.ExplosionTime = Time1
        self.bombtimer = bombtimer
        self.ExplodedSound = ExplodedSound
        self.way = way
        self.Time1 = Time1
        self.BombAmmount = BombAmmount
        self.ExplosionPos = None

    def DrawBomber(self):
        win.blit(Bomberman1[self.way], (self.posX, self.posY))

    def BombDown(self):
        self.Time1 = Time1
        if self._BombDown == True:
            if self.bombtimer + BombDuration > self.Time1:
                self.BombPos.append([self.BombPosX, self.BombPosY])
                win.blit(Bomb, (self.BombPosX, self.BombPosY))
            else:
                self.Exploding = True
                self._BombDown = False
                self.BombAmmount -= 1
                self.ExplosionTime = Time1
                self.Explode()

    def Explode(self):
        global ExplosionPos1, ExplosionPos2
        global BallonDead
        if self.Exploding == True:
            self.BombPos.clear()
            for distance in range(0, self.BombRange, 1):
                if not [self.BombPosX + velocity * distance, self.BombPosY] in Not_Allowed_Pos and self.PassableRight:
                    for row in BrickWallList.copy():
                        if row == [self.BombPosX + velocity * distance, self.BombPosY]:
                            BrickWallList.remove(row)
                            self.PassableRight = False
                            if random.randint(0, 2) == 1:
                                self.BonusList.append(row)

                    if not [self.BombPosX + velocity * distance, self.BombPosY] in self.BonusList:
                        self.ExplosionPos.append([self.BombPosX + velocity * distance, self.BombPosY])

                    if [self.BombPosX + velocity * distance, self.BombPosY] == [BallonPosX, BallonPosY]:
                        self.PassableRight = False
                        BallonDead = True

                else:
                    self.PassableRight = False

                if not [self.BombPosX - velocity * distance, self.BombPosY] in Not_Allowed_Pos and self.PassableLeft:
                    for row in BrickWallList.copy():
                        if row == [self.BombPosX - velocity * distance, self.BombPosY]:
                            BrickWallList.remove(row)
                            self.PassableLeft = False
                            if random.randint(0, 2) == 1:
                                self.BonusList.append(row)

                    if not [self.BombPosX - velocity * distance, self.BombPosY] in self.BonusList:
                        self.ExplosionPos.append([self.BombPosX - velocity * distance, self.BombPosY])

                    if [self.BombPosX - velocity * distance, self.BombPosY] == [BallonPosX, BallonPosY]:
                        self.PassableLeft = False
                        BallonDead = True

                else:
                    self.PassableLeft = False

                if not [self.BombPosX, self.BombPosY + velocity * distance] in Not_Allowed_Pos and self.PassableDown:
                    for row in BrickWallList.copy():
                        if row == [self.BombPosX, self.BombPosY + velocity * distance]:
                            self.PassableDown = False
                            BrickWallList.remove(row)
                            if random.randint(0, 2) == 1:
                                self.BonusList.append(row)

                    if not [self.BombPosX, self.BombPosY + velocity * distance] in self.BonusList:
                        self.ExplosionPos.append([self.BombPosX, self.BombPosY + velocity * distance])

                    if [self.BombPosX, self.BombPosY + velocity * distance] == [BallonPosX, BallonPosY]:
                        self.PassableUp = False
                        BallonDead = True

                else:
                    self.PassableDown = False

                if not [self.BombPosX, self.BombPosY - velocity * distance] in Not_Allowed_Pos and self.PassableUp:
                    for row in BrickWallList.copy():
                        if row == [self.BombPosX, self.BombPosY - velocity * distance]:
                            BrickWallList.remove(row)
                            self.PassableUp = False
                            if random.randint(0, 2) == 1:
                                self.BonusList.append(row)

                    if not [self.BombPosX, self.BombPosY - velocity * distance] in self.BonusList:
                        self.ExplosionPos.append([self.BombPosX, self.BombPosY - velocity * distance])

                    if [self.BombPosX, self.BombPosY - velocity * distance] == [BallonPosX, BallonPosY]:
                        self.PassableDown = False
                        BallonDead = True
                else:
                    self.PassableUp = False

        if self.ExplosionTime + ExplosionDuration >= self.Time1:
            for Y in self.ExplosionPos:
                win.blit(Explosion, Y)
                if self.ExplodedSound == False:
                    BombSound.play()
                    self.ExplodedSound = True

        else:
            self.ExplosionPos.clear()
            self.ExplodedSound = False
            self.Exploding = False
            self.PassableUp = True
            self.PassableDown = True
            self.PassableRight = True
            self.PassableLeft = True

    def CheckIfDead(self):
        if self.Exploding == True and ([self.posX, self.posY] in ExplosionPos1 or [self.posX, self.posY] in ExplosionPos2):
            quit()


pygame.mixer.music.play(-1)

B1 = Bomber(32, 32, 3)
B2 = Bomber(544, 544, 3)
B1.ExplosionPos = ExplosionPos1
B2.ExplosionPos = ExplosionPos2

while run:
    clock.tick(30)
    Time1 = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                B1.way = 3
                if not [B1.posX - velocity, B1.posY] in Not_Allowed_Pos:
                    if not [B1.posX - velocity, B1.posY] in BrickWallList:
                        if not [B1.posX - velocity, B1.posY] in B1.BombPos:
                            B1.posX -= velocity
                            if [B1.posX, B1.posY] in B1.BonusList:
                                UpgradeSound.play()
                                B1.BombRange += 1
                                B1.BonusList.remove([B1.posX, B1.posY])

            if event.key == pygame.K_RIGHT:
                B1.way = 2
                if not [B1.posX + velocity, B1.posY] in Not_Allowed_Pos:
                    if not [B1.posX + velocity, B1.posY] in BrickWallList:
                        if not [B1.posX + velocity, B1.posY] in B1.BombPos:
                            B1.posX += velocity
                            if [B1.posX, B1.posY] in B1.BonusList:
                                UpgradeSound.play()
                                B1.BombRange += 1
                                B1.BonusList.remove([B1.posX, B1.posY])

            if event.key == pygame.K_UP:
                B1.way = 1
                if not [B1.posX, B1.posY - velocity] in Not_Allowed_Pos:
                    if not [B1.posX, B1.posY - velocity] in BrickWallList:
                        if not [B1.posX, B1.posY - velocity] in B1.BombPos:
                            B1.posY -= velocity
                            if [B1.posX, B1.posY] in B1.BonusList:
                                UpgradeSound.play()
                                B1.BombRange += 1
                                B1.BonusList.remove([B1.posX, B1.posY])

            if event.key == pygame.K_DOWN:
                B1.way = 0
                if not [B1.posX, B1.posY + velocity] in Not_Allowed_Pos:
                    if not [B1.posX, B1.posY + velocity] in BrickWallList:
                        if not [posX, posY + velocity] in B1.BombPos:
                            B1.posY += velocity
                            if [B1.posX, B1.posY] in B1.BonusList:
                                UpgradeSound.play()
                                B1.BombRange += 1
                                B1.BonusList.remove([B1.posX, B1.posY])

            if event.key == pygame.K_k:
                if B1._BombDown == False and BombAmmount == 0 and B1.Exploding == False:
                    B1.BombPosX, B1.BombPosY = B1.posX, B1.posY
                    B1._BombDown = True
                    B1.bombtimer = Time1
                    B1.BombAmmount += 1

            if event.key == pygame.K_KP4:
                B2.way = 3
                if not [B2.posX - velocity, B2.posY] in Not_Allowed_Pos:
                    if not [B2.posX - velocity, B2.posY] in BrickWallList:
                        if not [B2.posX - velocity, B2.posY] in B2.BombPos:
                            B2.posX -= velocity
                            if [B2.posX, B2.posY] in B2.BonusList:
                                UpgradeSound.play()
                                B2.BombRange += 1
                                B2.BonusList.remove([B2.posX, B2.posY])

            if event.key == pygame.K_KP6:
                B2.way = 2
                if not [B2.posX + velocity, B2.posY] in Not_Allowed_Pos:
                    if not [B2.posX + velocity, B2.posY] in BrickWallList:
                        if not [B2.posX + velocity, B2.posY] in B2.BombPos:
                            B2.posX += velocity
                            if [B2.posX, B2.posY] in B2.BonusList:
                                UpgradeSound.play()
                                B2.BombRange += 1
                                B2.BonusList.remove([B2.posX, B2.posY])

            if event.key == pygame.K_KP8:
                B2.way = 1
                if not [B2.posX, B2.posY - velocity] in Not_Allowed_Pos:
                    if not [B2.posX, B2.posY - velocity] in BrickWallList:
                        if not [B2.posX, B2.posY - velocity] in B2.BombPos:
                            B2.posY -= velocity
                            if [B2.posX, B2.posY] in B2.BonusList:
                                UpgradeSound.play()
                                B2.BombRange += 1
                                B2.BonusList.remove([B2.posX, B2.posY])

            if event.key == pygame.K_KP2:
                B2.way = 0
                if not [B2.posX, B2.posY + velocity] in Not_Allowed_Pos:
                    if not [B2.posX, B2.posY + velocity] in BrickWallList:
                        if not [posX, posY + velocity] in B2.BombPos:
                            B2.posY += velocity
                            if [B2.posX, B2.posY] in B2.BonusList:
                                UpgradeSound.play()
                                B2.BombRange += 1
                                B2.BonusList.remove([B2.posX, B2.posY])

            if event.key == pygame.K_KP5:
                if B2._BombDown == False and BombAmmount == 0 and B2.Exploding == False:
                    B2.BombPosX, B2.BombPosY = B2.posX, B2.posY
                    B2._BombDown = True
                    B2.bombtimer = Time1
                    B2.BombAmmount += 1

    GameIntro()

    if GameplaySound == False:
        music = pygame.mixer.music.load("sounds/Gameplay.mp3")
        pygame.mixer.music.play(-1)
        GameplaySound = True


    CreateBackground()

    B1.DrawBomber()
    B2.DrawBomber()

    B1.BombDown()
    B2.BombDown()

    B1.Explode()
    B2.Explode()

    B1.CheckIfDead()
    B2.CheckIfDead()

    BallonEnemy()
    pygame.display.update()

pygame.quit()
###Solve music
