import math
import random
import os
import pygame
from pygame import mixer
os.chdir('assets/')
pygame.init()
screen = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.png')
mixer.music.load("arkaplan_kura.mp3")
mixer.music.play(-1)
pygame.display.set_caption("HTA YI VUR")
icon = pygame.image.load('siber_asker.png')
pygame.display.set_icon(icon)
hiz = 2
# Player
playerImg = pygame.image.load('siber_asker.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('hta.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)

# Bullet

# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
dosya = open("mermi.txt","r")
mermi_file = dosya.read()

bulletImg = pygame.image.load(mermi_file+'.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Hta yı vurma sayısı

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
testY = 10

# Game Over Codes
over_font = pygame.font.Font('freesansbold.ttf', 64)
Burbank_font = pygame.font.Font('BurbankBigCondensed-Bold.otf', 64)
Burbank_font_small = pygame.font.Font('BurbankBigCondensed-Bold.otf', 32)
def show_score(x, y):
    global hiz
    score = font.render("HTA TI VURMA SAYISI : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))
#    skor_str = str(score)
#    if int(skor_str) >= 31:
#        hiz = 3


def game_over_text():
    Game_over = Burbank_font.render("OYUN BİTTİ", True, (255, 255, 255))
    screen.blit(Game_over, (300, 390))

def win_text():
    playerImg = pygame.image.load('pepe_zafer.png')
    screen.blit(playerImg, (300, 780))
    Win = Burbank_font_small.render("HTA YI YENDIN SEN GERÇEK BİR SİBER ASKERSİN", True, (255, 255, 255))
    screen.blit(Win, (150, 390))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                if bullet_state is "ready":
                    bulletSound = mixer.Sound("dri.mp3")
                    bulletSound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # 5 = 5 + -0.1 -> 5 = 5 - 0.1
    # 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for i in range(num_of_enemies):

        # Game Over or Win
        if score_value > 100:
            win_text()
            break
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = int(hiz)
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -int(hiz)
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosionSound = mixer.Sound("kura.mp3")
            explosionSound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            if score_value > 30:
                hiz = 3
            if score_value > 50:
                hiz = 4
            if score_value > 75:
                hiz = 4.34
            if score_value > 99:
                playerImg = pygame.image.load('pepe_zafer.png')
                score_value = score_value + 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
