from teamwork import Table, tablers

# execute the program so it works
def excecute():
    '''
    The function to execute the entire program.
    
    program designed so that it manages orders and creates invoices. 
    It should be possible to view each table individually. Orders should be
    taken per table. The products ordered should be noted for each table.
    Of course, there can be repeat orders.
    
    An invoice should be able to be created at the end. In order to be able
    to resolve discrepancies, it must be possible to cancel or add
    individual items up until the invoice is paid.

    >>> input_people(5)
    >>> Table 1: 8 seats, 0 taken seats
    >>> Table 2: 6 seats, 0 taken seats
    >>> Table 3: 6 seats, 0 taken seats
    >>> input_table(3)
    >>> Table 3: 6 seats, 5 taken seats
    '''
    # first asks how many people will arrive
    input_people = input("Please input how many people shall be seated: ") 

    # if int, proceed, if not, reaffirm that it is a number
    try:    
        input_people = int(input_people)
    except:
        print("Not a valid input")
        return

    # there are no tables with more than 8 seats
    if input_people > 8:
        print("Too many people, please seperate them in smaller groups")
        return

    # show newly loaded list with available seating
    available = []
    for table in tablers:
        if table.seats - table.taken >= input_people:
            table.show_table()
            available.append(table)

    # ask for table
    input_table = int(input("Please input where you want to seat them: "))

    # ensures that the number put in is valid
    selected_table = next((table for table in tablers if table.table_number == input_table), None)
        (table for table in tablers if table.table_number == input_table),

    # check wether the selected table is even available
    if selected_table not in available:
        print(f"Table {input_table} is not available.")
        return

    # notif of a table being full
    if selected_table.seats == selected_table.taken:
        print(f"Table {selected_table} is full!")

    # add the people to the selected table
    else:
        selected_table.taken_seat(input_people)
        selected_table.show_table()


# keeps the code running till fatal error occurs
while True:
    excecute()
