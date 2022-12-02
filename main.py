import math
import tkinter.messagebox

import pygame
import random
import tkinter as tk
import button
from question import Question
from tkinter import messagebox
from equationfunction import generateEquation

pygame.init()

# Debug Mode Default (False), enable by pressing 'd' in-game
DEBUGMODE = False

# Default start time and default question difficulty
DEFAULTMAXTIME = 150
DEFAULTDIFFICULTY = 2

# Amount of time, in seconds the timer counts down to (can be changed)
MAXTIME = DEFAULTMAXTIME

# Default difficulty and amounts of questions, changes in game loop
CURRENTDIFFICULTY = DEFAULTDIFFICULTY
QUESTIONSINCURRENTMAZE = 0
QUESTIONSSEENINCURRENTMAZE = 0
CURRENTQUESTION = 0
MAZESPASSED = 0
QUESTIONSSEEN = 0
QUESTIONSCORRECT = 0
REMAININGTIME = 0

# Initializes the total score of the player
PLAYERSCORE = 0

# Sets the bounds of the GUI
screenW = 800
screenH = 600
screen = pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption('Mars Mathematical Materials')

# Assigns information to user sprite
playerImg = pygame.image.load('sprites\player.png')
initialPlayerX = 375
initialPlayerY = 80
playerX = initialPlayerX
playerY = initialPlayerY
playerX_change = 0
playerY_change = 0
playerMoveSpeed = 3
playerSideToCheck = "D"

# Creating list of maze image files
mazelist = ["mazes/maze{}.png".format(i+1) for i in range(20)]

# Sets initial maze, can be changed in the game loop
currentmaze = mazelist[random.randint(0, len(mazelist) - 1)]


def text(contents, x, y, font="Arial", size=20):
    # Displays text based off a determined X and Y coordinate
    textcontent = pygame.font.SysFont(font, size).render(contents, 1, (0, 0, 0))
    screen.blit(textcontent, (x, y))


def maze(filepath, x=150, y=75, widthScale=1.5, heightScale=1.5):
    # Takes the maze image, converts it to desired width and height, places it at an assigned X and Y coordinate
    imp = pygame.image.load(filepath).convert()
    imp = pygame.transform.scale(imp, (imp.get_width() * widthScale, imp.get_height() * heightScale))
    screen.blit(imp, (x, y))


def setmaze():
    global QUESTIONSSEENINCURRENTMAZE
    QUESTIONSSEENINCURRENTMAZE = 0
    maze(currentmaze, 150, 75, 1.5, 1.5)


def changemaze():
    global currentmaze, questionsloaded, QUESTIONSSEENINCURRENTMAZE
    questionlist.clear()
    currentmaze = mazelist[random.randint(0, len(mazelist) - 1)]
    questionsloaded = False
    QUESTIONSSEENINCURRENTMAZE = 0


def player(x, y):
    # Takes an image and assigns it to the user sprite placed at an assigned X and Y coordinate
    screen.blit(playerImg, (x, y))


def questionicon(question):
    # Assigns the math equation to a sprite placed at an assigned X and Y coordinate
    screen.blit(question.icon, (question.x, question.y))


def showHelpGUI():
    root = tk.Tk()
    root.resizable(0, 0)
    root.geometry('350x350')
    root.title("Help Menu")

    # TODO: Flesh out Help Menu
    label = tk.Label(root, text="Welcome to Mars Mathematical Materials!", font=("Arial", 14)).pack()
    label2 = tk.Label(root, text="Your player (green square) must move\n"
                                 "through the mazes quickly while touching,\n"
                                 "and attempting all questions (red squares).\n"
                                 "\n"
                                 "Only then will you be able to solve the maze\n"
                                 "itself, and move on to the next maze.\n"
                                 "\n"
                                 "Use arrow keys to move, and space to pause.\n"
                                 "\n"
                                 "Extra time is gained for answering correctly,\n"
                                 "and time is removed for wrong answers.\n"
                                 "The questions get more difficult as the mazes\n"
                                 "go on, and so do the amount of questions\n"
                                 "present. The game autosaves after each maze.\n"
                                 "\n"
                                 "Put on your thinking cap\n"
                                 "and flex your math and maze-solving muscles!", font=("Arial", 12)).pack()

    root.mainloop()


