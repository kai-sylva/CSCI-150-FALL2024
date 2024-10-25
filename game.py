#Kai Rebich - game.py
#10/24/2024 - CSCI 150
#This file is a simulation of a simple game using the
#functions imported from gamefunctions.py

import gamefunctions

# Get user's name, print welcome
user_name = input("What is your name? ")
print("")
gamefunctions.print_welcome(user_name)

# Dictionary with user stats
user_stats = {
    'user_name': user_name,
    'currentHP': 100,
    'currentMoney': 250,
    'health_potions': 1
}

# Dictionary with current shop items
shop_items = {
    'apples': 1,
    'strawberries': 2,
    'health potion': 50
}

# Display (default) user stats
print("Here are your stats!")
gamefunctions.getUserStats(user_stats)

# Main game loop
quit_game = False

while quit_game == False:
    gamefunctions.getUserGameOptions()
    user_action = input("\nWhat would you like to do? ")
    if user_action == '1':
        gamefunctions.buyShopItems(user_stats, shop_items)
    elif user_action == '2':
        gamefunctions.fightMonster(user_stats)
    elif user_action == '3':
        gamefunctions.sleep(user_stats)
    elif user_action == '4':
        gamefunctions.drinkHealthPotion(user_stats)
    elif user_action == '5':
        gamefunctions.getUserStats(user_stats)
    elif user_action == 'q':
        quit_game = True
    else:
        print("Invalid option, please try again")

if quit_game == True:
    print(f"Thanks for playing, {user_name}!")