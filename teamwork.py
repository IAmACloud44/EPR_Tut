'''--- Menu ---'''

import pandas as pd
import json

df = pd.read_excel('food.xlsx') # Be careful with the file path!

menu = {}
for typ, group_typ in df.groupby("typ"):
    menu[typ] = {}
    for category, group_category in group_typ.groupby("categorie"):
        menu[typ][category] = group_category.set_index("name")["price"].to_dict()

print((json.dumps(menu, indent=4)))

# Restaurant Table arrangement
def assign_tables(seats):
    dict[table] = {}
    for i in range (0,8):
        dict.add[table] = i


def take_tables(table, clients):
    pass