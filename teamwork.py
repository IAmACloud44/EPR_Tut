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

test = Menu()
test.take_position(test.menu, 'FOREST-BURGER', 1)