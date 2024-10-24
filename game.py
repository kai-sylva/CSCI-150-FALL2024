#Kai Rebich - game.py
#10/15/2024 - CSCI 150
#This file is a simulation of a simple game using the
#functions imported from gamefunctions.py

import gamefunctions
import time
import random

# Get user's name, print welcome
user_name = input("What is your name? ")
print("")
gamefunctions.print_welcome(user_name)

# Beginning of interaction at shop
gamefunctions.print_shop_menu("Apples", 0.99, "Strawberries", 2.99)

# While loop lets user choose item and locks them to only apples or strawberries
x = False
while x == False:
    item = input(f'\nWhat would you like to buy, {user_name}? ')
    if item == "apples" or item == "strawberries":
        x = True
    else:
        print("That is an invalid option.")

if item == "apples":
    itemPrice = 0.99
elif item == "strawberries":
    itemPrice = 2.99

# Take additional user inputs for transaction
quantityToPurchase = int(input(f"How many {item} would you like to purchase? "))
# FIXME consider adding a condition for if they input 0 items to purchase
startingMoney = int(input("How much money do you have? "))

transaction = gamefunctions.purchase_item(itemPrice, startingMoney, quantityToPurchase)
currentMoney = transaction[1]

# Check if user can afford what they want
if transaction[2] == True:
    print(f"""\nSorry, you can only afford {transaction[0]} {item}. 
Here they are and your change of ${transaction[1]:.2f}""")
else:
    print(f'\nAwesome, here are your {transaction[0]} {item} ' + 
f'and your change of ${transaction[1]:.2f}!')

# There's a monster outside. Generate monster and simulate time delay leaving shop
time.sleep(1)
monster = gamefunctions.new_random_monster()

print(f"\nHave a good day and watch out for the {monster['name']} on your way home!")

time.sleep(1)
print(".", end='', flush=True)
time.sleep(1)
print(".", end='', flush=True)
time.sleep(1)
print(".", end='', flush=True)
time.sleep(2)

# User encounters monster. Display stats and a message.
print(f"""\n**You've encountered the {monster['name']}!**""")

currentHP = 100
gamefunctions.displayFightStats(monster, currentMoney, currentHP)
gamefunctions.getUserFightOptions(True)
user_action = input("\nChoose your next action wisely. ")

#FIXME -- what if the user dies?
while user_action not in ['3','4']:
    fight_results = gamefunctions.fightScenarios(monster, currentHP, currentMoney, user_action)
    if 'input_invalid' in fight_results:
        user_action = input("Invalid option, please try again. ")
        continue
    monster['health'] = fight_results['monster_health']
    currentHP = fight_results['currentHP']
    currentMoney = fight_results['currentMoney']
    if monster['health'] <= 0:
        user_action = '4'
        break
    gamefunctions.displayFightStats(monster, currentMoney, currentHP)
    gamefunctions.getUserFightOptions(False)
    if currentHP <=25:
        print("\nWarning! HP at or below 25, sleep soon or run away!")
    user_action = input("\nChoose your next action... ")

# FIXME -- should I move the following code to gamefunctions?? idk
if user_action == "3":
    print("\nCoward. You ran away!")
elif user_action == "4":
    print(f"\nCongratulations! You have slain the {monster['name']}")
    currentMoney += monster['money']
    print(f"You now have ${currentMoney:.2f}")