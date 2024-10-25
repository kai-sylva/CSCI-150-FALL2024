"""Collection of functions created for CSCI-150 project.

The various functions include...
    purchase_item(): takes itemprice, startingmoney, and 
    quantityToPurchase and returns tuple containing information on
    transaction.

    new_random_monster(): takes no arguments and returns dictionary
    with a stats and description of a randomly generated monster.

    fightMonster(): Takes user stats and monster stats and allows user to attack
    the monster, drink health potions, run away, or cheat and instantly slay 
    the monster.

    attackMonster(): Generates random damage values (both dealt and received)
    and adjusts user stats and monster stats accordingly. User can cheat and
    instantly slay monster to acquire its gold. Takes user stats, monster stats,
    and cheat boolean as parameters.

    displayFightStats(): Prints a formatted summary of the current fight 
    statistics between user anda monster. 

    drinkHealthPotion(): Takes user's stats from a dictionary and adds 75 HP
    if user possesses at least 1 health potion.

    print_welcome(): takes name (and optional width argument) and outputs
    a centered welcome message.

    print_shop_menu(): takes dictionary of shop items (keys) and prices (values)
    and prints a formatted menu.

    getUserStats(): Prints formatted menu of current player stats.

    buyShopItems(): Takes user's stats and dictionary of shop items and allows
    user to purchase items from the shop.

    sleep(): User "sleeps" and restores 10 HP. Can be used as a way to restore
    HP when user has no health potions or money to buy health potions. 
    Can only be done outside of a fight.

    getUserGameOptions(): Prints a menu of game options for user to choose from.
    Main navigation, 'q' to quit.

"""

### Kai Rebich
### 10/25/2024
### gamefunctions.py
### This file is a collection of various functions and project additions
### made throughout the course of CSCI 150

import random

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

def fightMonster(user_stats_dict, monster={}):
    """Takes user stats and monster stats and allows user to attack the monster,
    drink health potions, run away, or cheat and instantly slay the monster.
    THIS FUNCTION ALTERS ITS MUTABLE PARAMETERS.

    Parameters:
        user_stats_dict (dict): Dictionary containing user stats.
        monster (dict): Dictionary containing monster stats. If no value is
            passed, a random monster is generated.
    
    Returns: None

    Special Notes:
        User Actions:
            1) "Attack": User attacks monster, dealing damage and receiving
            damage. Calls attackMonster() function.
            2) "Drink health potion": User drinks health potion (calls
            drinkHealthPotion() function) and restores 75 HP.
            3) "Run Away": User runs away and abandons fight.
            4) "(Cheat) Instantly slay monster": User slays monster for free.

            If or when user slays monster, they are rewarded the monster's
            stash of gold.
        Parameters altered:
            user_stats_dict: ['currentHP'] ['health_potions'] ['currentMoney']
            monster: ['health']
    """
    # if monster stats not passed in, create new random monster
    if len(monster) == 0:
        monster = new_random_monster()
    print(f"You've encountered a {monster['name']}!")
    displayFightStats(user_stats_dict, monster)

    quit_fight = False
    while quit_fight == False:
        getUserFightOptions(user_stats_dict, monster)
        user_action = input("Choose your action: ")
        print("")
        if user_action == '1':
            quit_fight = attackMonster(user_stats_dict, monster)
        elif user_action == '2':
            drinkHealthPotion(user_stats_dict)
            displayFightStats(user_stats_dict, monster)
        elif user_action == '3':
            print("You ran away!")
            getUserStats(user_stats_dict)
            quit_fight = True
        elif user_action == '4':
            quit_fight = attackMonster(user_stats_dict, monster, cheat=True)
        else:
            print("Invalid option, please try again.")

def attackMonster(user_stats_dict, monster, cheat=False):
    """Generates random damage values that the user deals and receives and  
    updates user stats and monster stats to reflect damage dealt and received.
    If monster HP falls to 0, user is congratulated and awarded monster's gold. 
    If user HP falls to 0, user is forced to abandon the fight.
    THIS FUNCTION ALTERS ITS MUTABLE PARAMETERS.

    Parameters:
        user_stats_dict (dict) - Dictionary containing user stats
        monster (dict) - Dictionary containing monster stats
        cheat (bool) - Default is False and function proceeds normally. If True,
        the user slays the monster for free and acquires its gold, taking no
        damage.
    
    Returns: 'True' if user HP or monster HP falls to 0, 'False' if otherwise.
    """

    if cheat == True:
        print(f"You have slain the {monster['name']}!")
        print(f"Gold acquired: {monster['money']}")
        user_stats_dict['currentMoney'] += monster['money']
        getUserStats(user_stats_dict)
        return True
    elif cheat == False:
        print("You chose to fight!\n")

        # User deals max damage when monster's health at or below 5 HP
        if monster['health'] <= 5:
            damage_dealt = monster['health']
        else:
            damage_dealt = random.randint(1, monster['health'])
        monster['health'] -= damage_dealt

        damage_received = random.randint(1, 25)
        if user_stats_dict['currentHP'] <= damage_received:
            damage_received = user_stats_dict['currentHP']
            user_stats_dict['currentHP'] -= damage_received
        else:
            user_stats_dict['currentHP'] -= damage_received
        print(f"Damage dealt: {damage_dealt}")
        print(f"Damage Received: {damage_received}\n")
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

