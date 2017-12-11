import pygame
from pygame.locals import *
import sys
import random

class SpaceInvaders:
    def __init__(self):

        self.lives = 3
        pygame.font.init()
        self.font = pygame.font.Font("pics/space_invaders.ttf", 15)


        self.screen = pygame.display.set_mode((800, 600))
        self.enemySprites = {
                0:[pygame.image.load("pics/enemy.png").convert(), pygame.image.load("pics/enemy2.png").convert()],
                1:[pygame.image.load("pics/enemy.png").convert(), pygame.image.load("pics/enemy2.png").convert()],
                2:[pygame.image.load("pics/enemy.png").convert(), pygame.image.load("pics/enemy2.png").convert()],
                }
        self.player = pygame.image.load("pics/player.png").convert()
        self.animationOn = 0
        self.direction = 1
        self.enemySpeed = 20
        self.lastEnemyMove = 0
        self.playerX = 400
        self.playerY = 550
        self.bullet = None
        self.bullets = []
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
        self.skot = 990

        space = 10


    def enemyUpdate(self):
        if not self.lastEnemyMove:
            for enemy in self.enemies:
                for enemy in enemy:
                    enemy = enemy[1]
                    if enemy.colliderect(pygame.Rect(self.playerX, self.playerY, self.player.get_width(), self.player.get_height())): #Finnur collision, ef þú ert skotinn missiru 1 live
                        self.lives -= 1
                        self.resetPlayer()
                    enemy.x += self.enemySpeed * self.direction #fer til hægri/vinstri
                    self.lastEnemyMove = 25
                    if enemy.x >= 750 or enemy.x <= 0: #Þegar þau komast á endan til hægri/vinstri fara þau niður
                        self.moveEnemiesDown()
                        self.direction *= -1
                    
                    skot = random.randint(0, 1000) #Notað til þess að skot koma frá geimveronum ekki bara á random stað
                    if skot > self.skot:
                        self.bullets.append(pygame.Rect(enemy.x, enemy.y, 10, 20))

            if self.animationOn:
                self.animationOn -= 1
            else:
                self.animationOn += 1
        else:
            self.lastEnemyMove -= 1
    
        
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
        if key[K_SPACE] and not self.bullet:
            self.bullet = pygame.Rect(self.playerX + self.player.get_width() / 2- 2, self.playerY - 15, 5, 10)
    "Þetta er notað þegar einhver deir, að þeir myndu hætta að skjóta, fann á google"
    def bulletUpdate(self):
        for i, enemy in enumerate(self.enemies):
            for j, enemy in enumerate(enemy):
                enemy = enemy[1]
                if self.bullet and enemy.colliderect(self.bullet):
                    self.enemies[i].pop(j)
                    self.bullet = None
                    self.skot -= 1

        "Hraðinn á skotinu í byssuni"
        if self.bullet:
            self.bullet.y -= 10
            if self.bullet.y < 0:
                self.bullet = None

        "Byssuhraði invadera, og að lives myndi fara niður um einn ef collide"
        for x in self.bullets:
            x.y += 10
            if x.y > 600:
                self.bullets.remove(x)
            if x.colliderect(pygame.Rect(self.playerX, self.playerY, self.player.get_width(), self.player.get_height())):
                self.lives -= 1
                self.bullets.remove(x)
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
                    self.screen.blit(pygame.transform.scale(self.enemySprites[enemy[0]][self.animationOn], (35,35)), (enemy[1].x, enemy[1].y)) #tók smá tíma að leita af þessu, var originally með bara 1 mynd fyrir hvert
            self.screen.blit(self.player, (self.playerX, self.playerY))
            if self.bullet:
                pygame.draw.rect(self.screen, (255, 255, 255), self.bullet)
            for bullet in self.bullets:
                pygame.draw.rect(self.screen, (255,255,255), bullet)



            if self.lives > 0:
                self.bulletUpdate()
                self.enemyUpdate()
                self.playerUpdate()

            self.screen.blit(self.font.render("Lives: {}".format(self.lives), -1, (255,255,255)), (20, 10))
            pygame.display.flip()


if __name__ == "__main__":
    SpaceInvaders().run()
