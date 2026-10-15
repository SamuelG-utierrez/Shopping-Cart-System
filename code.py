from datetime import date  # import the date class from the datetime module

products = ["Chips", "Soda", "Candy", "Cookies", "Water", "Sandwich"]  # store inventory names
prices = [2.00, 2.50, 1.50, 3.00, 1.00, 5.00]  # prices share the same index as products
shopping_cart = []  # starts empty, holds each product name once
quantities = []  # starts empty, quantities[i] is how many of shopping_cart[i]


def show_menu():
    # prints the main menu
    print("\n========== SMART SHOPPING CART ==========")  # menu title
    print("""
1. View Available Products
2. Add Product to Cart
3. Remove Product from Cart
4. View Shopping Cart
5. View Current Total
6. Checkout""")  # menu options


def get_valid_number(prompt, low, high, error_message):
    # keeps asking until the user enters a whole number between low and high
    valid = False  # flag that controls the validation loop
    while valid == False:  # repeat until we get a good number
        choice = int(input(prompt))  # read the number from the user
        if choice < low or choice > high:  # check if it is out of range
            print(error_message)  # tell the user what went wrong
        else:
            valid = True  # good number, stop looping
    return choice  # send the valid number back to the caller


def display_products(products, prices):
    # shows every product with its price
    print("\n========== AVAILABLE PRODUCTS ==========")  # section title
    for i in range(len(products)):  # loop over every product
        print(f"{i + 1}. {products[i]:<10} ${prices[i]:.2f}")  # number, name, price


def add_product(products, prices, shopping_cart, quantities):
    # lets the user pick a product and adds it (or raises its quantity)
    print("Which product would you like to add?")  # ask the question
    display_products(products, prices)  # show the choices
    choice = get_valid_number("Enter product number: ", 1, len(products),
                              "Invalid product!\nPlease choose a number between 1 and " + str(len(products))) - 1  # validated index
    name = products[choice]  # name of the chosen product
    if name in shopping_cart:  # product is already in the cart
        position = shopping_cart.index(name)  # find where it sits in the cart
        quantities[position] += 1  # raise the quantity at the matching index
        print(name + " quantity increased to " + str(quantities[position]) + "!")  # confirm the new quantity
    else:  # product is not in the cart yet
        shopping_cart.append(name)  # add the name once
        quantities.append(1)  # matching quantity starts at 1
        print(name + " was added to your cart!")  # confirm to the user


def calculate_total_items(quantities):
    # adds up every quantity and returns how many items are in the cart
    count = 0  # running count of items
    for amount in quantities:  # loop over each quantity
        count += amount  # add it to the count
    return count  # send the count back


def display_cart(shopping_cart, quantities, products, prices):
    # shows each product with price, quantity, and line total
    print("\n========== YOUR SHOPPING CART ==========\n")  # section title
    print(f"   {'Product':<10} {'Price':>7} {'Quantity':>9} {'Total':>9}\n")  # column headers
    subtotal = 0  # running subtotal for the cart
    for i in range(len(shopping_cart)):  # loop over every cart entry
        price = prices[products.index(shopping_cart[i])]  # look up the price in the inventory
        line_total = price * quantities[i]  # price times quantity for this product
        subtotal += line_total  # add it to the subtotal
        print(f"{i + 1}. {shopping_cart[i]:<10} ${price:>6.2f} {quantities[i]:>9} ${line_total:>8.2f}")  # one row
    print("\nTotal Items: " + str(calculate_total_items(quantities)))  # items including quantities
    print(f"\nSubtotal: ${subtotal:.2f}")  # subtotal with two decimals


def remove_product(shopping_cart, quantities, products, prices):
    # lets the user remove one of a product from the cart
    if len(shopping_cart) == 0:  # nothing to remove
        print("Your shopping cart is empty!")  # tell the user
        print("There is nothing to remove.")  # explain
    else:
        display_cart(shopping_cart, quantities, products, prices)  # show the numbered cart
        print("\nWhich item would you like to remove?")  # ask the question
        remove = get_valid_number("Enter item number: ", 1, len(shopping_cart),
                                  "That item does not exist in your cart!") - 1  # validated index
        name = shopping_cart[remove]  # name of the chosen product
        if quantities[remove] > 1:  # more than one in the cart
            quantities[remove] -= 1  # just lower the quantity
            print("One " + name + " was removed!")  # confirm the removal
            print(name + " quantity is now " + str(quantities[remove]) + ".")  # show the new quantity
        else:  # only one left
            shopping_cart.pop(remove)  # remove the name from the cart
            quantities.pop(remove)  # remove the matching quantity so the lists stay in sync
            print(name + " was removed from your cart!")  # confirm the removal


