### Kai Rebich
### 11/15/2024
### gameGraphics.py
### A version of game.py that utilizes pyGame for graphics

import gamefunctions
from os import path
from sys import exit
from graphicsFunctions import *

# Initialize game with font, screen size, and initial user position
game = MyAdventure()
clock = pygame.time.Clock()

# Check if save files exist
newGame = False
if not path.exists("user_stats.json"):
    start_options = ["Starting new game... (press enter)"]
    newGame = True
    highlight = 0
else:
    start_options = ["Start from save or new game? (press enter)",
    "1) Start from save",
    "2) New Game"]
    highlight = 1

# Initial screen
started = False
while started == False:
    game.screen.fill((50,50,50))
    drawOptions(game.screen, game.font, start_options, 0, 160, highlight)
    # If no save files exist, show "Starting from new game..."
    if newGame == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                started = True
                # sys.exit() if user doesn't want to start game
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                user_stats, inventory = gamefunctions.newGame(default=True)
                started = True
    # If save files exist, give user option to load from save or start new
    else: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                started = True
                exit()
            elif event.type == pygame.KEYDOWN:
                # highlight is used to select between options
                if event.key == pygame.K_DOWN:
                    highlight = 2
                elif event.key == pygame.K_UP:
                    highlight = 1
                elif event.key == pygame.K_RETURN:
                    # Loads user's stats from json file
                    if highlight == 1:
                        user_stats, inventory = gamefunctions.loadFromSave()
                        started = True
                    # Creates new set of default stats
                    elif highlight == 2:
                        user_stats, inventory = gamefunctions.newGame(default=True)
                        started = True
    clock.tick(60)
    pygame.display.flip()

# Main game loop
running = True
while running:
    game.screen.fill((50, 50, 50))
    stats = gamefunctions.getUserStats(user_stats, display=False)
    drawStats(game.screen, game.font, stats, 0, 0)
    drawUser(game.screen, game.user_pos)
    drawShop(game.screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        elif event.type == pygame.KEYDOWN:
            # Move user down 32 pixels
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                moveUser(game.user_pos, y=32)
            # ... up 32 pixels
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                moveUser(game.user_pos, y=-32)
            # ... right 32 pixels
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                moveUser(game.user_pos, x=32)
            # ... left 32 pixels
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                moveUser(game.user_pos, x=-32)
            # a second way to end the game
            elif event.key == pygame.K_q:
                running = False
    clock.tick(60)
    pygame.display.flip()

# If user ends game with 'q', give option to save stats
save_selection = saveGame(game.screen, game.font)
if save_selection == 1:
    gamefunctions.saveGame(user_stats, inventory)

pygame.quit()