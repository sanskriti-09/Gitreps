import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

bg = pygame.image.load("background.jpg")

mixer.music.load('Epic Sport Rock.mp3')
mixer.music.play(-1)

pygame.display.set_caption("Sniper")
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Adding Image SNIPER
sniperImg = pygame.image.load("shooter.png")
sniperX = 655
sniperY = 350
sniperY_change = 0

# Adding Image BANDIT

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("bandit.png"))
    enemyX.append(random.randint(0, 400))
    enemyY.append(random.randint(0, 500))
    enemyX_change.append(40)
    enemyY_change.append(3)

# Adding Image BULLET
bulletImg = pygame.image.load("bullets.png")
bulletX = 650
bulletY = 350
bulletX_change = 20
bulletY_change = 0
bullet_state = "ready"

score_val = 0
font = pygame.font.Font("Roboto-Black.ttf", 32)
textX = 10
textY = 10

game_over = pygame.font.Font("KeeponTruckin.ttf", 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_val), True, (0, 0, 0))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = game_over.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 170))


def player(x, y):
    screen.blit(sniperImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x - 15, y + 18))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 15:
        return True
    else:
        return False


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                sniperY_change = -3
            if event.key == pygame.K_DOWN:
                sniperY_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = sniperX
                    fire_bullet(bulletX, sniperY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                sniperY_change = 0

    screen.fill((0, 0, 0))

    screen.blit(bg, (0, 0))

    sniperY += sniperY_change

    if sniperY <= 0:
        sniperY = 0
    elif sniperY >= 472:
        sniperY = 472

    for i in range(num_of_enemies):

        if enemyX[i] > 540:
            for j in range(num_of_enemies):
                enemyX[j] = 2000
            game_over_text()
            break

        enemyY[i] += enemyY_change[i]

        if enemyY[i] <= 0:
            enemyY_change[i] = 0.5
            enemyX[i] += enemyX_change[i]
        elif enemyY[i] >= 500:
            enemyY_change[i] = -0.5
            enemyX[i] += enemyX_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            exp_sound = mixer.Sound("explosion.wav")
            exp_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_val += 1
            print(score_val)
            enemyX[i] = random.randint(0, 400)
            enemyY[i] = random.randint(0, 500)

        enemy(enemyX[i], enemyY[i], i)

    if bulletX <= 0:
        bulletX = 650
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, sniperY)
        bulletX -= bulletX_change

    player(sniperX, sniperY)
    show_score(textX, textY)
    pygame.display.update()
