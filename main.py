import pygame
import random

pygame.init()

screenW = 800
screenH = 600
screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption('Mars Mathematical Materials')

playerImg = pygame.image.load('sprites\player.png')
playerX = 390
playerY = 85
playerX_change = 0
playerY_change = 0
playerMoveSpeed = 3
playerSideToCheck = "D"
playerTopAtWall = False
playerBottomAtWall = False
playerLeftAtWall = False
playerRightAtWall = False

font = pygame.font.SysFont("Arial", 20)


def text(contents, x, y):
    textcontent = font.render(contents, 1, (0, 0, 0))
    screen.blit(textcontent, (x, y))


def maze(filepath, x, y, widthScale, heightScale):
    imp = pygame.image.load(filepath).convert()
    imp = pygame.transform.scale(imp, (imp.get_width() * widthScale, imp.get_height() * heightScale))
    screen.blit(imp, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def wallAtPlayerSide(side):
    try:
        if playerSideToCheck == "U":
            color = screen.get_at((playerX, playerY - 3))
            color2 = screen.get_at((playerX + int(playerImg.get_width() / 3), playerY - 3))
            color3 = screen.get_at((playerX + int(playerImg.get_width() / 1.5), playerY - 3))
            color4 = screen.get_at((playerX + playerImg.get_width(), playerY - 3))
        elif playerSideToCheck == "L":
            color = screen.get_at((playerX - 2, playerY))
            color2 = screen.get_at((playerX - 2, playerY + int(playerImg.get_height() / 3)))
            color3 = screen.get_at((playerX - 2, playerY + int(playerImg.get_height() / 1.5)))
            color4 = screen.get_at((playerX - 2, playerY + playerImg.get_height()))
        elif playerSideToCheck == "D":
            color = screen.get_at((playerX, playerY + 12))
            color2 = screen.get_at((playerX + int(playerImg.get_width() / 3), playerY + 12))
            color3 = screen.get_at((playerX + int(playerImg.get_width() / 1.5), playerY + 12))
            color4 = screen.get_at((playerX + playerImg.get_width(), playerY + 12))
        elif playerSideToCheck == "R":
            color = screen.get_at((playerX + 12, playerY))
            color2 = screen.get_at((playerX + 12, playerY + int(playerImg.get_height() / 3)))
            color3 = screen.get_at((playerX + 12, playerY + int(playerImg.get_height() / 1.5)))
            color4 = screen.get_at((playerX + 12, playerY + playerImg.get_height()))

        if color == (0, 0, 0, 255) or color2 == (0, 0, 0, 255) or color3 == (0, 0, 0, 255) or color4 == (0, 0, 0, 255):
            return True
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

    screen.fill((255, 255, 255))

    maze("mazes/maze1.png", screenW/4, screenH/6, 1.5, 1.5)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_SPACE:
                paused = True if paused == False else False
                print("paused?: ", paused)
            if event.key == pygame.K_LEFT:
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "L"
                if not wallAtPlayerSide("L"):
                    playerX_change = -playerMoveSpeed
            elif event.key == pygame.K_RIGHT:
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "R"
                if not wallAtPlayerSide("R"):
                    playerX_change = playerMoveSpeed
            elif event.key == pygame.K_UP:
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "U"
                if not wallAtPlayerSide("U"):
                    playerY_change = -playerMoveSpeed
            elif event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "D"
                if not wallAtPlayerSide("D"):
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

    player(playerX, playerY)
    text("x: {}, y: {}, x mov: {}, y mov: {}, side moving: {}, wall at side?: {}".format(playerX, playerY, playerX_change, playerY_change, playerSideToCheck, wallAtPlayerSide(playerSideToCheck)), 0, 0)
    pygame.display.update()

    if wallAtPlayerSide(playerSideToCheck):
        if playerSideToCheck == "L":
            playerX_change = 0
            playerLeftAtWall = True
        elif playerSideToCheck == "R":
            playerX_change = 0
            playerRightAtWall = True
        elif playerSideToCheck == "U":
            playerY_change = 0
            playerTopAtWall = True
        elif playerSideToCheck == "D":
            playerY_change = 0
            playerBottomAtWall = True

    clock.tick(60)  # game runs at 60 FPS
