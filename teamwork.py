'''--- Menu ---'''

import pandas
import json
import csv

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

    def take_position(self, position, amount):

        def search(menu):
            for key, value in menu.items():
                if key == position:
                    return {'position': key, 'price': value, 
                            'amount': amount}
                elif isinstance(value, dict):
                    deeper = search(value)
                    if deeper: return deeper
            return None

        result = search(self.menu)
        if result:
            print(f"You've ordered {amount} {position} "
                  f"for {result['price']} €.")
        return result


class Order():

    order_id = 0

    def __init__(self):
        # order_per_person = [order_id,
        # {'position': 'BURGER', 'price': 10.0, 'amount': 1},
        # {'position': 'COLA 0.5', 'price': 3.5, 'amount': 1}]
        Order.order_id += 1
        self.order_per_person = [Order.order_id]

    def add_position(self, menu, position, amount):
        take = menu.take_position(position, amount)

        if take is None:
            print('There is no such position on the menu.'
                  'Try another position.\n'
                  'If you have any difficulties, please contact the staff.')
            self.add_position(menu, position, amount)

        self.order_per_person.append(take)

    def remove_position(self, position):
        self.order_per_person = [item for item in self.order_per_person[1:]
                                 if item["position"] != position]
        print(f"You've removed {position} from your order.")
        return self.order_per_person

    def complete_order(self):
        bill = 0
        all_positions = []
        path = r"C:\Users\rener\Documents\GitHub\EPR_Teamwork\invoices"

        with open(rf"{path}\{self.order_id}.txt", "w") as invoice:
            writer = csv.writer(invoice, delimiter="\t")
            invoice.write(f"The order Nr: {self.order_id} \n")
            for i in self.order_per_person:
                if isinstance(i, dict):
                    bill += i['price'] * i['amount']
                    all_positions.append((i['position'],
                                          i['price'],
                                          i['amount']))
            all_positions.append(('Sum EUR', bill))
            writer.writerows(all_positions)

        return [self.order_id] + self.order_per_person

menu = Menu()
order = Order()
order.add_position(menu, 'FOREST-BURGER', 2)
order.add_position(menu, 'COLA (0.4)', 1)
order.remove_position('FOREST-BURGER')
order.add_position(menu, 'PIZZA-HAWAI', 1)
order.complete_order(0)

############################################################################



############################################################################

# Restaurant Table arrangement
class Restaurant:
    def __init__(self, table_number, seats):
        self.table_number = table_number  # Table numbers
        self.seats = seats  # Total Seats
        self.taken = 0  # Initial seat that are taken

    def __str__(self):
        return f"Table {self.table_number}"

    # show the text nicer
    def show_table(self):
        print(f"Table {self.table_number}: {self.seats} seats, 
              {self.taken} taken seats")
    
    def taken_seat(self, taken):
        self.taken += taken  # Update the taken seats


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
