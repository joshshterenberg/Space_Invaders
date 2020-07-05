import pygame
import random
import math
from pygame import mixer
#initialize pygame
pygame.init()

#creates screen / background / sound
screen = pygame.display.set_mode((800,600))
background = pygame.image.load('SpaceInvaders/background.png')
mixer.music.load('SpaceInvaders/background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders!!!")
icon = pygame.image.load('SpaceInvaders/spaceship.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('SpaceInvaders/player.png')
playerX = 370
playerY = 480
playerX_change = 0

#Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('SpaceInvaders/alien.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(1.5)
    enemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load('SpaceInvaders/bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 4
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (220,220,220))
    screen.blit(score, (x,y))
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (220,220,220))
    screen.blit(over_text, (200,250))
def player(x,y):
    screen.blit(playerImg, (x,y))
def enemy(x,y,i):
    screen.blit(enemyImg[i], (x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10))
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

#Game Loop
running = True
while running:
    #RGB background fill
    screen.fill((0,0,30))
    screen.blit(background, (0,0))
    #keeps window open until you click close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #checks keystrokes to move character
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -2
            if event.key == pygame.K_RIGHT:
                playerX_change = 2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('SpaceInvaders/laser.wav')
                    bullet_sound.play()
                    #gets current x coordinate of spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    #updates player position
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    #updates enemy position
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        #collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('SpaceInvaders/explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    #UPDATES DISPLAY
    pygame.display.update()