def calculate_total(shopping_cart, quantities, products, prices):
    # returns the cart subtotal, counting each product's quantity
    total = 0  # running total
    for i in range(len(shopping_cart)):  # loop over every cart entry
        total += prices[products.index(shopping_cart[i])] * quantities[i]  # price times quantity
    return total  # send the total back


def display_total(shopping_cart, quantities, products, prices):
    # shows each product's line total and the current subtotal
    print("\n========== CURRENT TOTAL ==========\n")  # section title
    for i in range(len(shopping_cart)):  # loop over every cart entry
        price = prices[products.index(shopping_cart[i])]  # look up the price
        print(f"{shopping_cart[i]:<10} {quantities[i]} x ${price:.2f} = ${price * quantities[i]:.2f}")  # name, math, line total
    total = calculate_total(shopping_cart, quantities, products, prices)  # get the subtotal
    print(f"\nSubtotal:  ${total:.2f}")  # show it with two decimals


def calculate_discount(subtotal):
    # returns the discount percent for a given subtotal
    if subtotal >= 40:  # $40 or more
        discount = 15  # 15% off
    elif subtotal >= 20:  # $20 to less than $40
        discount = 10  # 10% off
    elif subtotal >= 10:  # $10 to less than $20
        discount = 5  # 5% off
    else:  # less than $10
        discount = 0  # no discount
    return discount  # send the percent back


def checkout(shopping_cart, quantities, products, prices):
    # prints the receipt and returns True if checkout happened
    if len(shopping_cart) == 0:  # can't check out with nothing in the cart
        print("Your shopping cart is empty!")  # tell the user
        print("Add something before checking out.")  # explain
        return False  # checkout did not happen, go back to the menu
    subtotal = calculate_total(shopping_cart, quantities, products, prices)  # subtotal before discount
    discount = calculate_discount(subtotal)  # discount percent
    saved = subtotal * discount / 100  # dollars saved
    final_total = subtotal - saved  # amount the customer pays
    print("\n========== RECEIPT ==========\n")  # receipt title
    print("Date: " + date.today().strftime("%m/%d/%Y") + "\n")  # today's date as MM/DD/YYYY
    for i in range(len(shopping_cart)):  # loop over every cart entry
        price = prices[products.index(shopping_cart[i])]  # look up the price
        print(f"{shopping_cart[i]:<10} {quantities[i]} x ${price:.2f}   ${price * quantities[i]:.2f}")  # name, math, line total
    print(f"\nSubtotal:      ${subtotal:.2f}")  # subtotal
    print(f"Discount:      {discount}%")  # discount percent
    print(f"Amount Saved:  ${saved:.2f}")  # dollars saved
    print(f"\nFinal Total:   ${final_total:.2f}")  # final amount
    print("\nThank you for shopping!")  # goodbye message
    return True  # checkout happened


at_checkout = False  # becomes True when the customer checks out

while at_checkout == False:  # main menu loop
    show_menu()  # display the menu
    number = get_valid_number("Enter your choice: ", 1, 6, "Invalid option!")  # validated menu choice
    if number == 1:  # view products
        display_products(products, prices)  # show the inventory
    elif number == 2:  # add to cart
        add_product(products, prices, shopping_cart, quantities)  # add a product
    elif number == 3:  # remove from cart
        remove_product(shopping_cart, quantities, products, prices)  # remove a product
    elif number == 4:  # view cart
        if len(shopping_cart) == 0:  # nothing in the cart
            print("Your shopping cart is empty!")  # tell the user
        else:
            display_cart(shopping_cart, quantities, products, prices)  # show the cart
    elif number == 5:  # view total
        display_total(shopping_cart, quantities, products, prices)  # show items and subtotal
    elif number == 6:  # checkout
        at_checkout = checkout(shopping_cart, quantities, products, prices)  # True ends the program