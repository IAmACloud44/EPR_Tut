'''--- Menu ---'''

import pandas
import json


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

# test = Menu()
# test.take_position(test.menu, 'FOREST-BURGER', 1)


# Restaurant Table arrangement
class Table:
    def __init__(self, table_number, seats):
        self.table_number = table_number  # Table numbers
        self.seats = seats  # Total Seats
        self.taken = 0  # Initial seat that are taken

    def __str__(self):
        return f"Table {self.table_number}"

    # show the text nicer
    def show_table(self):
        print(f"Table {self.table_number}: {self.seats} seats, {self.taken} taken seats")
    
    def taken_seat(self, taken):
        self.taken += taken  # Update the taken seats


tablers = [
    Table(1, 8),
    Table(2, 6),
    Table(3, 6),
    Table(4, 4),
    Table(5, 4),
    Table(6, 4),
    Table(7, 2),
    Table(8, 2),
    Table(9, 2),
    Table(10, 2),
    Table(11, 2),
    Table(12, 2)
]
