"""Collection of functions created for CSCI-150 project.

The various functions include...
    purchase_item(): takes itemprice, startingmoney, and 
    quantityToPurchase and returns tuple containing information on
    transaction.

    new_random_monster(): takes no arguments and returns dictionary
    with a stats and description of a randomly generated monster.

    print_welcome(): takes name (and optional width argument) and outputs
    a centered welcome message.

    print_shop_menu(): takes name and price of two items and prints a 
    nicely formatted menu.

"""

### Kai Rebich
### 10/08/2024
### gamefunctions.py
### This file is a collection of various functions and project additions
### made throughout the course of CSCI 150

import random
import time

def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """ Returns a tuple containing the number of items purchased, 
    leftover money, and boolean notEnoughMoney indicating whether the user
    had enough money for the transaction.

    Parameters:
    itemPrice (float) -- represents price of the item
    startingMoney (float) -- represents the user's starting money
    quantityToPurchase (int) -- represents how many items are being 
    purchased. Defaults to 1.

    Returns: tuple (
        quantity_purchased (int),
        leftoverMoney (float),
        notEnoughMoney (boolean) -- true if cannot afford, false otherwise
    )

    Note: if attempting to buy more than user can afford, returns the max
    quantity they can afford.
    """

    if quantityToPurchase == 0:
        quantityToPurchase = 1

    # if attempting to purchase more items than you can afford:
    if (quantityToPurchase * itemPrice) > startingMoney: 
        quantity_purchased = startingMoney // itemPrice
        leftoverMoney = round((startingMoney % itemPrice), 2)
        notEnoughMoney = True
        return int(quantity_purchased), leftoverMoney, notEnoughMoney
    # otherwise good to go
    else:
        leftoverMoney = round((startingMoney - (quantityToPurchase * itemPrice)), 2)
        notEnoughMoney = False
        return int(quantityToPurchase), leftoverMoney, notEnoughMoney


def new_random_monster():
    """Returns a dictionary of a random monster with random health, power,
    and money attributes.

    Parameters: none

    Returns: dictionary {
    'name':(str)
    'health':(int)
    'power':(int)
    'money':(int)
    }
    """

    monster = {}
    # random number generator
    randomNumber = random.randint(1, 3) 

    if randomNumber == 1:
        monster['name'] = "goblin"
        monster['description'] = """This is a lone goblin. When it notices you,"
it rushes at you quickly with a dagger that could be mistaken for a butter knife."""
        monster['health'] = random.randint(5, 12)
        monster['power'] = random.randint(1, 5)
        monster['money'] = random.randint(1, 50)
    elif randomNumber == 2:
        monster['name'] = "dragon"
        monster['description'] = """You hear the terrible cry of a hungry dragon 
emerging from a nearby cave. Good luck."""
        monster['health'] = random.randint(5000, 20000)
        monster['power'] = random.randint(125, 250)
        monster['money'] = random.randint(3000, 12000)
    elif randomNumber == 3:
        monster['name'] = "frost troll"
        monster['description'] = """As you continue your quest to find treasure at
the top of a mountain with eternal blizzards you encounter 
a frost troll guarding a suspicious chest."""
        monster['health'] = random.randint(2000, 3000)
        monster['power'] = random.randint(50, 80)
        monster['money'] = random.randint(5000, 7000)
    return monster

def displayFightStats(monsterStats, currentMoney, currentHP=100):
    """ Prints a formatted summary of the current fight statistics between user and
    a monster. 

    Parameters:
        monsterStats (dict) {
            'name':(str)
            'money':(int)
            'health':(int)
            'power':(int)
        }
        currentMoney (int) - represents user's current money
        currentHP (int) - represents user's current health points
    
    Returns: None
    """
    currentMoney_output = f'{currentMoney:.2f}'
    currentMoney_output = str(currentMoney_output)
    print(f"""
{monsterStats['name'].title()+' Stats':-^25}{'Your Stats':-^25}
{'Money:':<7}{'$'+str(monsterStats['money']):>18} {'Money:':<7}{'$'+currentMoney_output:>18}
{'HP:':<7}{monsterStats['health']:>18} {'HP:':<7}{currentHP:>18}
{'Power:':<7}{monsterStats['power']:>18}
""")


def getUserFightOptions(startingFight):
    """FIXME add docstring
    """
    if startingFight == True:
        print("1) Fight Monster")
        print("2) Sleep (restore 10 HP for $5)")
        print("3) Quit (run away)")
        print("4) (Cheat) Instantly slay the monster")
    elif startingFight == False:
        print("1) Continue Fighting")
        print("2) Sleep (restore 10 HP for $5)")
        print("3) Quit (run away)")
        print("4) (Cheat) Instantly slay the monster")

def fightScenarios(monster, currentHP, currentMoney, user_action='0'): 
    """FIXME -- finish docstring
    Function holding the outputs and stuff from game.py  
    returns : monster health, currentHP, currentMoney, new user action  
    """
    scenario_results = {
        'currentHP': currentHP,
        'currentMoney': currentMoney,
        'monster_health': monster['health']
        }

    if user_action not in ['1','2']:
        scenario_results['input_invalid'] = True
        return scenario_results
    elif user_action == '1':
        print(f"\n**You chose to fight the {monster['name']}!**")
        time.sleep(1)
        if monster['health'] <= 5:
            damage_dealt = 5
        else:
            damage_dealt = random.randint(0, monster['health'])
        scenario_results['monster_health'] -= damage_dealt

        damage_received = random.randint(1, 25)
        scenario_results['currentHP'] -= damage_received
    elif user_action == '2':
        if currentMoney >= 5:
            print("\n**You chose to sleep and restored 10 HP!**")
            time.sleep(1)
            scenario_results['currentHP'] += 10
            scenario_results['currentMoney'] -= 5
            time.sleep(1)
        else:
            print("\n**You don't have enough money to do that.**")
            time.sleep(1)
    return scenario_results

def print_welcome(name="friend", width=20):
    """Prints a centered welcome message
    Parameters:
    name (str) -- string representing the person being welcomed
    
    Optional keyword parameter:
    width (int) -- defaults to 20, represents width of output string

    Returns: None
    """
    welcome = f'Hello {name}!'
    print(f'{welcome:^{width}}')

def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """Prints a nicely formatted shop menu with 2 items and 
    respective prices.

    Parameters, in order:
    item1Name (str) -- represents item 1's name
    item1Price (int or float) -- represents item 2's price
    item2Name (str) -- represents item 2's name
    item2Price (int or float) -- represents item 2's price

    Returns: None
    """
    border_dashes = "-" * 22
    item1Price = f'${item1Price:.2f}'
    item2Price = f'${item2Price:.2f}'
    print(f'/{border_dashes}\\')
    print(f'| {item1Name:<12}{item1Price:>8} |')
    print(f'| {item2Name:<12}{item2Price:>8} |')
    print(f'\\{border_dashes}/')

    
def test_functions():
    """test code to run if __name__ == __main__, each function runs 3x min
    
    Parameters: none

    Returns: None

    FIXME -- add test code for fightScenarios, getUserFightOptions and
    displayFightStatistics
    """

    # should return 2 items purchased and $4.20 change returned
    print(purchase_item(2.90, 10.0, 2))
    # should return 3 items purchased b/c 5 can't be afforded
    print(purchase_item(2.99, 10.0, 5))
    # should return 1 item purchased b/c default quantityToPurchase is 1
    print(purchase_item(5.99, 10.0)) 
    # should return 1 again, b/c default quantityToPurchase is 1
    print(purchase_item(5.99, 10.0, 0))

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


if __name__ == "__main__":
    test_functions()
