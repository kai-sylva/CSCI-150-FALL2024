#Kai Rebich - game.py
#10/15/2024 - CSCI 150
#This file is a simulation of a simple game using the
#functions imported from gamefunctions.py

import gamefunctions
import time

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
startingMoney = int(input("How much money do you have? "))

transaction = gamefunctions.purchase_item(itemPrice, startingMoney, quantityToPurchase)

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
print(f"""\n**You've encountered the {monster['name']}!**

{'Stats':-^25}
{'Money:':<7}{'$'+str(monster['money']):>18} 
{'Health:':<7}{monster['health']:>18} 
{'Power:':<7}{monster['power']:>18}
""")
print("**Choose your next action wisely**")
