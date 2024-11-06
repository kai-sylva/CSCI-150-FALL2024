"""Collection of functions created for CSCI-150 project.

The various functions include...
    getUserGameOptions(): Prints a menu of game options for user to choose from.
    Main navigation for the game loop, 'q' to quit.

    purchase_item(): takes itemprice, startingmoney, and 
    quantityToPurchase and returns tuple containing information on
    transaction.

    new_random_monster(): takes no arguments and returns dictionary
    with a stats and description of a randomly generated monster.

    fightMonster(): Takes user stats and monster stats and allows user to attack
    the monster, drink health potions, run away, or cheat and instantly slay 
    the monster.

    attackMonster(): Generates random damage values (both dealt and received)
    and adjusts user stats and monster stats accordingly. User can cheat or
    instantly slay monster to acquire its gold. Takes user stats, monster stats,
    and cheat boolean as parameters.

    equipWeapon(): Allows user to equip a weapon from their inventory.

    getUserFightOptions(): Prints a list of options for user to choose from when 
    fighting a monster.

    displayFightStats(): Prints a formatted summary of the current fight 
    statistics between user and a monster. 

    drinkHealthPotion(): Takes user's stats from a dictionary and adds 75 HP
    if user possesses at least 1 health potion in their inventory.

    print_welcome(): takes name (and optional width argument) and outputs
    a centered welcome message.

    print_shop_menu(): takes dictionary of shop items (keys) and prices (values)
    and prints a formatted menu.

    getUserStats(): Prints formatted menu of current player stats.

    buyShopItems(): Takes user's stats, inventory, and dictionary of shop items 
    and allows user to purchase items from the shop.

    addToInventory(): Adds an item to the user's inventory. If an item requires 
    a new itemId, calls the createItemId() function.

    createItemId(): Gathers a list of all the item IDs in user's inventory and 
    returns a unique item ID (not found in inventory) between 10 and 999.

    repairWeapon(): Allows user to repair a weapon with a durability less than 
    its max durability. Costs 25 gold to increase a weapon's durability by 1.

    sleep(): User "sleeps" and restores 10 HP. Can be used as a way to restore
    HP when user has no health potions or money to buy health potions. 
    Can only be done outside of a fight.

    loadFromSave(): Opens user_stats.json and user_inventory.json and grabs user
    data, returns as python objects.

    checkSaveExists(): Checks if the correct save files for game.py exist in the 
    same path as game.py. The files are user_stats.json and user_inventory.json.

    saveGame(): Saves user's stats and inventory to respective json files in the
    directory they are playing game.py in.

    newGame(): Creates and returns default user stats and inventory. Takes input
    on user's name.

"""

### Kai Rebich
### 11/6/2024
### gamefunctions.py
### This file is a collection of various functions and project additions
### made throughout the course of CSCI 150

import random
from copy import deepcopy
import json
import os

def getUserGameOptions():
    """Loops through a list of game options to prints a simple menu of 
    game options to the user. 

    Parameters: none

    Returns: 
        options (list): List of all options (if needed for verifyInput()
        or other uses)
    """

    game_options = [
        'Enter shop',
        'Fight monster',
        'Equip weapon',
        'Sleep (Restore 10HP)',
        'Drink Health Potion (Restore 75 HP)',
        'Display stats',
        'Display inventory',
        'Repair weapon (costs 25 gold)',
        'Quit game'
    ]

    option_number = 1
    options = ['q', 'cheat gold']

    for option in range(len(game_options)):
        if game_options[option] == 'Quit game':
            print("q) Quit game")
        else:
            print(f"{option_number}) {game_options[option]}")
            options.append(str(option_number))
            option_number += 1
    return options