def getUserFightOptions(user_stats_dict, monster):
    """Prints a list of options for user to choose from when fighting a monster.
    Mutable parameters are NOT altered.

    Parameters: 
        user_stats_dict (dict): Dictionary containing user stats
        monster (dict): Dictionary contianing monster stats

    Returns: None
    """
    print("1) Attack")
    print(f"2) Drink health potion ({user_stats_dict['health_potions']} remaining)")
    print("3) Run away")
    print(f"4) (Cheat) Instantly slay the {monster['name']}")

def displayFightStats(user_stats_dict, monster):
    """Prints a formatted summary of the current fight statistics between user and
    a monster. Mutable parameters are NOT altered.

    Parameters:
        user_stats_dict (dict): Dictionary containing user stats
        monster (dict): Dictionary containing monster stats
    
    Returns: None
    """

    print(f"""
{monster['name'].title()+' Stats':-^25} {'Your Stats':-^25}
{'Gold:':<7}{str(monster['money']):>18} {'Gold:':<7}{user_stats_dict['currentMoney']:>18}
{'HP:':<7}{monster['health']:>18} {'HP:':<7}{user_stats_dict['currentHP']:>18}
{'Power:':<7}{monster['power']:>18}
""")

def drinkHealthPotion(user_stats_dict):
    """Takes user stats and checks for valid number of health potions. If user 
    has health potions, restores 75 HP and subtracts 1 health potion. 
    THIS FUNCTION ALTERS ITS MUTABLE PARAMETERS.

    Parameters:
        user_stats_dict (dict): Dictionary containing user stats.
    
    Returns: None
    """
    if user_stats_dict['health_potions'] > 0:
        user_stats_dict['health_potions'] -= 1
        user_stats_dict['currentHP'] += 75
        print(f"75 HP Restored!")
        print(f"Health potions remaining: {user_stats_dict['health_potions']}\n")
    else:
        print("No health potions remaining\n")

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

def print_shop_menu(shop_items_dict):
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
    for item, price in shop_items_dict.items():
        print(f'| {item.title():<15}{price:>8} |')
    print(f'\\{border_dashes}/')

def getUserStats(user_stats_dict):
    """Prints formatted menu of current player stats.
    Mutable parameters are NOT altered.

    Parameters:
        user_stats_dict (dict) -- dictionary containing various user stats
            ['user_name']: User's name
            ['currentHP']: User's current HP
            ['currentMoney']: User's current gold inventory
            ['health_potions']: User's current health potion inventory
    
    Returns: None

    """
    print(f"""
{'Stats':-^25}
{'Name:':<7}{user_stats_dict['user_name']:>18}
{'HP:':<7}{user_stats_dict['currentHP']:>18}
{'Gold:':<7}{user_stats_dict['currentMoney']:>18}
{'Health Potions:':<15}{user_stats_dict['health_potions']:>10}
""")

def buyShopItems(user_stats_dict, shop_items_dict):
    """Takes user stats and shop items and prints a shop menu from which the
    user can choose to buy an item. 
    THIS FUNCTION ALTERS ITS MUTABLE PARAMETERS.

    Parameters:
        user_stats_dict (dict): Dictionary containing user's stats.
        shop_items_dict (dict): Dictionary containing shop items (keys) and 
        prices (values).
    
    Returns: None

    Notes:
        This function currently only allows the health potions to be added to
        the user's inventory. Attempting to buy any other items will simply
        result in a donation to the shop.
    
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
            quantityToPurchase = int(input(f'Quantity of {item} to purchase: '))
            # Pass transaction info into purchase_item
            transaction = purchase_item(shop_items_dict[item], user_stats_dict['currentMoney'], quantityToPurchase)
            # Update user's remaining gold inventory
            user_stats_dict['currentMoney'] = transaction[1]

            # FIXME-(fix @ later date) allow more items to be added to inventory
            # Update user's health potion inventory (if purchased)
            if item == "health potion":
                user_stats_dict['health_potions'] += transaction[0]
            # Check if they had enough gold for quantityToPurchase and
            # print receipt of transaction
            if transaction[2] == True:
                print(f"""\nOops, you can only afford {transaction[0]} {item}. 
\nQuantity purchased: {transaction[0]}
Remaining gold: {transaction[1]}""")
            else:
                print(f"""\nQuantity purchased: {transaction[0]}
Remaining gold: {transaction[1]}""")
                
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

def getUserGameOptions():
    """Prints a simple menu of game options to the user. 

    Parameters: none

    Returns: None
    """
    print("1) Enter shop")
    print("2) Fight monster")
    print("3) Sleep (Restore 10HP)")
    print("4) Drink Health Potion (Restore 75 HP)")
    print("5) Display stats")
    print("q) Quit game")

    
def test_functions():
    """test code to run if __name__ == __main__, each function runs 3x min
    
    Parameters: none

    Returns: None

    """

    user_stats = {
        'user_name': 'kai',
        'currentHP': 100,
        'currentMoney': 250,
        'health_potions': 1
    }
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
    drinkHealthPotion(user_stats)

    shop_items_1 = {"Apple": 1000, "Banana": 2, "Raspberries": 4}
    shop_items_2 = {"Sourdough": 6, "Flour": 7}
    shop_items_3 = {"Tomato": 2, "Ketchup": 17}
    print_shop_menu(shop_items_1)
    print_shop_menu(shop_items_2)
    print_shop_menu(shop_items_3)

    getUserStats(user_stats)
    buyShopItems(user_stats, shop_items_1)
    fightMonster(user_stats)



if __name__ == "__main__":
    test_functions()
