import pygame
from pygame.locals import *
import sys
import random

class SpaceInvaders:
    def __init__(self):

        self.hp = 3
        pygame.font.init()
        self.font = pygame.font.Font("pics/space_invaders.ttf", 15)


        self.screen = pygame.display.set_mode((800, 600))
        self.enemySprites = {
                0:[pygame.image.load("pics/enemy.png").convert(), pygame.image.load("pics/enemy2.png").convert()],
                1:[pygame.image.load("pics/enemy.png").convert(), pygame.image.load("pics/enemy2.png").convert()],
                2:[pygame.image.load("pics/enemy.png").convert(), pygame.image.load("pics/enemy2.png").convert()],
                }
        self.player = pygame.image.load("pics/player.png").convert()
        self.animation = 0 #skipt á milli tveggja myndana
        self.direction = 1 #átt
        self.geimveruHreyfing = 20 #Hveru langt þau fara hvert einasta skipti
        self.geimveruHraði = 0 #Hversu hratt þau fara
        self.playerX = 400
        self.playerY = 550
        self.skot = None
        self.skotlist = []
        self.enemies = []
        startY = 50
        startX = 50
        for rows in range(6):
            out = []
            if rows < 2:
                enemy = 0
            elif rows < 4:
                enemy = 1
            else:
                enemy = 2
            for columns in range(10):
                out.append((enemy,pygame.Rect(startX * columns, startY * rows, 35, 35))) #35 er tíminn milli hreifinga
            self.enemies.append(out)
        self.skotloc = 990

        space = 10


    def enemyUpdate(self):
        if not self.geimveruHraði:
            for enemy in self.enemies:
                for enemy in enemy:
                    enemy = enemy[1]
                    if enemy.colliderect(pygame.Rect(self.playerX, self.playerY, self.player.get_width(), self.player.get_height())): #Finnur collision, ef þú ert skotinn missiru 1 live
                        self.hp -= 1
                        self.resetPlayer()
                    enemy.x += self.geimveruHreyfing * self.direction #fer til hægri/vinstri
                    self.geimveruHraði = 20
                    if enemy.x >= 750 or enemy.x <= 0: #Þegar þau komast á endan til hægri/vinstri fara þau niður
                        self.moveEnemiesDown()
                        self.direction *= -1
                    
                    skotloc = random.randint(0, 1000) #Notað til þess að skot koma frá geimveronum ekki bara á random stað
                    if skotloc > self.skotloc:
                        self.skotlist.append(pygame.Rect(enemy.x, enemy.y, 10, 20))

            if self.animation:
                self.animation -= 1
            else:
                self.animation += 1
        else:
            self.geimveruHraði -= 1
    
        
    def moveEnemiesDown(self):
        for enemy in self.enemies:
            for enemy in enemy:
                enemy = enemy[1]
                enemy.y += 20

    "Controls fyrir skipið"
    def playerUpdate(self):
        key = pygame.key.get_pressed()
        if key[K_RIGHT] and self.playerX < 800 - self.player.get_width():
            self.playerX += 5
        elif key[K_LEFT] and self.playerX > 0:
            self.playerX -= 5
        if key[K_SPACE] and not self.skot:
            self.skot = pygame.Rect(self.playerX + self.player.get_width() / 2, self.playerY - 15, 5, 10)
    "Þetta er notað þegar einhver deir, að þeir myndu hætta að skjóta, fann á google"
    def skotUpdate(self):
        for i, enemy in enumerate(self.enemies):
            for j, enemy in enumerate(enemy):
                enemy = enemy[1]
                if self.skot and enemy.colliderect(self.skot):
                    self.enemies[i].pop(j)
                    self.skot = None
                    self.skotloc -= 1

        "Hraðinn á skotinu í byssuni"
        if self.skot:
            self.skot.y -= 10
            if self.skot.y < 0:
                self.skot = None

        "Byssuhraði invadera, og að hp myndi fara niður um einn ef collide"
        for x in self.skotlist:
            x.y += 10
            if x.y > 600:
                self.skotlist.remove(x)
            if x.colliderect(pygame.Rect(self.playerX, self.playerY, self.player.get_width(), self.player.get_height())):
                self.hp -= 1
                self.skotlist.remove(x)
                self.resetPlayer()


    "Þegar hann missir Live, fer hann aftur í miðju"
    def resetPlayer(self):
        self.playerX = 400
    "Meðan prógramið er í gangi, clock til þess að leikurinn væri á réttum hraða, hérna þurfti ég smá hjálp í google"
    def run(self):
        clock = pygame.time.Clock()
        for x in range(3):
            self.moveEnemiesDown()
        while True:

            clock.tick(60)
            self.screen.fill((0,0,0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
            for enemy in self.enemies:
                for enemy in enemy:
                    self.screen.blit(pygame.transform.scale(self.enemySprites[enemy[0]][self.animation], (35,35)), (enemy[1].x, enemy[1].y)) #tók smá tíma að leita af þessu, var originally með bara 1 mynd fyrir hvert
            self.screen.blit(self.player, (self.playerX, self.playerY))
            if self.skot:
                pygame.draw.rect(self.screen, (255, 255, 255), self.skot)
            for skot in self.skotlist:
                pygame.draw.rect(self.screen, (255,255,255), skot)



            if self.hp > 0:
                self.skotUpdate()
                self.enemyUpdate()
                self.playerUpdate()

            self.screen.blit(self.font.render("HP: {}".format(self.hp), -1, (255,255,255)), (20, 10))
            pygame.display.flip()


if __name__ == "__main__":
    SpaceInvaders().run()
