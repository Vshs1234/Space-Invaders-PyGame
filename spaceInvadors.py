import pygame
import random
import math
from pygame import mixer
# use freepik for bg images
# use falticon for icons

# this is used to initalize the pygame...so taht we can use all the methods of it
pygame.init()

# now lets create a window
screen = pygame.display.set_mode((500, 500))

# background image
bgImg = pygame.image.load('bg.jpg')
bgImg = pygame.transform.scale(bgImg, (500, 500))

#background music
mixer.music.load("background.wav")
mixer.music.play(-1)#-1 bcz we need to play it in loop

# to create title and logo
pygame.display.set_caption("Space Invadors training", "Icon");
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

score=0
font = pygame.font.Font("freesansbold.ttf",25)#fro other fonts u can visit dafont website
textX=10
textY=10
def show_score(x,y):
    scoreDisp = font.render("Score - "+str(score),True,(255,255,255))
    screen.blit(scoreDisp,(x,y))
# for adding images to the window

# adding player
playerImg = pygame.image.load('spaceship (1).png')
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerX = 222
playerY = 425
playerChange = 0


def player(x, y):
    screen.blit(playerImg, (x, y))  # to draw the image on the screen


# adding enemy
# enemyImg = pygame.image.load('alien.png')
# enemyImg = pygame.transform.scale(enemyImg, (40, 40))
# enemyX = random.randint(0, 424)
# enemyY = random.randint(20, 100)
# enemyChangeX = 0.1
# enemyChangeY = 20
# enimies
enemyImg = []
enemyImg =[]
enemyX = []
enemyY =[]
enemyChangeX =[]
enemyChangeY =[]
numOfEnimies=4
for i in range(numOfEnimies):
    enemyImg.append(pygame.image.load('alien.png'))
    enemyImg[i]=(pygame.transform.scale(enemyImg[i], (40, 40)))
    enemyX.append(random.randint(0, 424))
    enemyY.append(random.randint(20, 100))
    enemyChangeX.append(0.1)
    enemyChangeY.append(20)



def enemy(x, y,i):
    screen.blit(enemyImg[i], (x, y))


# adding bullet

bulletImg = pygame.image.load('bullet.png')
bulletImg = pygame.transform.scale(bulletImg, (40, 40))
bulletX = 0
bulletY = 425
bulletChangeX = 0
bulletChangeY = 0.6
# ready - is not visible on scrren
# fire - ur bullet strts firing
bulletState = "ready"

def gameOver():
    gameOverFont=pygame.font.Font("freesansbold.ttf",50)
    gameOverTxt=gameOverFont.render("GAME OVER",True,(255,255,255))
    screen.blit(gameOverTxt,(100,250))

def fireBullet(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x+5, y+8))

def collide(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<40:
        return True
    return False


# coming to events all the minimize quit and fullscreens are considered to be events in pygame
# if u execute only the above code u could only get a 2 sec of window and it will disappeaer as it will run 3 lines and terminates....in order to get it properly we need to use the functionality of buttons llike only if x is pressed then window has to shut...which is done using the quit event in pygame.
# anything u wnat to display continously in window has to be written inside this while loop only
running = True

while running:
    screen.fill((2, 123, 124))
    screen.blit(bgImg, (0, 0))
    # imageX-=0.1 #movemnet of image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #         so we are gonna check weathre keystroke is pressed if pressed right or left and move it accordingly
        #     keydown is pressing the key and keyup is releaing teh key...here key means any letter o rdigit or arrows on keyboard
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                playerChange = -0.2
            elif event.key == pygame.K_RIGHT:
                playerChange = 0.2
            elif event.key == pygame.K_SPACE:
                if bulletState=="ready":
                    bulletSound=mixer.Sound("laser.wav")
                    bulletSound.play()
                    bulletX=playerX
                    fireBullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerChange = 0
    # screen.fill((2,123,124))
    #     by the above line the code is npt gng to work u need to use the below lne to screen that it got updated after evry game u need to write thi spiece of code

    playerX += playerChange
    # adding boundaries to teh space ship in order to not cross teh window
    if playerX <= 3:
        playerX = 3
    elif playerX >= 445:
        playerX = 445

    for i in range(numOfEnimies):

        # game over
        if enemyY[i]>=250:
            for j in range(numOfEnimies):
                enemyY[j]=2000
            gameOver()

        enemyX[i] += enemyChangeX[i]
        if enemyX[i]  <= 3:
            enemyChangeX[i]  = 0.1
            enemyY[i]  += enemyChangeY[i]
        elif enemyX[i]  >= 445:
            enemyChangeX[i]  = -0.1
            enemyY[i]  += enemyChangeY[i]

        collision = collide(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collisionSound = mixer.Sound("explosion.wav")
            collisionSound.play()
            bulletY = 425
            bulletState = "ready"
            score += 1
            enemyX[i] = random.randint(0, 424)
            enemyY[i]= random.randint(20, 100)
        enemy(enemyX[i], enemyY[i],i)

    if bulletY<=0:
        bulletY=425
        bulletState="ready"

    if bulletState == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletChangeY




    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()