def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """ Returns a tuple containing the number of items purchased, 
    leftover money, and boolean notEnoughMoney indicating whether the user
    had enough money for the transaction.

    Parameters:
    itemPrice (int) -- represents price of the item
    startingMoney (int) -- represents the user's starting money
    quantityToPurchase (int) -- represents how many items are being 
    purchased. Defaults to 1.

    Returns: tuple (
        quantity_purchased (int),
        leftoverMoney (int),
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

def fightMonster(user_stats_dict, inventory, monster={}):
    """Takes user stats and monster stats and allows user to attack the monster,
    drink health potions, run away, or cheat and instantly slay the monster.
    THIS FUNCTION ALTERS ITS MUTABLE PARAMETERS.

    Parameters:
        user_stats_dict (dict): Dictionary containing user stats.
        inventory (list): List of nested dictionaries; each dictionary holds 
            information about an item in user's inventory.
        monster (dict): Dictionary containing monster stats. If no value is
            passed, a random monster is generated.
    
    Returns: None

    Special Notes:
        User Actions:
            1) "Attack": User attacks monster, dealing damage and receiving
            damage. Calls attackMonster() function.
            2) "Equip weapon": Allows user to equip a weapon from their
                inventory. Calls equipWeapon() function.
            3) "Drink health potion": User drinks health potion (calls
            drinkHealthPotion() function) and restores 75 HP.
            4) "Run Away": User runs away and abandons fight.
            5) "Instakill": Allows user to instantly slay monster if they 
                have at least one instakill spell in their inventory.
            cheat) "Instantly slay monster": User slays monster for free. Not
                advertised to user.

            If or when user slays monster, they are rewarded the monster's
            stash of gold.
    """
    # if monster stats not passed in, create new random monster
    if len(monster) == 0:
        monster = new_random_monster()
    print(f"You've encountered a {monster['name']}!")
    displayFightStats(user_stats_dict, monster)

    quit_fight = False
    while quit_fight == False:
        getUserFightOptions(monster)
        user_action = input("Choose your action: ")
        print("")
        if user_action == '1':
            quit_fight = attackMonster(user_stats_dict, inventory, monster)
        elif user_action == '2':
            equipWeapon(user_stats_dict, inventory)
            displayFightStats(user_stats_dict, monster)
        elif user_action == '3':
            drinkHealthPotion(user_stats_dict, inventory)
            displayFightStats(user_stats_dict, monster)
        elif user_action == '4':
            print("You ran away!")
            getUserStats(user_stats_dict)
            quit_fight = True
        elif user_action == '5':
            quit_fight = attackMonster(user_stats_dict, inventory, monster, instakill=True)
        elif user_action == 'cheat':
            quit_fight = attackMonster(user_stats_dict, inventory, monster, cheat=True)
        else:
            print("Invalid option, please try again.")

def attackMonster(user_stats_dict, inventory, monster, cheat=False, instakill=False):
    """User attacks monster, dealing damage to the monster's HP equal to the 
        user's attack power. Attack power is a combination of the user's base 
        power and weapon power IF their equipped weapon is not broken. Monster 
        also deals a random amount of damage between 1 and 25. If monster HP
        falls to 0, user is congratulated and awarded monster's gold. If user HP
        falls to 0, user is forced to abandon the fight.
    THIS FUNCTION ALTERS ITS MUTABLE PARAMETERS.

    Parameters:
        user_stats_dict (dict) - Dictionary containing user stats
        inventory (list): List of nested dictionaries; each dictionary holds 
            information about an item in user's inventory.
        monster (dict) - Dictionary containing monster stats
        cheat (bool) - Default is False and function proceeds normally. If True,
            the user slays the monster for free and acquires its gold, taking no
            damage.
        instakill (bool) - Default is false and function proceeds normally. If 
            True, checks that user has at least 1 instakill spell. If they do,
            consumes instakill spell and user slays monster and takes 0 damage.
    
    Returns: 'True' if user HP or monster HP falls to 0, 'False' if otherwise.
    """

    if instakill == True:
        for item in inventory:
            if item['name'] == 'instakill':
                if item['quantity'] < 1:
                    print("You have no more instakill spells remaining.")
                    displayFightStats(user_stats_dict, monster)
                    return False
                else:
                    item['quantity'] -= 1
                    print(f"You have slain the {monster['name']} with an instakill spell!")
                    print(f"Gold acquired: {monster['money']}")
                    user_stats_dict['currentMoney'] += monster['money']
                    getUserStats(user_stats_dict)
                    return True
            else:
                continue
        print("You have no instakill spells.")
        displayFightStats(user_stats_dict, monster)
        return False
    elif cheat == True:
        print(f"You have slain the {monster['name']}!")
        print(f"Gold acquired: {monster['money']}")
        user_stats_dict['currentMoney'] += monster['money']
        getUserStats(user_stats_dict)
        return True
    elif cheat == False:
        print("You chose to fight!\n")

        attack_power = user_stats_dict['attack_power']

        if monster['health'] <= attack_power:
            damage_dealt = monster['health']
        else:
            damage_dealt = attack_power
        monster['health'] -= damage_dealt
        
        for item in inventory:
            if item['itemId'] == user_stats_dict['weapon_id']:
                # weapon_ref is only used to reference weapon's durability
                weapon_ref = item
                if item['durability'] > 1:
                    item['durability'] -= 1
                elif item['durability'] == 1:
                    item['durability'] -= 1
                    user_stats_dict['attack_power'] -= item['attack power']
                    user_stats_dict['weapon_power'] = 0
                    attack_power = user_stats_dict['attack_power']
                    print(f"{item['name'].title()} broke! Attack power has fallen to {attack_power}")

        damage_received = random.randint(1, 25)
        if user_stats_dict['currentHP'] <= damage_received:
            damage_received = user_stats_dict['currentHP']
            user_stats_dict['currentHP'] -= damage_received
        else:
            user_stats_dict['currentHP'] -= damage_received
        print(f"Damage dealt: {damage_dealt}")
        print(f"Damage Received: {damage_received}")
        if user_stats_dict['equipped_weapon'] != 'None':
            print(f"{weapon_ref['name'].title()} durability: {weapon_ref['durability']}")
        print()
        displayFightStats(user_stats_dict, monster)

        if monster['health'] == 0:
            print(f"You have slain the {monster['name']}!")
            print(f"Gold acquired: {monster['money']}")
            user_stats_dict['currentMoney'] += monster['money']
            getUserStats(user_stats_dict)
            return True
        elif user_stats_dict['currentHP'] == 0:
            print("Your HP has fallen to 0 and you have been defeated.")
            print("You must run away and sleep to regenerate health.\n")
            return True
        else:
            return False

def equipWeapon(user_stats_dict, inventory):
    """Allows user to equip a weapon from their inventory.
    THIS FUNCTION ALTERS ITS MUTABLE PARAMETERS

    Parameters:
        user_stats_dict (dict) - Dictionary containing user stats
        inventory (list): List of nested dictionaries; each dictionary holds 
            information about an item in user's inventory.
    
    Returns: None

    """

    # Grab list of weapons and IDs
    weapon_list = []
    weapon_ids = []
    for item in inventory:
        if item['type'] == 'weapon':
            weapon_list.append(item)
            weapon_ids.append(item['itemId'])

    if len(weapon_list) == 0:
        print("\nYou have no weapons to equip\n")
        return None
    
    print(f"\nCurrently equipped: {user_stats_dict['equipped_weapon']}\n")

    # Show available weapons to equip
    getUserInventory(weapon_list, "Weapons")

    quit_equip = False
    while quit_equip == False:
        user_action = input("What would you like to equip?(enter itemId or 'q' for quit) ")

        if user_action == 'q':
            quit_equip = True
        elif user_action in weapon_ids:
            # Remove currently equipped weapon and update weapon in inventory
            if user_stats_dict['equipped_weapon'] != 'None':
                user_stats_dict['attack_power'] -= user_stats_dict['weapon_power']
                user_stats_dict['weapon_power'] = 0
                user_stats_dict['weapon_id'] = 'None'
                user_stats_dict['equipped_weapon'] = 'None'
                for item in inventory:
                    if item['equipped'] == True:
                        item['equipped'] = False
                        print(f"\n{item['name']} (ID: {item['itemId']}) unequipped.")
            # Find weapon and equip, updating user stats and weapon details
            for item in inventory:
                if item['itemId'] == user_action:
                    # If item is broken, allow user option to continue equipping
                    if item['durability'] <= 0:
                        print("\nYou may equip this weapon, but it is broken and won't")
                        print("increase your overall damage.")

                        quit_equipBroken = False
                        while quit_equipBroken == False:
                            equipBroken = input("Would you like to continue?(y/n) ")
                            if equipBroken == 'n':
                                quit_equipBroken = True
                            # Equip broken weapon
                            elif equipBroken == 'y':
                                item['equipped'] = True
                                user_stats_dict['equipped_weapon'] = item['name']
                                user_stats_dict['weapon_id'] = item['itemId']
                                print(f"\n{item['name'].title()} successfully equipped!")
                                print(f"Durability: {item['durability']}")
                                print(f"Total attack power: {user_stats_dict['attack_power']}\n")
                                quit_equipBroken = True
                                quit_equip = True
                            else:
                                print("Invalid option, please try again")
                    # Equip chosen weapon, update user power and weapon status
                    else:
                        user_stats_dict['attack_power'] += item['attack power']
                        item['equipped'] = True
                        user_stats_dict['equipped_weapon'] = item['name']
                        user_stats_dict['weapon_power'] = item['attack power']
                        user_stats_dict['weapon_id'] = item['itemId']
                        
                        print(f"\n{item['name'].title()} successfully equipped!")
                        print(f"Durability: {item['durability']}")
                        print(f"Total attack power: {user_stats_dict['attack_power']}\n")
                        quit_equip = True
        elif user_action not in weapon_ids:
            print("Invalid option, please try again\n")

def getUserFightOptions(monster):
    """Prints a list of options for user to choose from when fighting a monster.
    Mutable parameters are NOT altered.

    Parameters: 
        monster (dict): Dictionary contianing monster stats.

    Returns: None
    """
    print("1) Attack")
    print("2) Equip weapon")
    print(f"3) Drink health potion")
    print("4) Run away")
    print(f"5) Instakill the {monster['name']}")

def displayFightStats(user_stats_dict, monster):
    """Prints a formatted summary of the current fight statistics between user and
    a monster. Mutable parameters are NOT altered.

    Parameters:
        user_stats_dict (dict): Dictionary containing user stats
        monster (dict): Dictionary containing monster stats
    
    Returns: None
    """

    # FIXME (@ later date) -- fix readability
    print(f"""
{monster['name'].title()+' Stats':-^25} {'Your Stats':-^25}
{'Gold:':<7}{str(monster['money']):>18} {'Gold:':<7}{user_stats_dict['currentMoney']:>18}
{'HP:':<7}{monster['health']:>18} {'HP:':<7}{user_stats_dict['currentHP']:>18}
{'Power:':<7}{monster['power']:>18} {'Equipped Weapon: ':<12}{user_stats_dict['equipped_weapon']:>8}
{' '*25} {'Attack Power: ':<12}{user_stats_dict['attack_power']:>11}
""")

def drinkHealthPotion(user_stats_dict, inventory):
    """Allows user to consume a health potion from their inventory, grants 75 HP
    THIS FUNCTION ALTERS ITS MUTABLE PARAMETERS

    Parameters:
        user_stats_dict (dict) - Dictionary containing user stats
        inventory (list): List of nested dictionaries; each dictionary holds 
            information about an item in user's inventory.
    
    Returns: None

    """

    for item in inventory:
        if item['name'] != 'health potion':
            continue
        else:
            if item['quantity'] > 0:
                item['quantity'] -= 1
                user_stats_dict['currentHP'] += 75
                print(f"\n75 HP Restored!")
                print(f"Current HP: {user_stats_dict['currentHP']}")
                print(f"Health potions remaining: {item['quantity']}\n")
            else:
                print("No health potions remaining")

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

def loadFromSave():
    """Opens user_stats.json and user_inventory.json and grabs user data, returns
    as python objects.
    
    Parameters: None

    Returns:
        user_stats (dict): Dictionary containing user stats.
        inventory (list): List of inventory items.
    """
    with open("user_stats.json", 'r') as file:
        user_stats = json.load(file)
    with open("user_inventory.json", 'r') as file:
        inventory = json.load(file)
    return user_stats, inventory

def checkSaveExists():
    """Checks if the correct save files for game.py exist in the same path
    as game.py. The files are user_stats.json and user_inventory.json. If 
    the files exist, takes input on whether user wants to start game from
    the save files.
    
    Parameters: None

    Returns: True if the files exist and user wants to start from those files, 
    False if they don't exist or user chooses to not load from those files.
    
    """
    if not os.path.exists("user_stats.json") and not os.path.exists("user_inventory.json"):
        print("Starting from new game.\n")
        return False
    else:
        print("1) Start from new game")
        print("2) Start from save file")

        msg = "What would you like to do? "
        user_input = verifyInput(msg, ['1', '2'])
        if user_input == '1':
            return False
        elif user_input == '2':
            return True
        else:
            print("Invalid option, please try again.")

def saveGame(user_stats, inventory):
    """Saves user's stats and inventory to respective json files in the
    directory they are playing game.py in.
    
    Parameters: None

    Returns: None
    
    """
    with open("user_stats.json", 'w') as file:
        json.dump(user_stats, file, indent=4)
    with open("user_inventory.json", 'w') as file:
        json.dump(inventory, file, indent=4)

def newGame():
    """Creates and returns default user stats and inventory. Takes input on 
    user's name.
    
    Parameters: None

    Retrns:
        user_stats (dict): Dictionary containing user's stats.
        inventory (list): List containing default inventory, which is one
        health potion.
    """

    # Get user's name, print welcome
    user_name = input("What is your name? ")
    print()
    print_welcome(user_name, width=0)

    # Initial inventory
    inventory = [
        {'name': 'health potion', 'price': 50, 'quantity': 1, 'type': 'potion', 
        'equipped': False, 'itemId': '1'}
    ]


    # Initial user stats
    user_stats = {
        'user_name': user_name,
        'currentHP': 100,
        'currentMoney': 250,
        'attack_power': 20,
        'equipped_weapon': 'None',
        'weapon_power': 0,
        'weapon_id': 'None'
    }

    return user_stats, inventory

def print_shop_menu(shop_items_dict):
    #FIXME -- allow item names longer than 15 characters
    """Takes a dictionary of shop items and prints a nicely formatted shop menu 
    with item names and respective prices. 
    Mutable parameters are NOT altered.

    Parameters:
        shop_items_dict (dict): Dictionary containing shop items (keys) and
        item prices (values)

    Returns: None

    Notes:
        Item names are currently limited to 15 characters. Providing more than
        15 characters will break the menu formatting.
    """
    border_dashes = "-" * 25
    print(f'/{border_dashes}\\')
    print(f'{"| Item":<15}{"Price":>10} |')
    print(f'|{border_dashes}|')
    for item, details in shop_items_dict.items():
        print(f"| {item.title():<15}{details['price']:>8} |")
    print(f'\\{border_dashes}/')

def getUserStats(user_stats_dict):
    """Prints formatted menu of current player stats.
    Mutable parameters are NOT altered.

    Parameters:
        user_stats_dict (dict) -- dictionary containing various user stats
            ['user_name']: User's name
            ['currentHP']: User's current HP
            ['attack_power']: User's total attack power
            ['equipped_weapon']: User's currently equipped weapon.
            ['currentMoney']: User's current gold inventory
    
    Returns: None

    """
    print(f"""
{'Stats':-^25}
{'Name:':<7}{user_stats_dict['user_name']:>18}
{'HP:':<7}{user_stats_dict['currentHP']:>18}
{'Attack Power:':<15}{user_stats_dict['attack_power']:>10}
{'Equipped Weapon:':<15}{user_stats_dict['equipped_weapon']:>9}
{'Gold:':<7}{user_stats_dict['currentMoney']:>18}
""")
    
def getUserInventory(inventory, type_name="Type: Not Specified"):
    """Prints a formatted menu of user's inventory items. Type of item(s) should
    be specified.
    Mutable parameters are NOT altered.

    Parameters:
        inventory (list): List of nested dictionaries; each dictionary holds 
            information about an item in user's inventory.
        type_name (str): Type of inventory item(s) displayed.

    Returns: None
    """
    print()
    print(f'<->-<->-<->{type_name:}<->-<->-<->')
    for item in inventory:
        print(f"{item['name']:-^20}")
        for key, value in item.items():
            if key != 'name':
                print(f'{key}: {value}')
        print()

def buyShopItems(user_stats_dict, shop_items_dict, inventory):
    """Takes user stats, inventory, and shop items and prints a shop menu from 
    which the user can choose to buy an item. 
    THIS FUNCTION ALTERS ITS MUTABLE PARAMETERS.

    Parameters:
        user_stats_dict (dict): Dictionary containing user's stats.
        shop_items_dict (dict): Dictionary containing shop items (keys) and 
        prices (values).
        inventory (list): List of nested dictionaries; each dictionary holds 
            information about an item in user's inventory.
    
    Returns: None
    """

    # Welcome user and print shop menu with the items in shop_items_dict
    print(f"Hello, {user_stats_dict['user_name']}! Check out our current items!\n")
    print_shop_menu(shop_items_dict)
    # Display user's current gold inventory
    print(f"\nGold: {user_stats_dict['currentMoney']}")

    quit_interact = False
    while quit_interact == False:
        item = input("What would you like to buy?('q' to leave) ")
        if item == 'q':
            print("")
            quit_interact = True
        elif item not in shop_items_dict:
            print("Invalid option, please try again")
            continue
        elif item in shop_items_dict:
            # Get input on quantity to purchase
            quantityValid = False
            while quantityValid == False:
                quantityToPurchase = input(f'Quantity of {item} to purchase: ')
                if quantityToPurchase.isdigit():
                    quantityToPurchase = int(quantityToPurchase)
                    quantityValid = True
                else:
                    print("Invalid option, please try again\n")

            # Pass transaction info into purchase_item
            transaction = purchase_item(shop_items_dict[item]['price'], user_stats_dict['currentMoney'], quantityToPurchase)
            # Update user's remaining gold inventory
            user_stats_dict['currentMoney'] = transaction[1]
            purchased_item = shop_items_dict[item]

            if type(purchased_item['quantity']) == int:
                purchased_item['quantity'] = transaction[0]

            # Add purchased item to user's inventory
            addToInventory(purchased_item, inventory, transaction[0])
                    

            # Print receipt of transaction
            if transaction[2] == True:
                print(f"""\nOops, you can only afford {transaction[0]} {item}. 
