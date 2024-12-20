__author__ = "8456041, Kolos, 7528006, Feldmann"

import pandas
import yaml
import csv


class Menu():
    '''
    Reads, displays and finds food on the menu from a cvs load-in
    '''

    def __init__(self):
        self.__menu = {}
        # File should be in the same folder as py file
        df = pandas.read_excel('food.xlsx')   
        # turns the csv into a dict
        for typ, group_typ in df.groupby("typ"):
            self.__menu[typ] = {}
            for category, group_category in group_typ.groupby("categorie"):
                self.__menu[typ][category] = group_category.set_index("name")[
                    "price"].to_dict()

        return


    def show_menu(self):
        '''
        function to show the menu prettier using yaml
        '''
        print(yaml.dump(self.__menu, default_flow_style=False))


    def take_position(self, position, amount):
        '''
        finds the position within the dictionary to access it whilst taking orders 
        '''


        def search(menu):
            '''
            searches on the menu
            '''
            for key, value in menu.items():
                if key == position:
                    # shows dict and appends all values needed
                    return {'position': key, 'price': value, 'amount': amount}
                # if key isnt the position taken, it goes deeper
                elif isinstance(value, dict):
                    deeper = search(value)
                    if deeper: return deeper
            return None

        result = search(self.__menu)
        if result: return result


class Order():
    '''
    handles orders, adding positions & beverages, removing them and completing the 
    order to turn it into a txt file
    '''

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
            return None

        if preferences is not None:
            if 'extra' in preferences.lower():
                take['preferences'] = preferences
                take['price'] += 1  # Increase price for extra
            elif 'no' in preferences.lower():
                take['preferences'] = preferences
            else:
                take['preferences'] = None
        else:
            take['preferences'] = None

        self.order_per_person.append(take)
        print(self.order_per_person)
        return self.order_per_person


    def remove_position(self, position):
        self.order_per_person = [item for item in self.order_per_person[1:]
                                 if item["position"] != position]
        print(f"You've removed {position} from your order.")
        print(self.order_per_person)
        return self.order_per_person


    def complete_order(self, table_id):
        bill = 0
        all_positions = []
        # Be careful with the path!
        path = r".\invoices"
        
        file_name = f"Table_{table_id}_Order_{self.order_id}.txt"

        with open(rf"{path}\{file_name}.txt", "w") as invoice:
            writer = csv.writer(invoice, delimiter="\t")
            invoice.write(f"Table: {table_id}, Order Nr: {self.order_id}\n")
            for i in self.order_per_person:
                if isinstance(i, dict):
                    bill += i['price'] * i['amount']
                    all_positions.append((i['position'],
                                          i['price'],
                                          i['amount'],
                                          i['preferences']))
            all_positions.append(('Sum EUR', bill))
            writer.writerows(all_positions)

        return [f"Table: {table_id}", self.order_id] + self.order_per_person


class Table():


    def __init__(self, table_number, seats):
        self.table_number = table_number  # Table numbers
        self.seats = seats  # Total Seats
        # self.all_tables[str(Restaurant.table_id)] = seats
        self.taken = 0  # Initial seat that are taken
        self.orders_per_table = []


    def serve(self, table_number, order_id):
        # Take an invoice from the order.
        id = str(table_number) + '0' + str(order_id)
        self.orders_per_table.append(id)
        return self.orders_per_table


    def remove_order(self, order):
        self.orders_per_table.remove(order)


    def __str__(self):
        return f"Table {self.table_number}\n"

    # show the text nicer
    def show_table(self):
        print(f"Table {self.table_number}: {self.seats} seats, {self.taken} taken seats")


    def taken_seat(self, taken):
        self.taken += taken  # Update the taken seats
        return taken


    def free_table(self):
        # When the clients are done, their table becomes free and can be
        # occupied by other customers.
        self.taken = 0
        return self.taken


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
