#Kai Rebich - game.py
#10/15/2024 - CSCI 150
#This file is a simulation of a simple game using the
#functions imported from gamefunctions.py

import gamefunctions

user_name = input("What is your name? ")
gamefunctions.print_welcome(user_name)

print(f"\nI see you would like to purchase some apples, {user_name}! The price of each is listed on our menu below...")
gamefunctions.print_shop_menu("Apple", 0.99, "Strawberries", 2.99)

startingMoney = int(input("\nHow much money do you have? "))
quantityToPurchase = int(input("How many apples would you like to purchase? "))

transaction = gamefunctions.purchase_item(0.99, startingMoney, quantityToPurchase)

if transaction[2] == True:
    print(f"\nSorry, you can only afford {transaction[0]} apples. Here they are and your change of ${transaction[1]:.2f}")
else:
    print(f'\nAwesome, here are your {transaction[0]} apples and your change of ${transaction[1]:.2f}!')

monster = gamefunctions.new_random_monster()

print(f"\nHave a good day and watch out for the {monster['name']} on your way home!")
print(f"(You've encountered the {monster['name']} on your walk home. It is carrying ${monster['money']} and has {monster['health']} health points with a power rating of {monster['power']}.)")
print("(Choose your next action wisely)")
