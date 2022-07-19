from turtle import distance
import pygame
import random
import math 
from pygame import mixer

#Initialize the pygame
pygame.init()

#Creating the screen
screen = pygame.display.set_mode((800,600))

#Adding background image
background = pygame.image.load('space_bg.jpg')
#Scalling the image according to the need
final_bg = pygame.transform.scale(background,(800,600))

#Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

#Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('main_spaceship.png')
playerX = 370
playerY = 450
playerX_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.35)
    enemyY_change.append(40)

#Bullet
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.3  #Bullet Speed
bullet_state = "ready" 
# Ready- You can't see the bullet on the screen.
# Fire- The bullet is currently moving.


#Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',64)

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))

def player(x,y):
    #Drawing player in given co-ordinate
    screen.blit(playerImg,(x, y))

def enemy(x,y,i):
    #Drawing enemy in given co-ordinate
    screen.blit(enemyImg[i],(x, y))

def fire_bullet(x,y):
    #Function for executing the firing of bullet
     global bullet_state
     bullet_state = "fire"
     screen.blit(bulletImg,(x +16, y +10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    #Function for calculating distance between enemy and bullet
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))

    if distance < 27:
        return True

#Game Loop
running = True
while running :

    #RGB = (Red, Green, Blue)
    screen.fill((0,0,0))

    #Background Image
    screen.blit(final_bg,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        #if keyboard is pressed check whether it's right or left.
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
               playerX_change = -1
            
            if event.key == pygame.K_RIGHT:
                playerX_change = 1

            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX  #Assigning the x-coordinate of the spaceship in the bulletX
                    fire_bullet(bulletX, bulletY)
            
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
               playerX_change = 0
    
    #Checking for boundries of player
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    
    elif playerX >= 735:
        playerX = 735

    #Checking for boundries of enemies
    for i in range(num_of_enemies):

        #GAME OVER
        if enemyY[i] > 420:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.35
            enemyY[i] += enemyY_change[i]
        
        elif enemyX[i] >= 735:
            enemyX_change[i] = -0.35
            enemyY[i] += enemyY_change[i]

        #Collision 
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i],enemyY[i], i)
    
    #Resetting the bullet position
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    #Bullet Movement
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
