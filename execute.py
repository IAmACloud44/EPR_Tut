from teamwork import Table, tablers

def excecute():
    input_people = input("Please input how many people shall be seated: ")

    try:    
        input_people = int(input_people)
    except:
        print("Not a valid input")
        return

    available = [table for table in tablers.values() if table.seats >= input_people and table.seats - table.taken >= input_people]
    print(str(available))

    input_table = input("Please input where you want to seat them: ")

    # if input_table not in available:
    #     print("That Table is not available.")
    #     return

    if input_people > tablers[input_table].seats or input_people > tablers[input_table].seats - tablers[input_table].taken:
        print("Not enough seats.")
    else:
        tablers[input_table].taken_seat(input_people)
        tablers[input_table].show_table()


while True:
    excecute()
