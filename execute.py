__author__ = "8456041, Kolos, 7528006, Feldmann"

from teamwork import tablers, Menu, Order, Table


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
2. Order per table
3. Pay Bill
4. Shut down
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
        pay_bill()
    if choice == "4":
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
    # get order for all people at a table
    menu = Menu()
    order = Order()
    table = Table()
    menu.show_menu()

    table_input = int(input("What table wants to order? "))
    table_id = tablers[table_input-1].taken
    
    try: 
        int(table_id)
    except:
        print("Please enter a valid input.")
        return
    
    if table_id == 0:
        print(f"There are no guests at table {table_input}, please seat guests before ordering food.")
    
    for i in range(table_id):
        while True:
            order_input = input(f"What would customer {i+1} like to order today? (Type 'Done' if you are done.)").upper()
            if order_input == "DONE":
                order.complete_order(table_input)
                break
            try:
                amount_input = int(input("How many of those do you want?" ))
            except ValueError:
                print("Please enter a valid amount.")
                continue
            
            preferences_input = input("Any preferences? (Extra... or No...)")
            if preferences_input == "No":
                order.add_food(menu, order_input, amount_input)
            else:
                order.add_food(menu, order_input, amount_input, preferences_input)
    
    orderhold = table.serve(table_input, order.order_id)
    print(f"Order {orderhold} has been placed")


def pay_bill():
    # pays for every order per table
    order = Order()
    table = Table()
    
    pay_table_input = int(input("what table is paying?"))
    pay_table = tablers[pay_table_input-1].table_number
    
    print(table.orders_per_table)
    pay_order_input = int(input("what order shall be paid off? "))
    
    
    pay_table.free_table(pay_table_input)
    
    
    


# keeps the code running till fatal error occurs
while True:
    excecution()