def showquestion(question):

    global CURRENTQUESTION, QUESTIONSSEEN, QUESTIONSSEENINCURRENTMAZE

    createQuestionWindow(question)
    CURRENTQUESTION += 1
    QUESTIONSSEEN += 1
    QUESTIONSSEENINCURRENTMAZE += 1


def createQuestionWindow(question):
    root = tk.Tk()
    root.resizable(0, 0)
    root.geometry('350x150')
    root.title("Quick, time is passing!".format(question.question))

    label = tk.Label(root, text="{} =".format(question.question), font=("Arial", 20)).pack()
    inputbox = tk.Text(root, height=2, width=20)
    inputbox.pack()

    def submitAnswer():
        global MAXTIME, QUESTIONSCORRECT, PLAYERSCORE

        useranswer = inputbox.get(1.0, "end-1c")
        if useranswer == str(question.answer):
            root.destroy()
            question.hidequestion()
            tkinter.messagebox.showinfo(message="{} is Correct!".format(useranswer))
            MAXTIME += CURRENTDIFFICULTY * 2
            QUESTIONSCORRECT += 1
            PLAYERSCORE += question.difficulty
        else:
            root.destroy()
            question.hidequestion()
            tkinter.messagebox.showinfo(message="Incorrect, {} is correct.".format(question.answer))
            MAXTIME -= CURRENTDIFFICULTY * 2

    button = tk.Button(root, text="Submit", command= lambda: submitAnswer()).pack()

    root.mainloop()


def wallAtPlayerSide(side):
    """
        Takes which direction the player sprite is moving
        Based off which way, records the pixels touching the side of the sprite
        Compares these recorded pixels to the defined colors if statement.
        If the color is black, it says there's a collision and to stop the user from moving that direction
        If the color is red, it identifies it as a question, prints questionImg Touched and removes the question sprite
        if the color is white, collision is false, the player sprite can progress
    """
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
            color4 = screen.get_at((playerX - 3, playerY + int(playerImg.get_height() - 1)))
        elif playerSideToCheck == "D":
            color = screen.get_at((playerX, playerY + int(playerImg.get_height() + 2)))
            color2 = screen.get_at((playerX + int(playerImg.get_width() / 3), playerY + int(playerImg.get_height() + 2)))
            color3 = screen.get_at((playerX + int(playerImg.get_width() / 1.5), playerY + int(playerImg.get_height() + 2)))
            color4 = screen.get_at((playerX + int(playerImg.get_width() + 0), playerY + int(playerImg.get_height() + 2)))
        elif playerSideToCheck == "R":
            color = screen.get_at((playerX + int(playerImg.get_width() + 2), playerY))
            color2 = screen.get_at((playerX + int(playerImg.get_width() + 2), playerY + int(playerImg.get_height() / 3)))
            color3 = screen.get_at((playerX + int(playerImg.get_width() + 2), playerY + int(playerImg.get_height() / 1.5)))
            color4 = screen.get_at((playerX + int(playerImg.get_width() + 2), playerY + int(playerImg.get_height() - 1)))

        if color == (0, 0, 0, 255) or color2 == (0, 0, 0, 255) or color3 == (0, 0, 0, 255) or color4 == (0, 0, 0, 255):
            return True
        if color == (255, 0, 0, 255) or color2 == (255, 0, 0, 255) or color3 == (255, 0, 0, 255) or color4 == (255, 0, 0, 255):
            for qToTest in questionlist:
                if abs(playerY - qToTest.y) < 10 and abs(playerX - qToTest.x) < 10:  # if user is close to a question
                    showquestion(qToTest)  # show specific question the user is touching
                    # qToTest.hidequestion()
        elif color == (255, 255, 255, 255) and color2 == (255, 255, 255, 255) and color3 == (255, 255, 255, 255) and color4 == (255, 255, 255, 255):
            return False
        else:
            return True
    except:
        return False


questionsloaded = False
questionlist = []
paused = False
running = True
global clock
clock = pygame.time.Clock()

# TODO: Have a save system in place to auto save a user's progress at the completion of each maze, and they can load the progress in the main menu

# Default behavior is to start the game at the Main Menu
ATMAINMENU = True

