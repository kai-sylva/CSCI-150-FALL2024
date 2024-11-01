#Kai Rebich - game.py
#10/31/2024 - CSCI 150
#This file is a simulation of a simple game using the
#functions imported from gamefunctions.py

import gamefunctions

# Get user's name, print welcome
user_name = input("What is your name? ")
print()
gamefunctions.print_welcome(user_name, width=0)

inventory = [
    {'name': 'health potion', 'price': 50, 'quantity': 1, 'type': 'potion', 
     'equipped': False, 'itemId': '1'}
]


# Dictionary with user stats
user_stats = {
    'user_name': user_name,
    'currentHP': 100,
    'currentMoney': 250,
    'attack_power': 20,
    'equipped_weapon': 'None',
    'weapon_power': 0,
    'weapon_id': 'None'
}

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
    gamefunctions.getUserGameOptions()
    user_action = input("\nWhat would you like to do? ")
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
    else:
        print("Invalid option, please try again\n")

if quit_game == True:
    print(f"Thanks for playing, {user_name}!")