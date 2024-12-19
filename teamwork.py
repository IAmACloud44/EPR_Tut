__author__ = "8456041, Kolos, 7528006, Feldmann"

'''--- Menu ---'''

import pandas
import yaml
import csv


class Menu():

    def __init__(self):
        self.__menu = {}
        df = pandas.read_excel('food.xlsx')  # Be careful with the file path!
        for typ, group_typ in df.groupby("typ"):
            self.__menu[typ] = {}
            for category, group_category in group_typ.groupby("categorie"):
                self.__menu[typ][category] = group_category.set_index("name")[
                    "price"].to_dict()

        return

    def show_menu(self):
        print(yaml.dump(self.__menu, default_flow_style=False))


    def take_food(self, food, amount):

        def search(menu):
            for key, value in menu.items():
                if key == food:
                    return {'food': key, 'price': value, 'amount': amount}
                elif isinstance(value, dict):
                    deeper = search(value)
                    if deeper: return deeper
            return None

        result = search(self.__menu)
        if result: return result


class Order():

    order_id = 0

    def __init__(self):
        # order_per_person = [order_id,
        # {'position': 'BURGER', 'price': 10.0, 'amount': 1},
        # {'position': 'COLA 0.5', 'price': 3.5, 'amount': 1}]
        Order.order_id += 1
        self.order_per_person = [str(Order.order_id)]

    def add_food(self, menu, food, amount, preferences=None):
        take = menu.take_food(food, amount)

        if take is None:
            print('There is no such food on the menu.'
                  'Try another food.\n'
                  'If you have any difficulties, please contact the staff.')
            self.add_food(menu, food, amount, preferences)

        if preferences is not None:
            if 'extra' in preferences.lower():
                take['food'] = food + ' + ' + preferences
                take['price'] += 1
            elif 'no' in preferences.lower():
                take['food'] = food + ' - ' + preferences

        self.order_per_person.append(take)
        print(self.order_per_person)
        return self.order_per_person


    def remove_food(self, food):
        self.order_per_person = [item for item in self.order_per_person[1:]
                                 if item["food"] != food]
        print(f"You've removed {food} from your order.")
        return self.order_per_person


    def complete_order(self):
        bill = 0
        all_foods = []
        # Be careful with the path!
        path = r".\invoices"

        with open(rf"{path}\{self.order_id}.txt", "w") as invoice:
            writer = csv.writer(invoice, delimiter="\t")
            invoice.write(f"The order Nr: {self.order_id} \n")
            for i in self.order_per_person:
                if isinstance(i, dict):
                    bill += i['price'] * i['amount']
                    all_foods.append((i['food'],
                                          i['price'],
                                          i['amount']))
            all_foods.append(('Sum EUR', bill))
            writer.writerows(all_foods)

        return [self.order_id] + self.order_per_person


class Table():

    def __init__(self):
        self.orders_per_table = []

    def serve(self, table_number, order_id):
        # Take an invoice from the order.
        id = table_number + '0' + order_id
        self.orders_per_table.append(id)
        return self.orders_per_table


# Restaurant Table arrangement
class Restaurant:
    def __init__(self, table_number, seats):
        self.table_number = table_number  # Table numbers
        self.seats = seats  # Total Seats
        # self.all_tables[str(Restaurant.table_id)] = seats
        self.taken = 0  # Initial seat that are taken

    def __str__(self):
        return f"Table {self.table_number}\n"


    # show the text nicer
    def show_table(self):
        print(f"Table {self.table_number}: {self.seats} seats, {self.taken} taken seats")


    def taken_seat(self, taken):
        self.taken += taken  # Update the taken seats


    def free_table(self, table_number):
        # When the clients are done, their table becomes free and can be
        # occupied by other customers.
        del self.taken[table_number]
        return self.taken


tablers = [
    Restaurant(1, 8),
    Restaurant(2, 6),
    Restaurant(3, 6),
    Restaurant(4, 4),
    Restaurant(5, 4),
    Restaurant(6, 4),
    Restaurant(7, 2),
    Restaurant(8, 2),
    Restaurant(9, 2),
    Restaurant(10, 2),
    Restaurant(11, 2),
    Restaurant(12, 2)
]
