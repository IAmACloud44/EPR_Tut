'''--- Menu ---'''

import pandas
import json


# Menu
class Menu():

    def __init__(self):
        self.menu = {}

        df = pandas.read_excel('food.xlsx')  # Be careful with the file path!
        for typ, group_typ in df.groupby("typ"):
            self.menu[typ] = {}
            for category, group_category in group_typ.groupby("categorie"):
                self.menu[typ][category] = group_category.set_index("name")[
                    "price"].to_dict()

        print((json.dumps(self.menu, indent=4)))

    def take_position(self, menu, position, amount):

        for key, value in menu.items():
            if key == position:
                print(f"You've ordered {amount} {key} for {value} €.")
                return {key: value, 'amount': amount}
            elif isinstance(value, dict):
                result = self.take_position(value, position, amount)
                if result: return result
        '''If return None, ask for another position in the next function.'''
        return None

test = Menu()
test.take_position(test.menu, 'FOREST-BURGER', 1)


# Restaurant Table arrangement
class Table:
    def __init__(self, table_number, seats):
        self.table_number = table_number
        self.seats = seats
        self.taken = 0

    def __str__(self):
        return self.table_number, self.seats, self.taken

    def show_table(self):
        print(f"{self.table_number},{self.seats},{self.taken}")
    
    def taken_seat(self, taken):
        self.taken += taken


tablers = {
    "Table1" : Table("Table1", 8),
    "Table2" : Table(2, 6),
    "Table3" : Table(3, 6),
    "Table4" : Table(4, 4),
    "Table5" : Table(5, 4),
    "Table6" : Table(6, 4),
    "Table7" : Table(7, 2),
    "Table8" : Table(8, 2),
    "Table9" : Table(9, 2),
    "Table10" : Table(10, 2),
    "Table11" : Table(11, 2),
    "Table12" : Table(12, 2)
}
