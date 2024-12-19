__author__ = "8456041, Kolos, 7528006, Feldmann"

from teamwork import tablers, Menu, Order, Table, Restaurant


# execute the program so it works
def excecution():
    '''
    The function to execute the entire program.

    program designed so that it manages orders and creates invoices. 
    It should be possible to view each table individually. Orders should be
    taken per table. The products ordered should be noted for each table.
    Of course, there can be repeat orders.

    An invoice should be able to be created at the end. In order to be able
    to resolve discrepancies, it must be possible to cancel or add
    individual items up until the invoice is paid.
    '''
    # print the starting menu
    print("""
----------------------
Choose an action: 
----------------------
1. Take seats 
2. Order Food
3. Shut down
----------------------""")

    choice = input("What will you be doing today? \n")
    # taking seats
    if choice == "1":
        take_seats()
    # order food
    if choice == "2":
        ordering()
    # shut down
    if choice == "3":
        exit()
    else: 
        print("Not a valid input.")


def take_seats():
    '''
    Function for taking up and seating people
    
    does include how many people are in an incoming group, how many 
    seats are taken
    does not include if a seat has been left, will be included in paying
    the bill.
    
    Has a continuous track of people coming in and taking seats.
    '''
    # first asks how many people will arrive
    input_people = input("\nPlease input how many people shall be seated: ") 

    # if int, proceed, if not, reaffirm that it is a number
    try:    
        input_people = int(input_people)
    except:
        print("Not a valid input")
        return

    # there are no tables with more than 8 seats
    if input_people > 8:
        print("\nToo many people, please seperate them in smaller groups")
        return

    # show newly loaded list with available seating
    available = []
    for table in tablers:
        if table.seats - table.taken >= input_people:
            table.show_table()
            available.append(table)

    # ask for table
    input_table = int(input("\nPlease input where you want to seat them: "))

    # ensures that the number put in is valid
    selected_table = next((table for table in tablers if table.table_number == input_table), None)
    # (table for table in tablers if table.table_number == input_table),

    # check wether the selected table is even available
    if selected_table not in available:
        print(f"\nTable {input_table} is not available.")
        return

    # notif of a table being full
    if selected_table.seats == selected_table.taken:
        print(f"\nTable {selected_table} is full!")

    # add the people to the selected table
    else:
        selected_table.taken_seat(input_people)
        selected_table.show_table()


def ordering():
    '''
    function designed to order food.
    reads in the menu and displays it, then runs input prompts to
    be put into a list, which after completion will be saved as a txt file.
    
    
    '''
    menu = Menu()
    menu.show_menu()
    order = Order()
    serve = Table()

    while True:
        order_input = input("What would you like to order today? ").upper()
        if order_input == "NOTHING":
            return False
        else:
            amount_input = int(input("How many of those do you want? (Type 'Nothing' to stop) "))
            preferences_input = input("Any preferences? (Extra... or No...)")
            if preferences_input == "No":
                order.add_food(menu, order_input, amount_input)
            else:
                order.add_food(menu, order_input, amount_input, preferences_input)


def upgrade_order():
    menu = Menu()
    order = Order()
    table_id = input("Which Order should be updated? ")


    food_update = input("What food should be updated? ") 
    amount_update = int(input("What is the amount changing to? "))
    preference_update = input("Are any of the preferences changing? ").lower()
    if preference_update == "no":
        order.add_food(menu, food_update, amount_update)
    else:
        order.add_food(menu, food_update, amount_update, preference_update)
        
def pay_bill():
    pass


# keeps the code running till fatal error occurs
while True:
    excecution()