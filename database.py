import sqlite3
import csv

class Database:

    def __init__(self, connection, cursor):

        self.connection = connection
        self.cursor = cursor

        cursor.execute("CREATE TABLE IF NOT EXISTS users("
                       "id INTEGER PRIMARY KEY,"
                       "login TEXT,"
                       "password TEXT,"
                       "role TEXT,"
                       "department TEXT)")

        cursor.execute("CREATE TABLE IF NOT EXISTS transactions("
                       "department TEXT,"
                       "operation TEXT,"
                       "balance REAL)")


    def add_user(self, login, password, role, department):

        self.cursor.execute("SELECT MAX(id) FROM users")
        last_id = self.cursor.fetchone()[0]
        id = last_id + 1 if last_id is not None else 1

        self.cursor.execute("INSERT INTO users VALUES (?,?,?,?,?)",
                       (id, login, password, role, department))
        self.connection.commit()


    def delete_user(self, id):
        """
        id should be given as a string! (It's just how it works...)
        """
        self.cursor.execute("DELETE FROM users WHERE rowid = (?)", (id,))
        self.connection.commit()


    def get_user(self, login, password):

        try:
            self.cursor.execute("""SELECT role FROM users WHERE login = (?) 
                                AND password = (?)""", (login, password))
            return self.cursor.fetchone()[0]
        except TypeError: return None


    def department_members(self, department):

        self.cursor.execute("""SELECT * FROM users
                            WHERE department = (?)""", (department,))

        return self.cursor.fetchall()


    def assign_treasurer(self, id, department):

        in_department = False
        for i in self.department_members(department):
            if i[0] == int(id): in_department = True

        if in_department is False:
            return None
        else:
            self.cursor.execute("""UPDATE users SET role = 'treasurer'
                                    WHERE id = (?)""", (id,))
            self.connection.commit()


    def make_deposit(self, department, money):

        self.cursor.execute("""SELECT balance FROM transactions
                            WHERE department = (?)
                            ORDER BY rowid DESC LIMIT 1""", (department,))

        status = self.cursor.fetchone()
        balance = status[0] + money if status is not None else money
        operation = f"deposit of {money} € was made"

        self.cursor.execute("""INSERT INTO transactions VALUES (?,?,?)""",
                            (department, operation, balance))
        self.connection.commit()


    def make_withdraw(self, department, money):

        self.cursor.execute("""SELECT balance FROM transactions
                            WHERE department = (?)
                            ORDER BY rowid DESC LIMIT 1""", (department,))

        status = self.cursor.fetchone()
        if status is None or status[0] < money:
            print('Not enough money in the account.')
            return None
        else: balance = status[0] - money
        operation = f"withdraw of {money} € was made"

        self.cursor.execute("""INSERT INTO transactions VALUES (?,?,?)""",
                            (department, operation, balance))
        self.connection.commit()


    def transfer(self, money, donor, recipient):

        self.cursor.execute("""SELECT balance FROM transactions
                            WHERE department = (?)
                            ORDER BY rowid DESC LIMIT 1""", (donor,))

        status = self.cursor.fetchone()
        if status is None or status[0] < money:
            print('Not enough money in the account.')
            return None
        else:
            donor_balance = status[0] - money
            operation = f"transfer {money} € to {recipient} department"
            self.cursor.execute("""INSERT INTO transactions VALUES (?,?,?)""",
                                (donor, operation, donor_balance))

            self.cursor.execute("""SELECT balance FROM transactions
                                WHERE department = (?)
                                ORDER BY rowid DESC LIMIT 1""", (recipient,))
            status = self.cursor.fetchone()
            recipient_balance = status[0] + money
            operation = (f"receive {money} € from {donor} department")
            self.cursor.execute("""INSERT INTO transactions VALUES (?,?,?)""",
                                (recipient, operation, recipient_balance))


    def view_history(self, department='club'):

        if department == 'club':
            self.cursor.execute("""SELECT * FROM transactions""")
        else:
            self.cursor.execute("""SELECT * FROM transactions
                                WHERE department = (?)""", (department,))

        self.connection.commit()
        return self.cursor.fetchall()


    def save_status(self):

        self.cursor.execute("""SELECT * FROM users""")
        info = self.cursor.fetchall()
        columns = ['id', 'login', 'password', 'role', 'department']
        path = "./users.csv"
        with open(path, 'w') as users_file:
            writer = csv.writer(users_file)
            writer.writerow(columns)
            writer.writerows(info)

        self.cursor.execute("""SELECT * FROM transactions""")
        info = self.cursor.fetchall()
        columns = ['department', 'operation', 'balance']
        path = "./transactions.csv"
        with open(path, 'w') as transactions_file:
            writer = csv.writer(transactions_file)
            writer.writerow(columns)
            writer.writerows(info)


    def current_balance(self, department):

        self.cursor.execute("""SELECT balance FROM transactions
                            WHERE department = (?)
                            ORDER BY rowid DESC LIMIT 1""",
                            (department,))
        return self.cursor.fetchone()[0]