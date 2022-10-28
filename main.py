import pygame
import random

pygame.init()

DEBUGMODE = True

screenW = 800
screenH = 600
screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption('Mars Mathematical Materials')

playerImg = pygame.image.load('sprites\player.png')
initialPlayerX = 375
initialPlayerY = 80
playerX = initialPlayerX
playerY = initialPlayerY
playerX_change = 0
playerY_change = 0
playerMoveSpeed = 3
playerSideToCheck = "D"

questionImg = pygame.image.load('sprites\question.png')


def text(contents, x, y, font="Arial", size=20):
    textcontent = pygame.font.SysFont(font, size).render(contents, 1, (0, 0, 0))
    screen.blit(textcontent, (x, y))


def maze(filepath, x, y, widthScale, heightScale):
    imp = pygame.image.load(filepath).convert()
    imp = pygame.transform.scale(imp, (imp.get_width() * widthScale, imp.get_height() * heightScale))
    screen.blit(imp, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def question(contents, x, y):
    screen.blit(questionImg, (x, y))


def wallAtPlayerSide(side):
    try:
        if playerSideToCheck == "U":
            color = screen.get_at((playerX, playerY - 3))
            color2 = screen.get_at((playerX + int(playerImg.get_width() / 3), playerY - 3))
            color3 = screen.get_at((playerX + int(playerImg.get_width() / 1.5), playerY - 3))
            color4 = screen.get_at((playerX + playerImg.get_width(), playerY - 3))
        elif playerSideToCheck == "L":
            color = screen.get_at((playerX - 3, playerY))
            color2 = screen.get_at((playerX - 3, playerY + int(playerImg.get_height() / 3)))
            color3 = screen.get_at((playerX - 3, playerY + int(playerImg.get_height() / 1.5)))
            color4 = screen.get_at((playerX - 3, playerY + playerImg.get_height() - 1))
        elif playerSideToCheck == "D":
            color = screen.get_at((playerX, playerY + 12))
            color2 = screen.get_at((playerX + int(playerImg.get_width() / 3), playerY + 12))
            color3 = screen.get_at((playerX + int(playerImg.get_width() / 1.5), playerY + 12))
            color4 = screen.get_at((playerX + playerImg.get_width(), playerY + 12))
        elif playerSideToCheck == "R":
            color = screen.get_at((playerX + 13, playerY))
            color2 = screen.get_at((playerX + 13, playerY + int(playerImg.get_height() / 3)))
            color3 = screen.get_at((playerX + 13, playerY + int(playerImg.get_height() / 1.5)))
            color4 = screen.get_at((playerX + 13, playerY + playerImg.get_height() - 1))

        if color == (0, 0, 0, 255) or color2 == (0, 0, 0, 255) or color3 == (0, 0, 0, 255) or color4 == (0, 0, 0, 255):
            return True
        if color == (255, 255, 0, 255) or color2 == (255, 255, 0, 255) or color3 == (255, 255, 0, 255) or color4 == (255, 255, 0, 255):
            print("questionImg Touched")
            questionImg.fill((0, 0, 0, 0))
        elif color == (255, 255, 255, 255) and color2 == (255, 255, 255, 255) and color3 == (255, 255, 255, 255) and color4 == (255, 255, 255, 255):
            return False
        else:
            return True
    except:
        return False


paused = False
running = True
clock = pygame.time.Clock()
while running:

    screen.fill((255, 155, 155))

    maze("mazes/maze1.png", 150, 75, 1.5, 1.5)

    question("Test contents", 210, 200)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                DEBUGMODE = not DEBUGMODE
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_F11:
                pygame.display.toggle_fullscreen()
            if event.key == pygame.K_SPACE:
                paused = not paused
                print("paused?: ", paused)
                if paused:
                    playerX_change = 0
                    playerY_change = 0
            if event.key == pygame.K_LEFT:
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "L"
                if not wallAtPlayerSide("L") and not paused:
                    playerX_change = -playerMoveSpeed
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "R"
                if not wallAtPlayerSide("R") and not paused:
                    playerX_change = playerMoveSpeed
            elif event.key == pygame.K_UP:
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "U"
                if not wallAtPlayerSide("U") and not paused:
                    playerY_change = -playerMoveSpeed
            elif event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "D"
                if not wallAtPlayerSide("D") and not paused:
                    playerY_change = playerMoveSpeed
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    # Defining Movement
    playerX += playerX_change
    playerY += playerY_change

    # Defining Player Bounds
    if playerX <= 0:
        playerX = 0
    elif playerX >= screenW - playerImg.get_width():
        playerX = screenW - playerImg.get_width()

    if playerY <= 0:
        playerY = 0
    if playerY >= screenH - playerImg.get_height():
        playerY = screenH - playerImg.get_height()

    if playerY >= 548:
        print("Done!")
        playerX = initialPlayerX
        playerY = initialPlayerY

    player(playerX, playerY)
    if DEBUGMODE:
        text("Press D to hide: x: {}, y: {}, x mov: {}, y mov: {}, side moving: {}, wall at side?: {}".format(playerX, playerY, playerX_change, playerY_change, playerSideToCheck, wallAtPlayerSide(playerSideToCheck)), 20, 10)
    if paused:
        text("-PAUSED-", 50, 500, "Impact", 24)
    pygame.display.flip()

    if wallAtPlayerSide(playerSideToCheck):
        if playerSideToCheck == "L":
            playerX_change = 0
        elif playerSideToCheck == "R":
            playerX_change = 0
        elif playerSideToCheck == "U":
            playerY_change = 0
        elif playerSideToCheck == "D":
            playerY_change = 0

    clock.tick(60)  # game runs at 60 FPS
