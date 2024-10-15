import gamefunctions

user_name = input("What is your name? ")
gamefunctions.print_welcome(user_name)

print(f"\nI see you would like to purchase some apples, {user_name}! The price of each is listed on our menu below...")
gamefunctions.print_shop_menu("Apple", 0.99, "Strawberries", 2.99)

startingMoney = int(input("\nHow much money do you have? "))
quantityToPurchase = int(input("How many apples would you like to purchase? "))

transaction = gamefunctions.purchase_item(0.99, startingMoney, quantityToPurchase)

print(f'Awesome, here are your {transaction[0]} apples and your change of ${transaction[1]:.2f}!')

