import pandas
import json
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

        print((json.dumps(self.__menu, indent=4)))

    def take_position(self, position, amount):

        def search(menu):
            for key, value in menu.items():
                if key == position:
                    return {'position': key, 'price': value, 'amount': amount}
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

    def add_position(self, menu, position, amount, preferences=None):
        take = menu.take_position(position, amount)

        if take is None:
            print('There is no such position on the menu.'
                  'Try another position.\n'
                  'If you have any difficulties, please contact the staff.')
            self.add_position(menu, position, amount, preferences)

        if preferences is not None:
            if 'extra' in preferences.lower():
                take['position'] = position + ' + ' + preferences
                take['price'] += 1
            elif 'no' in preferences.lower():
                take['position'] = position + ' - ' + preferences

        self.order_per_person.append(take)
        return self.order_per_person

    def remove_position(self, position):
        self.order_per_person = [item for item in self.order_per_person[1:]
                                 if item["position"] != position]
        print(f"You've removed {position} from your order.")
        return self.order_per_person

    def complete_order(self):
        bill = 0
        all_positions = []
        # Be careful with the path!
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

class Table():

    def __init__(self):
        self.orders_per_table = []

    def serve(self, table_id, order_id, clients):
        # Take an invoice from every client from the table.
        for _ in range(clients):
            id = table_id + '0' + order_id
            self.orders_per_table.append(id)
        return self.orders_per_table

class Restaurant():

    table_id = 0

    def __init__(self):
        # all_tables = {'table_id': seats}
        self.all_tables = {}
        # occupied_tables = {'table_id': clients}
        self.occupied_tables = {}

    def assign_table(self, seats):
        # With each new table its id is increased by 1.
        Restaurant.table_id += 1
        self.all_tables[str(Restaurant.table_id)] = seats
        # Sort dictionary by the number of seats, so it would be easier
        # to occupy them. Herewith tables with the least number of seats
        # suitable for the certain number of clients will be allocated first.
        self.all_tables = dict(sorted(self.all_tables.items()))
        return self.all_tables

    def take_table(self, clients):
        for i in self.all_tables:
            # Taken will be the first table with the smallest appropriate
            # number of seats.
            if ((self.all_tables[i] >= clients)
                and (i not in self.occupied_tables)):
                self.occupied_tables[i] = clients
                return self.occupied_tables
        # if there is no table big enough for such a large number of customers,
        # returns None.
        print(f"Unfortunately we can't provide a table for {clients} people.\n"
              f"We apologise for any inconvenience caused!")
        return None

    def free_table(self, table_id):
        # When the clients are done, their table becomes free and can be
        # occupied by other customers.
        del self.occupied_tables[table_id]
        return self.occupied_tables