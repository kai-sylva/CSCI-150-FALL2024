### Kai Rebich
### 11/18/2024
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

# Dictionary with main shop items
shop_items = {
    'health potion': {'price': 50, 'quantity': 1, 'type': 'potion', 
                      'name': 'health potion', 'equipped': False},
    'sword': {'price': 100, 'quantity': 'single', 'type': 'weapon', 'durability': 5, 
              'max durability': 10, 'attack power': 500, 'name': 'sword',
              'equipped': False},
    'instakill': {'price': 100, 'quantity': 1, 'type': 'spell',
                        'name': 'instakill', 'equipped': False}, 
    'shield': {'price': 200, 'quantity': 'single', 'type': 'shield', 'durability': 10,
               'max durability': 20, 'defense power': 10, 'name': 'shield'}
}

shop_pos = {'x_pos': 256, 'y_pos': 160}
main_shop = Shop(shop_pos, shop_items)

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
                user = User(user_stats, inventory)
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
                        user = User(user_stats, inventory)
                        started = True
                    # Creates new set of default stats
                    elif highlight == 2:
                        user_stats, inventory = gamefunctions.newGame(default=True)
                        user = User(user_stats, inventory)
                        started = True
    clock.tick(60)
    pygame.display.flip()

# Initialize list of monsters on screen
monsters = []
monsters.append(Monster(enderman=True))

# Main game loop
# track user movement (for monster movement)
move_iter = 1
running = True
while running:
    game.screen.fill((50, 50, 50))
    stats = gamefunctions.getUserStats(user.stats, display=False)
    drawStats(game.screen, game.font, stats, 0, 0)
    main_shop.draw(game.screen)
    drawUser(game.screen, user.pos)
    # If no monsters exist, create two new ones
    if len(monsters) == 0:
        monsters.append(Monster(enderman=True))
        monsters.append(Monster(enderman=True))
    # Draw each monster onto screen
    for monster in monsters:
        monster.draw(game.screen)
    # Check for user interacting with monster
    for monster in monsters:
        if user.pos == monster.pos:
            drawUser(game.screen, user.pos)
            drawOverlay(game.screen, user.pos, monster.image)
            pygame.display.flip()
            result = gamefunctions.fightMonster(user.stats, user.inventory, monster.stats)
            if result == 'victory':
                # Remove dead monster
                monsters.remove(monster)
                # Reset user position
                user.pos = {'x_pos': 32, 'y_pos': 128}
            elif result == 'defeat':
                user.pos = {'x_pos': 32, 'y_pos': 128}
            elif result == 'quit':
                user.pos = {'x_pos': 32, 'y_pos': 128}

    # Check for user interacting with shop
    if user.pos == main_shop.pos:
        drawUser(game.screen, user.pos)
        drawOverlay(game.screen, user.pos, main_shop.image)
        pygame.display.flip()
        quit_interact = main_shop.interact(user.stats, user.inventory)
        if quit_interact == True:
            user.pos['x_pos'] -= 32

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        elif event.type == pygame.KEYDOWN:
            # Move user down 32 pixels
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                move_iter += 1
                user.move(y=32)
            # ... up 32 pixels
            elif event.key == pygame.K_w or event.key == pygame.K_UP:
                move_iter += 1
                user.move(y=-32)
            # ... right 32 pixels
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                move_iter += 1
                user.move(x=32)
            # ... left 32 pixels
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                move_iter += 1
                user.move(x=-32)
            # a second way to end the game
            elif event.key == pygame.K_q:
                running = False
    
    # Move monster(s) every time move_iter is 3 and reset move_iter
    if move_iter % 3 == 0:
        for monster in monsters:
            monster.move()
        move_iter = 1
    clock.tick(60)
    pygame.display.flip()

# If user ends game with 'q', give option to save stats
save_selection = saveGame(game.screen, game.font)
if save_selection == 1:
    gamefunctions.saveGame(user.stats, inventory)

pygame.quit()