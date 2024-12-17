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
        if result:
            print(f"You've ordered {amount} {position} "
                  f"for {result['price']} €.")
        return result

class Order():

    __order_id = 0

    def __init__(self):
        # order_per_person = [order_id,
        # {'position': 'BURGER', 'price': 10.0, 'amount': 1},
        # {'position': 'COLA 0.5', 'price': 3.5, 'amount': 1}]
        Order.__order_id += 1
        self.order_per_person = [Order.__order_id]

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

        with open(rf"{path}\{self.__order_id}.txt", "w") as invoice:
            writer = csv.writer(invoice, delimiter="\t")
            invoice.write(f"The order Nr: {self.__order_id} \n")
            for i in self.order_per_person:
                if isinstance(i, dict):
                    bill += i['price'] * i['amount']
                    all_positions.append((i['position'],
                                          i['price'],
                                          i['amount']))
            all_positions.append(('Sum EUR', bill))
            writer.writerows(all_positions)

        return [self.__order_id] + self.order_per_person

class Table():

    def __init__(self):


class Restaurant():

    table_id = 0

    def __init__(self):
        # structure: {'table_id': number_of_seats}
        # all_tables = {'1', 2, '2', 2, '3': 4, '4': 4, '5': 8}
        self.__all_tables = {}
        self.occupied_tables = {}

    def assign_table(self, seats):
        Restaurant.table_id += 1
        self.__all_tables[str(Restaurant.table_id)] = seats
        self.__all_tables = dict(sorted(self.__all_tables.items()))
        return self.__all_tables

    def take_table(self, clients):
        for i in self.__all_tables:
            if self.__all_tables[i] >= clients and i not in self.occupied_tables:
                self.occupied_tables[i] = clients
                return self.occupied_tables