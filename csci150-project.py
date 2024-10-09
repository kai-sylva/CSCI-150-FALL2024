### Kai Rebich
### 10/08/2024
### gamefunctions.py // will be CSCI150-project
### This file is a collection of various functions and project additions
### made throughout the course of CSCI 150

import random

def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """ Returns a tuple containing the number of items purchased and leftover money.
    Arguments:
    itemPrice -- float representing the price of the item
    startingMoney -- float representing the user's starting money
    quantityToPurchase -- integer representing how many items are being purchased. Defaults to 1.

    If user attempts to buy more items than they can afford, returns only what can be afforded.
    """

    if quantityToPurchase == 0:
        quantityToPurchase = 1

    # if attempting to purchase more items than you can afford:
    if (quantityToPurchase * itemPrice) > startingMoney: 
        quantity_purchased = startingMoney // itemPrice
        leftoverMoney = round((startingMoney % itemPrice), 2)
        return int(quantity_purchased), leftoverMoney
    # otherwise good to go
    else:
        leftoverMoney = round((startingMoney - (quantityToPurchase * itemPrice)), 2)
        return int(quantityToPurchase), leftoverMoney


def new_random_monster():
    """Returns a dictionary of a random monster with random health, power, and money attributes."""

    monster = {}
    # random number generator
    randomNumber = random.randint(1, 3) 

    if randomNumber == 1:
        monster['name'] = "A goblin"
        monster['description'] = "This is a lone goblin. When it notices you, it rushes at you quickly with a dagger that could be mistaken for a butter knife."
        monster['health'] = random.randint(5, 12)
        monster['power'] = random.randint(1, 5)
        monster['money'] = random.randint(1, 50)
    elif randomNumber == 2:
        monster['name'] = "A dragon"
        monster['description'] = "You hear the terrible cry of a hungry dragon emerging from a nearby cave. Good luck."
        monster['health'] = random.randint(5000, 20000)
        monster['power'] = random.randint(125, 250)
        monster['money'] = random.randint(3000, 12000)
    elif randomNumber == 3:
        monster['name'] = "A frost troll"
        monster['description'] = "As you continue your quest to find treasure at the top of a mountain with eternal blizzards you encounter a frost troll guarding a suspicious chest."
        monster['health'] = random.randint(2000, 3000)
        monster['power'] = random.randint(50, 80)
        monster['money'] = random.randint(5000, 7000)
    return monster

def print_welcome(name="friend", width=20):
    """Prints a centered welcome message
    Arguments:
    name -- string representing the person being welcomed
    
    Optional keyword arguments:
    width -- integer defaulting to 20, represents width of output string
    """
    welcome = f'Hello {name}!'
    print(f'{welcome:^{width}}')

def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """Prints a nicely formatted shop menu with 2 items and respective prices.
    Arguments, in order:
    item1Name -- string representing item 1's name
    item1Price -- integer or float representing item 2's price
    item2Name -- string representing item 2's name
    item2Price -- integer or float representing item 2's price
    """
    border_dashes = "-" * 22
    item1Price = f'${item1Price:.2f}'
    item2Price = f'${item2Price:.2f}'
    print(f'/{border_dashes}\\')
    print(f'| {item1Name:<12}{item1Price:>8} |')
    print(f'| {item2Name:<12}{item2Price:>8} |')
    print(f'\\{border_dashes}/')

    


# testing purchase_item() function
print(purchase_item(2.90, 10.0, 2)) # should return 2 items purchased and $4.20 change returned
print(purchase_item(2.99, 10.0, 5)) # should return 3 items purchased b/c 5 can't be afforded
print(purchase_item(5.99, 10.0)) # should return 1 item purchased b/c default quantityToPurchase is 1
print(purchase_item(5.99, 10.0, 0)) # should return 1 again, b/c default quantityToPurchase is 1

# testing new_random_monster() function
my_monster1 = new_random_monster()
my_monster2 = new_random_monster()
my_monster3 = new_random_monster()
print(f"Monster 1: {my_monster1['name']}, Power: {my_monster1['power']}, Description: {my_monster1['description']}")
print(f"Monster 2: {my_monster2['name']}, Power: {my_monster2['power']}, Money: {my_monster2['money']}")
print(f"Monster 3: {my_monster3['name']}, Power: {my_monster3['power']}, Health: {my_monster3['health']}")

#testing print_welcome() -- one test for no input
print_welcome("kai")
print_welcome("Gary")
print_welcome()

print_shop_menu("Apple", 1000, "Banana", 2)
print_shop_menu("Sourdough", 5.99, "Flour", 6.4)
print_shop_menu("Tomato", 1.99, "Ketchup", 17)

print("testing change to file in remote repository")