\nQuantity purchased: {transaction[0]}
Remaining gold: {transaction[1]}""")
            else:
                print(f"""\nQuantity purchased: {transaction[0]}
Remaining gold: {transaction[1]}""")
                
def addToInventory(item, inventory, quantity):
    """Adds an item to the user's inventory. If an item requires a new itemId,
    calls the createItemId() function.
    THIS FUNCTION ALTERS ITS MUTABLE PARAMETERS

    Parameters:
        item (dict): Dictionary containing details about an item.
        inventory (list): List of nested dictionaries; each dictionary holds 
            information about an item in user's inventory.
        quantity (int): Quantity of item to add to inventory. **READ NOTES**

    Returns: None

    Notes: The quantity parameter is currently only used for items that have a 
        quantity value of 'single'. It is NOT used for items whose quantity
        values are integers, such as health potions and instakill spells.
        The reason for this is to distinguish between items which may need to 
        have attributes altered other than the quantity key (ex. weapon 
        durability). 
    """
    # Inventory will typically default to having health potions at start, but
    # just in case the inventory is empty...
    if len(inventory) == 0:
        if item['quantity'] == 'single':
            for _ in range(quantity):
                itemId = createItemId(inventory)
                newitem = deepcopy(item)
                newitem['itemId'] = itemId
                inventory.append(newitem)
        else:
            itemId = createItemId(inventory)
            newitem = deepcopy(item)
            newitem['itemId'] = itemId
            inventory.append(newitem)

    else:
        # Check if item exists in inventory
        for inv_item in inventory:
            if inv_item['name'] == item['name']:
                # if item does not "stack" (ex. swords)
                if item['quantity'] == 'single':
                    for _ in range(quantity):
                        itemId = createItemId(inventory)
                        newitem = deepcopy(item)
                        newitem['itemId'] = itemId
                        inventory.append(newitem)
                    return None
                else:
                    newitem = deepcopy(inv_item)
                    inventory.remove(inv_item)
                    newitem['quantity'] += item['quantity']
                    inventory.append(newitem)
                    return None
            else:
                continue
        
        # If item does not exist in inventory, add to inventory
        if item['quantity'] == 'single':
            for _ in range(quantity):
                itemId = createItemId(inventory)
                newitem = deepcopy(item)
                newitem['itemId'] = itemId
                inventory.append(newitem)
            return None
        else:
            itemId = createItemId(inventory)
            newitem = deepcopy(item)
            newitem['itemId'] = itemId
            inventory.append(newitem)
            return None

def createItemId(inventory):
    """Gathers a list of all the item IDs in user's inventory and returns a
    unique item ID (not found in inventory) between 10 and 999.
    This function does NOT alter its mutable parameters.

    Parameters:
        inventory (list): List of nested dictionaries; each dictionary holds 
            information about an item in user's inventory.
    
    Returns: itemId (str): item ID between numbers 10-999. 
    """
    id_list = []

    if len(inventory) == 0:
        itemId = str(random.randint(10, 999))
    # If items exist in inventory, append all IDs to id_list
    else:
        for inv_item in inventory:
            inv_id = inv_item['itemId']
            id_list.append(inv_id)

        itemId = str(random.randint(10, 999))
        # Keep generating IDs until a unique ID is found.
        # FIXME (@ later date) -- Infinite loop if inventory is 'full'; idk how
        # to fix if I want to allow a seemingly infinite inventory.
        while itemId in id_list:
            itemId = str(random.randint(10, 999))
        
    return itemId

def repairWeapon(user_stats_dict, inventory):
    """Allows user to repair a weapon with a durability less than its max
    durability. Costs 25 gold to increase a weapon's durability by 1.

    Parameters:
        user_stats_dict (dict) - Dictionary containing user stats
        inventory (list): List of nested dictionaries; each dictionary holds 
            information about an item in user's inventory.
    
    Returns: None

    """
    # Grab a list of weapons and list of weapon IDs
    weapon_list = []
    # 'q' is needed when being passed into verifyInput(), not a real itemId
    weapon_ids = ['q']
    for item in inventory:
        if item['type'] == 'weapon' and item['durability'] < item['max durability']:
            weapon_list.append(item)
            weapon_ids.append(item['itemId'])

    quit_repair = False
    while quit_repair == False:
        # Basic checks to see if user can repair any weapons
        if len(weapon_list) == 0:
            print("You have no weapons to repair\n")
            return None
        if user_stats_dict['currentMoney'] < 25:
            print(f"You don't have enough gold.\n")
            return None
        # Show weapons in inventory as well as current gold
        getUserInventory(weapon_list, type_name="Weapons")
        print(f"Gold: {user_stats_dict['currentMoney']}")

        msg = "Which weapon would you like to repair?(enter itemId or 'q' to quit) "
        user_action = verifyInput(msg, weapon_ids)

        if user_action == 'q':
            quit_repair = True
        else:
            for item in inventory:
                if user_action == item['itemId']:
                    max_repair = item['max durability'] - item['durability']
                    # If user has enough money for full repair give them option
                    if user_stats_dict['currentMoney'] >= max_repair * 25:
                        msg = "Would you like to repair to max durability?(y/n) "
                        repairToMax = verifyInput(msg, ['y', 'n'])
                    else:
                        repairToMax = 'n'
                    
                    if repairToMax == 'y':
                        item['durability'] = item['max durability']
                        user_stats_dict['currentMoney'] -= max_repair * 25
                        print(f"{item['name'].title()} successfully repaired!")
                        weapon_list.remove(item)
                        weapon_ids.remove(item['itemId'])
                        continue
                    elif repairToMax == 'n':
                        item['durability'] += 1
                        user_stats_dict['currentMoney'] -= 25
                        print(f"{item['name'].title()} successfully repaired!")
                        if item['durability'] == item['max durability']:
                            weapon_list.remove(item)
                            weapon_ids.remove(item['itemId'])
                            continue

def verifyInput(msg, options):
    """Function to check for valid input.
    
    Parameters:
        msg (str): The message to be displayed to the user, prompting input.
        options (list): List of options to check user input against.
    
    Returns: 
        user_input (str): User's input if it matches an option
    
    """
    validInput = False
    while validInput == False:
        user_input = input(msg)
        if user_input in options:
            validInput = True
            return user_input
        else:
            print("Invalid option, please try again\n")

def sleep(user_stats_dict):
    """Takes user stats and adds 10 HP.
    THIS FUNCTION ALTERS ITS MUTABLE PARAMETERS.

    Parameters:
        user_stats_dict (dict): Dictionary containing user stats.
    
    Returns: None

    Notes:
        To curb player abusing sleep() while still allowing them to play if they
        are defeated during a fight and have no health potions, sleep() only
        restores 10 HP per instance. 
    """
    
    user_stats_dict['currentHP'] += 10
    print("\nYou chose to sleep and restore 10HP.")
    print(f"Current HP: {user_stats_dict['currentHP']}\n")
    
def test_functions():
    """test code to run if __name__ == __main__, each function runs 3x min
    
    Parameters: none

    Returns: None

    """

    user_stats = {
        'user_name': 'kai',
        'currentHP': 100,
        'currentMoney': 250,
        'attack_power': 20,
        'equipped_weapon': 'None',
        'weapon_power': 0,
        'weapon_id': 'None'
    }

    inventory = [
    {'name': 'health potion', 'price': 50, 'quantity': 1, 'type': 'potion', 
     'equipped': False, 'itemId': '1'}
    ]
    
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

    # Testing getUserGameOptions()
    getUserGameOptions()

    # Testing displayFightStats
    displayFightStats(user_stats, my_monster1)

    # Testing sleep()
    sleep(user_stats)

    # Testing drinkHealthPotion()
    drinkHealthPotion(user_stats, inventory)

    shop_items = {
        'health potion': {'price': 50, 'quantity': 1, 'type': 'potion', 
                        'name': 'health potion', 'equipped': False},
        'sword': {'price': 100, 'quantity': 'single', 'type': 'weapon', 'durability': 5, 
                'max durability': 10, 'attack power': 500, 'name': 'sword',
                'equipped': False},
        'instakill spell': {'price': 100, 'quantity': 1, 'type': 'spell',
                            'name': 'instakill', 'equipped': False}
    }
    print_shop_menu(shop_items)

    randomId = createItemId(inventory)
    print(f"\nThis is a random test ID: {randomId}")
    getUserStats(user_stats)
    buyShopItems(user_stats, shop_items, inventory)
    equipWeapon(user_stats, inventory)
    fightMonster(user_stats, inventory)
    repairWeapon(user_stats, inventory)

if __name__ == "__main__":
    test_functions()
