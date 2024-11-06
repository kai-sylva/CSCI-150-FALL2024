#Kai Rebich - game.py
#11/6/2024 - CSCI 150
#This file is a simulation of a simple adventure game using the
#functions imported from gamefunctions.py

import gamefunctions

# Check if save files exist. If not, new game.
if gamefunctions.checkSaveExists() == False:
    user_stats, inventory = gamefunctions.newGame()
else:
    user_stats, inventory = gamefunctions.loadFromSave()

# Display initial user stats and inventory
gamefunctions.getUserStats(user_stats)
gamefunctions.getUserInventory(inventory, "Inventory")

# Dictionary with current shop items
shop_items = {
    'health potion': {'price': 50, 'quantity': 1, 'type': 'potion', 
                      'name': 'health potion', 'equipped': False},
    'sword': {'price': 100, 'quantity': 'single', 'type': 'weapon', 'durability': 5, 
              'max durability': 10, 'attack power': 500, 'name': 'sword',
              'equipped': False},
    'instakill': {'price': 100, 'quantity': 1, 'type': 'spell',
                        'name': 'instakill', 'equipped': False}
}

# Main game loop
quit_game = False

while quit_game == False:
    game_options = gamefunctions.getUserGameOptions()
    user_action = gamefunctions.verifyInput("\nWhat would you like to do? ", game_options)
    if user_action == '1':
        gamefunctions.buyShopItems(user_stats, shop_items, inventory)
    elif user_action == '2':
        gamefunctions.fightMonster(user_stats, inventory)
    elif user_action == '3':
        gamefunctions.equipWeapon(user_stats, inventory)
    elif user_action == '4':
        gamefunctions.sleep(user_stats)
    elif user_action == '5':
        gamefunctions.drinkHealthPotion(user_stats, inventory)
    elif user_action == '6':
        gamefunctions.getUserStats(user_stats)
    elif user_action == '7':
        gamefunctions.getUserInventory(inventory, "Inventory")
    elif user_action == '8':
        gamefunctions.repairWeapon(user_stats, inventory)
    elif user_action == 'q':
        quit_game = True
    elif user_action == 'cheat gold':
        user_stats['currentMoney'] = 1000000

if quit_game == True:
    msg = "Would you like to save your progress?(y/n) "
    saveGame = gamefunctions.verifyInput(msg, ['y', 'n'])
    if saveGame == 'y':
        gamefunctions.saveGame(user_stats, inventory)
        print("Save successful!\n")
    elif saveGame == 'n':
        print()

    print(f"Thanks for playing, {user_stats['user_name']}!")