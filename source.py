import pygame
from random import randint
import time
import os
import math
pygame.font.init()

# use the code below to make spacegame.exe
# pyinstaller --onefile -w --icon='icon.ico' .\source.py

#import images
BG = pygame.image.load('Assets\\background.jpg')
SHIP = pygame.image.load('Assets\\spaceship.png')
ALIEN = pygame.image.load('Assets\\ufo.png')
BULLET = pygame.image.load('Assets\\bullet.png')
MISSILE = pygame.image.load('Assets\\missile.png')
ICON = pygame.image.load('Assets\\logo.png')

#set display
WIDTH, HEIGHT = 640, 427
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Space Game")
pygame.display.set_icon(ICON)

arrx = [-50]*50
arry = [-50]*50
arrz = [0]*50

lives = 0
score = 0

def free_array():
    for i in range(50):
        if arry[i] == -50:
            return i
    return 0

class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
    
    def update(self):
        self.x, self.y = pygame.mouse.get_pos()
        if self.x == 0 or self.y == 0 or self.x == WIDTH-1 or self.y == HEIGHT-1:
            self.x = WIDTH/2
            self.y = HEIGHT/1.3
        WIN.blit(SHIP, (self.x-16, self.y-16))

class Projectile:
    def __init__(self, vel, count_down):
        self.x = 0
        self.y = 0
        self.vel = vel
        self.count_down = count_down
        self.cool_down = 0    

    def fire(self, ammunation):
        if self.cool_down == 0:
            self.x, self.y = pygame.mouse.get_pos()
            index = free_array()
            arrx[index] = self.x
            arry[index] = self.y
            arrz[index] = ammunation
            self.cool_down = self.count_down
    
    def update(self):
        if self.cool_down > 0:
            self.cool_down -= 1
        for i in range(50):
            if arrz[i]!=3 and arry[i] < 0:
                arry[i] = -50
                arrx[i] = -50
                arrz[i] = 0
            else:
                if arrz[i]==1:
                    arry[i] -= 5
                elif arrz[i]==2:
                    arry[i] -= 50
            if arrz[i]==1:
                WIN.blit(BULLET, (arrx[i]-8, arry[i]-8))
            elif arrz[i]==2:
                WIN.blit(MISSILE, (arrx[i]-12, arry[i]-12))

class Enemy:
    def __init__(self, vel, count_down):
        self.x = 0
        self.y = 0
        self.vel = vel
        self.count_down = count_down
        self.cool_down = 0

    def spawn(self):
        index = free_array()
        arrx[index] = randint(50, WIDTH-50)
        arry[index] = 0
        arrz[index] = 3

    def update(self):
        global lives
        if self.cool_down == 0:
            self.spawn()
            self.cool_down=self.count_down
        else:
            self.cool_down-=1
        
        for i in range(50):
            if arrz[i]==3:
                arry[i]+=self.vel
                WIN.blit(ALIEN, (arrx[i], arry[i]))
                if arry[i]>HEIGHT:
                    arrx[i]=-50
                    arry[i]=-50
                    arrz[i]=0
                    lives-=1


def collition():
    global lives
    for i in range(50):
        if arrz[i] == 1:
            for j in range(50):
                if arrz[j] == 3:
                    if math.sqrt(pow((arrx[j]+16)-arrx[i], 2) + pow((arry[j]-16)-arry[i], 2))<16:
                        arrx[j]=-50
                        arry[j]=-50
                        arrz[j]=0
                        arrx[i]=-50
                        arry[i]=-50
                        arrz[i]=0
                        return 1
        if arrz[i] == 3:
            x, y = pygame.mouse.get_pos()
            if math.sqrt(pow((x)-arrx[i], 2) + pow((y)-arry[i], 2))<32:
                arrx[i]=-50
                arry[i]=-50
                arrz[i]=0
                lives-=1

    return 0

def endScreen():
    global score
    main_font = pygame.font.SysFont(None, 35)
    WIN.blit(BG, (0,0))
    label = main_font.render("You Lost!", 1, (255, 255, 255))
    score_label = main_font.render(f"Your Score: {score}", 1, (255, 255, 255))

    WIN.blit(label,(((WIDTH/2)-label.get_width()/2), ((HEIGHT/2)-50)))
    WIN.blit(score_label, (((WIDTH/2)-score_label.get_width()/2), (HEIGHT/2)))

    pygame.display.update()

def main():
    global score
    run = True
    FPS = 60
    global lives
    score = 0
    lives = 1
    main_font = pygame.font.SysFont(None, 35)

    clock = pygame.time.Clock()

    spaceship = Player()
    bullet = Projectile(2, 20)
    missile = Projectile(1, 50)
    ufo = Enemy(1.2, 40)

    def redraw_window():
        WIN.blit(BG, (0,0))
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        score_label = main_font.render(f"Score: {score}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10, 10)) 
        WIN.blit(score_label, (WIDTH-score_label.get_width()-10, 10))

        bullet.update()
        missile.update()
        spaceship.update()
        ufo.update()

        pygame.display.update()

    while run:
        clock.tick(FPS)
        score+=collition()
        if lives>-1:
            redraw_window()
        else:
            endScreen()

        lmb, mmb, rmb = pygame.mouse.get_pressed()
        if lmb and lives>-1:
            bullet.fire(1)
        if rmb and lives>-1:
            missile.fire(2)
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        
main()       