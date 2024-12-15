'''--- Menu ---'''

import pandas as pd
import json

df = pd.read_excel('food.xlsx') # Be careful with the file path!

menu = {}
for typ, group_typ in df.groupby("typ"):
    menu[typ] = {}
    for category, group_category in group_typ.groupby("categorie"):
        menu[typ][category] = group_category.set_index("name")["price"].to_dict()

# print((json.dumps(menu, indent=4)))

# Restaurant Table arrangement
class Table:
    def __init__(self, table_number, seats):
        self.table_number = table_number
        self.seats = seats
        self.taken = 0

    def show_table(self):
        print(f"{self.table_number},{self.seats},{self.taken}")
    
    def taken_seat(self, taken):
        self.taken = taken
        

tablers = {
    "Table1" : Table(1, 8),
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


tablers["Table3"].show_table()
tablers["Table2"].taken_seat(5)
tablers["Table3"].show_table()