while running:
    # Main game loop

    # MAIN MENU Screen
    while ATMAINMENU:

        menu_state = "main"

        newgame_img = pygame.image.load("sprites/button_newgame.png").convert_alpha()
        load_img = pygame.image.load("sprites/button_load.png").convert_alpha()
        help_img = pygame.image.load("sprites/button_help.png").convert_alpha()
        quit_img = pygame.image.load("sprites/button_quit.png").convert_alpha()

        newgame_button = button.Button(20, 120, newgame_img, 1)
        load_button = button.Button(20, 220, load_img, 1)
        help_button = button.Button(20, 320, help_img, 1)
        quit_button = button.Button(20, 420, quit_img, 1)

        run = True
        while run:
            screen.fill((190, 90, 90))

            text("Placeholder Mars Mathematical Materials Main Menu Screen", 125, 10)

            text("<- TBA", 170, 250)

            # check menu state
            if ATMAINMENU:
                if menu_state == "main":
                    # draw pause screen buttons
                    if newgame_button.draw(screen):
                        MAXTIME = DEFAULTMAXTIME + pygame.time.get_ticks()/1000
                        PLAYERSCORE = 0
                        MAZESPASSED = 0
                        QUESTIONSCORRECT = 0
                        QUESTIONSSEEN = 0
                        CURRENTDIFFICULTY = DEFAULTDIFFICULTY
                        playerX = initialPlayerX
                        playerY = initialPlayerY
                        ATMAINMENU = False
                        run = False
                        changemaze()
                        setmaze()
                        questionsloaded = False
                        paused = False
                    if load_button.draw(screen):
                        print("load save button on main menu pressed")
                    if help_button.draw(screen):
                        showHelpGUI()
                    if quit_button.draw(screen):
                        pygame.quit()
            else:
                menu_state = "not"

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pass
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    run = False

            pygame.display.flip()

            ms = clock.tick_busy_loop(60)
            MAXTIME += (ms / 1000)

    # PAUSE Screen
    while running and REMAININGTIME > 0 and paused:

        menu_state = "main"

        resume_img = pygame.image.load("sprites/button_resume.png").convert_alpha()
        load_img = pygame.image.load("sprites/button_load.png").convert_alpha()
        mainmenu_img = pygame.image.load("sprites/button_mainmenu.png").convert_alpha()
        help_img = pygame.image.load("sprites/button_help.png").convert_alpha()
        quit_img = pygame.image.load("sprites/button_quit.png").convert_alpha()

        # create button instances
        resume_button = button.Button(304, 75, resume_img, 1)
        load_button = button.Button(336, 175, load_img, 1)
        mainmenu_button = button.Button(336, 275, mainmenu_img, 1)
        help_button = button.Button(336, 375, help_img, 1)
        quit_button = button.Button(336, 475, quit_img, 1)

        # game loop for pause screen
        run = True
        while run:

            screen.fill((190, 90, 90))

            text("Game is currently paused, press space to unpause.", 50, 10, font="Arial", size=30)

            text("<- TBA", 470, 200)

            # check if game is paused
            if paused:
                # check menu state
                if menu_state == "main":
                    # draw pause screen buttons
                    if resume_button.draw(screen):
                        paused = False
                        run = False
                    if load_button.draw(screen):
                        print("load save button on pause screen pressed")
                    if mainmenu_button.draw(screen):
                        ATMAINMENU = True
                        run = False
                        paused = False
                    if help_button.draw(screen):
                        showHelpGUI()
                    if quit_button.draw(screen):
                        run = False
                        pygame.quit()
                        main_state = 'off'
            else:
                menu_state = 'not'

            # event handler
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                        run = not run
                if event.type == pygame.QUIT:
                    running = False
                    run = False

            pygame.display.flip()

            ms = clock.tick_busy_loop(60)

            if paused:
                MAXTIME += (ms / 1000)

    # GAME OVER Screen
    while running and REMAININGTIME <= 0 and paused:

        menu_state = "main"

        retry_img = pygame.image.load("sprites/button_retry.png").convert_alpha()
        savescore_img = pygame.image.load("sprites/button_savescore.png").convert_alpha()
        viewscores_img = pygame.image.load("sprites/button_viewscores.png").convert_alpha()
        load_img = pygame.image.load("sprites/button_load.png").convert_alpha()
        mainmenu_img = pygame.image.load("sprites/button_mainmenu.png").convert_alpha()
        quit_img = pygame.image.load("sprites/button_quit.png").convert_alpha()

        # create button instances
        retry_button = button.Button(304, 95, retry_img, 1)
        savescore_button = button.Button(266, 195, savescore_img, 1)
        viewscores_button = button.Button(406, 195, viewscores_img, 1)
        load_button = button.Button(336, 295, load_img, 1)
        mainmenu_button = button.Button(336, 395, mainmenu_img, 1)
        quit_button = button.Button(336, 495, quit_img, 1)

        run = True
        while run:

            screen.fill((190, 90, 90))

            text("GAME OVER, press space to try again.", 125, 10, font="Arial", size=30)
            text("Final score: {:.0f}, Mazes Cleared: {}, Question Accuracy: {:.0f}% ({}/{})".format(
                PLAYERSCORE, MAZESPASSED, ((100 * (QUESTIONSCORRECT / QUESTIONSSEEN)) if QUESTIONSSEEN > 0 else 0),
                QUESTIONSCORRECT, QUESTIONSSEEN), 75, 50, font="Arial", size=24)

            text("TBA ->", 200, 230)
            text("<- TBA", 540, 230)
            text("<- TBA", 465, 330)

            def retry():
                global clock, MAXTIME, PLAYERSCORE, MAZESPASSED, QUESTIONSCORRECT, QUESTIONSSEEN, CURRENTDIFFICULTY, playerX, playerY, paused, run
                clock = pygame.time.Clock()
                MAXTIME += DEFAULTMAXTIME
                PLAYERSCORE = 0
                MAZESPASSED = 0
                QUESTIONSCORRECT = 0
                QUESTIONSSEEN = 0
                CURRENTDIFFICULTY = DEFAULTDIFFICULTY
                playerX = initialPlayerX
                playerY = initialPlayerY
                changemaze()
                paused = False
                run = False

            if REMAININGTIME <= 0 and paused:
                if menu_state == "main":
                    if retry_button.draw(screen):
                        retry()
                    if savescore_button.draw(screen):
                        print("save score button on game over screen pressed")
                    if viewscores_button.draw(screen):
                        print("view scores button on game over screen pressed")
                    if load_button.draw(screen):
                        print("load save button on game over screen pressed")
                    if mainmenu_button.draw(screen):
                        ATMAINMENU = True
                        paused = False
                        run = False
                    if quit_button.draw(screen):
                        run = False
                        pygame.quit()
                else:
                    menu_state = "not"

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        retry()
                if event.type == pygame.QUIT:
                    running = False
                    run = False

            pygame.display.flip()

            ms = clock.tick_busy_loop(60)

            if paused:
                MAXTIME += (ms / 1000)

    # This point and below in the game loop is for the actual gameplay (not pause or main menu or game over screen)

    screen.fill((190, 90, 90))

    setmaze()

    QUESTIONSINCURRENTMAZE = round(2 * math.log(7/8 * CURRENTDIFFICULTY) + 1) # changed so difficulty is less linear

    if not questionsloaded:
        playerX_change = 0
        playerY_change = 0
        for number in range(QUESTIONSINCURRENTMAZE):
            # Makes new question instances in valid locations
            x = random.randrange(155, 615, 24)
            y = random.randrange(105, 524, 24)
            q = Question(x, y, CURRENTDIFFICULTY)
            questionlist.append(q)
        questionsloaded = True

    for question in questionlist:
        questionicon(question)

    for event in pygame.event.get():  # Records a keypress
        if event.type == pygame.QUIT:  # Exits the game
            running = False
        if event.type == pygame.KEYDOWN:  # Activates debug mode
            if event.key == pygame.K_d:
                DEBUGMODE = not DEBUGMODE
            if event.key == pygame.K_m and DEBUGMODE:     # DEBUG BEHAVIOR: Change maze
                changemaze()
                PLAYERSCORE = 0
                MAZESPASSED += 1
                if QUESTIONSSEEN > 0:
                    PLAYERSCORE += 100 * CURRENTDIFFICULTY * (QUESTIONSCORRECT / QUESTIONSSEEN)
                else:
                    PLAYERSCORE += 100
                CURRENTDIFFICULTY += 2
                MAXTIME += 5 * CURRENTDIFFICULTY + 20
                DEBUGMODE = not DEBUGMODE
            if event.key == pygame.K_ESCAPE:  # Exits the game
                running = False
            if event.key == pygame.K_F11:  # Toggles fullscreen for the game
                pygame.display.toggle_fullscreen()
            if event.key == pygame.K_SPACE:  # Pauses and unpauses the instance
                paused = not paused
                if paused:  # Locks user sprite movement
                    playerX_change = 0
                    playerY_change = 0
            if event.key == pygame.K_LEFT:  # Moves user sprite left if there is no collision or pause
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "L"
                if not wallAtPlayerSide("L") and not paused:
                    playerX_change = -playerMoveSpeed
            elif event.key == pygame.K_RIGHT:  # Moves user sprite right if there is no collision or pause
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "R"
                if not wallAtPlayerSide("R") and not paused:
                    playerX_change = playerMoveSpeed
            elif event.key == pygame.K_UP:  # Moves user sprite up if there is no collision or pause
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "U"
                if not wallAtPlayerSide("U") and not paused:
                    playerY_change = -playerMoveSpeed
            elif event.key == pygame.K_DOWN:  # Moves user sprite down if there is no collision or pause
                playerX_change = 0
                playerY_change = 0
                playerSideToCheck = "D"
                if not wallAtPlayerSide("D") and not paused:
                    playerY_change = playerMoveSpeed
        if event.type == pygame.KEYUP:  # Stops user sprite movement when pressed button is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or \
                    event.key == pygame.K_DOWN:
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

    ELAPSEDTIME = pygame.time.get_ticks()/1000

    # Occurs when user sprite passes the finish line; it places the user back at start, changes the maze, saves the game
    if playerY >= 548 and (QUESTIONSINCURRENTMAZE == QUESTIONSSEENINCURRENTMAZE):
        playerX = initialPlayerX
        playerY = initialPlayerY
        MAZESPASSED += 1
        PLAYERSCORE += (100 * CURRENTDIFFICULTY * (QUESTIONSCORRECT / QUESTIONSSEEN)) if QUESTIONSSEEN > 0 \
            else (100 * CURRENTDIFFICULTY)
        CURRENTDIFFICULTY += 1
        MAXTIME += 5 * CURRENTDIFFICULTY + 20
        changemaze()
        # TODO: automatically save game progress in a file, which the player can load from the main menu or pause screen

    # Update player position visually
    player(playerX, playerY)

    # Recalculates remaining time
    if not paused:
        REMAININGTIME = MAXTIME - (pygame.time.get_ticks() / 1000)

    if REMAININGTIME <= 0:
        paused = True

    # Update timer text
    text("Time Remaining: {:.2f}".format(abs(REMAININGTIME)), 20, 40)

    # Update player score
    text("Score: {}".format(PLAYERSCORE), 650, 40)

    # Update Maze Number
    text("MAZE #{}".format(MAZESPASSED + 1), 350, 40)

    # Update total question count
    if QUESTIONSSEEN == 0:
        text("Overall Accuracy: 0%", 5, 575)
    else:
        text("Overall Accuracy: {:.0f}%".format(100 * (QUESTIONSCORRECT / QUESTIONSSEEN)), 5, 575)

    if DEBUGMODE:   # Displays the debug menu when TRUE
        text("Press D to hide: x: {}, y: {}, x mov: {}, y mov: {}, side moving: {}, wall at side?: {}".format(playerX, playerY, playerX_change, playerY_change, playerSideToCheck, wallAtPlayerSide(playerSideToCheck)), 20, 10)
    if paused:  # Displays the pause menu when TRUE
        pass
        # text("-PAUSED-", 50, 500, "Impact", 24)

    # Updates the entire display each frame
    pygame.display.flip()

    if wallAtPlayerSide(playerSideToCheck):     # Stops user sprite movement when recording collision data
        if playerSideToCheck == "L":
            playerX_change = 0
        elif playerSideToCheck == "R":
            playerX_change = 0
        elif playerSideToCheck == "U":
            playerY_change = 0
        elif playerSideToCheck == "D":
            playerY_change = 0

    ms = clock.tick_busy_loop(60)  # game runs at 60 FPS, waits 1/60th of a second to restart the game's main loop

    # Used for ensuring the remaining time on the clock doesn't decrease while the game is paused
    if paused:
        MAXTIME += (ms/1000)
