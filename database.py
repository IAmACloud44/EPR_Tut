import csv


class Database:
    """
    The following class is responsible for creating a database. It allows to
    make changes to it and retrieve information from it.
    Connection to the database should be established at the moment of class
    object creation as its parameters, like this:
    db = Database(sqlite3.connect('database.db'),
                  sqlite3.connect('database.db').cursor())
    """
    def __init__(self, connection, cursor):
        """
        Creates 2 tables in the database (hereinafter abbreviated as DB):
        one with all the members of the club and information about them (users)
        and another with all the transactions within the club (transactions).
        """
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
        """
        Adds a new user to the users table of the DB.
        Does not return anything, just make changes directly in the DB.
        """
        self.cursor.execute("SELECT MAX(id) FROM users")
        last_id = self.cursor.fetchone()[0]
        id = last_id + 1 if last_id is not None else 1
        self.cursor.execute("INSERT INTO users VALUES (?,?,?,?,?)",
                            (id, login, password, role, department))
        self.connection.commit()


    def update_user(self, login, password, role, department):
        """
        Allows to update existing users' information.
        Does not return anything, just make changes directly in the DB.
        """
        self.cursor.execute("""UPDATE users SET department = ?, role = ?
                             WHERE login = ? AND password = ?""",
                            (department, role, login, password))
        self.connection.commit()

    def delete_user(self, id):
        """
        Removes a row from the users table by its id.
        Important: id should be given as a string!
        Changes DB directly, doesn't return anything.
        """
        self.cursor.execute("DELETE FROM users WHERE rowid = (?)", (id,))
        self.connection.commit()

    def get_user(self, login, password):
        """
        The following function is used primarily for log in in the console.
        If login and password are both in DB, it returns the role of this
        member. Otherwise, it returns None.
        """
        try:
            self.cursor.execute("""SELECT role FROM users WHERE login = (?)
                                AND password = (?)""", (login, password))
            return self.cursor.fetchone()[0]
        except TypeError:
            return None


    def all_departments(self):
        """
        Creates a list of all departments in the users table.
        Returns a sorted list with the departments.
        """
        self.cursor.execute("""SELECT department FROM transactions""")
        departments = self.cursor.fetchall()
        # Convert list of tuples to a set to remove duplicates,
        # then back to a sorted list.
        unique_departments = sorted(set(dept[0] for dept in departments))
        return unique_departments

    def department_members(self, department):
        """
        Lists all the members of a particular department.
        Returns a list of tupels.
        """
        self.cursor.execute("""SELECT * FROM users
                            WHERE department = (?)""", (department,))
        return self.cursor.fetchall()

    def get_id(self, login):
        """
        Finds an id of a member from the users table by his login.
        Returns it as a list with one tupel once it's found.
        """
        self.cursor.execute("""SELECT id FROM users
                            WHERE login = (?)""", (login,))
        return self.cursor.fetchall()

    def get_department(self, login):
        """
        Finds a department of a member from the users table by his login.
        Returns it as a list with one tupel once it's found.
        """
        self.cursor.execute("""SELECT department FROM users
                            WHERE login = (?)""", (login,))
        return self.cursor.fetchall()

    def assign_treasurer(self, id, department):
        """
        Changes one's role to a treasurer of a particular department,
        if this person is a member of this department.
        Returns None, if he's not. That means his role has not been changed.
        """
        # A variable to check, if this person is in the department.
        in_department = False
        for i in self.department_members(department):
            # If he is, the variable changes to True.
            if i[0] == int(id):
                in_department = True
        # If the person isn't a member of the department, return None.
        if in_department is False:
            return None
        # If he is, change his role.
        else:
            self.cursor.execute("""UPDATE users SET role = 'treasurer'
                                    WHERE id = (?)""", (id,))
            self.connection.commit()

    def check_treasurer(self, department):
        """Only one treasurer can be there per department, here it checks for
        it and makes sure only one is a treasurer. To reassign roles, one needs
        to remove the role, then add it."""

        self.cursor.execute("""SELECT COUNT(*) FROM users
                            WHERE department = (?) AND role = 'treasurer'
                            """, (department,))

        treasurer_count = int(self.cursor.fetchone()[0])

        if treasurer_count > 0:
            return True
        else:
            return False
    
    def check_if_treasurer(self, login):
        '''Checks wether the person is already a treasurer or not'''
        
        self.cursor.execute("""SELECT COUNT(*) FROM users
                            WHERE role = 'treasurer'
                            AND login = (?)""",
                            (login,))
        
        treasurer_count = int(self.cursor.fetchone()[0])
        
        if treasurer_count > 0:
            return True
        else:
            return False

    def update_department(self, login, department):
        """
        Allows to change the department of a member by his login.
        Changes DB directly, doesn't return anything.
        """
        self.cursor.execute("""UPDATE users SET department = ?
                            WHERE login = ?""", (department, login))
        self.connection.commit()

    def update_role(self, login, role, department):
        """
        Allows to change the role of a member of a specific department
        by his login.
        Changes DB directly, doesn't return anything.
        """
        self.cursor.execute("""UPDATE users SET department = ? AND role = ?
                            WHERE login = ?""", (department, role, login))
        self.connection.commit()


    def make_deposit(self, department, money):
        """
        Increases balance of a specific department by a certain amount
        of money. Therefore, s new row to the transactions table will be added.
        Changes DB directly, doesn't return anything.
        """
        self.cursor.execute("""SELECT balance FROM transactions
                            WHERE department = (?)
                            ORDER BY rowid DESC LIMIT 1""", (department,))
        # Maintains the last balance status of the department
        # If the balance was not yet defined, it becomes None.
        status = self.cursor.fetchone()
        # If the status is None, the new balance equals the amount
        # of money added. Otherwise, the last balance will be summarized with
        # the added money.
        balance = status[0] + money if status is not None else money
        # Adds an operation description to the row.
        operation = f"deposit of {money} € was made"
        self.cursor.execute("""INSERT INTO transactions VALUES (?,?,?)""",
                            (department, operation, balance))
        self.connection.commit()

    def make_withdraw(self, department, money):
        """
        Decreases balance of a specific department by a certain amount
        of money. Therefore, s new row to the transactions table will be added.
        Changes DB directly, doesn't return anything.
        Returns the new balance, if money were successfully withdrawn.
        Otherwise, returns None.
        """
        self.cursor.execute("""SELECT balance FROM transactions
                            WHERE department = (?)
                            ORDER BY rowid DESC LIMIT 1""", (department,))
        # Maintains the last balance status of the department
        # If the balance was not yet defined, it becomes None.
        status = self.cursor.fetchone()
        # If balance is None, no money could be withdrawn.
        # It's also impossible to withdraw more money than there is currently
        # in the account.
        if status is None or status[0] < money:
            return None
        # Otherwise, the balance will be reduced by a certain amount of money.
        else:
            balance = status[0] - money
        # Adds an operation description to the row.
        operation = f"withdraw of {money} € was made"
        self.cursor.execute("""INSERT INTO transactions VALUES (?,?,?)""",
                            (department, operation, balance))
        self.connection.commit()
        return balance

    def transfer(self, money, donor, recipient):
        """
        Simulates transfer of money from one department to another. Balance
        of the donor department will be reduced by 'money' and one of
        the recipient department will be increased by 'money', if the
        operation is possible. 2 new rows in transactions table will be added.
        Returns None, if the transfer wasn't possible.
        """
        # Donor part:
        self.cursor.execute("""SELECT balance FROM transactions
                            WHERE department = (?)
                            ORDER BY rowid DESC LIMIT 1""", (donor,))
        # Maintains the last balance status of the department
        # If the balance was not yet defined, it becomes None.
        status = self.cursor.fetchone()
        # If balance is None, no money could be withdrawn.
        # It's also impossible to withdraw more money than there is currently
        # in the account.
        if status is None or status[0] < money:
            return None
        # Otherwise, the donor's balance will be decreased.
        else:
            donor_balance = status[0] - money
            # Creates an operation description for the row.
            operation = f"transfer {money} € to {recipient} department"
            self.cursor.execute("""INSERT INTO transactions VALUES (?,?,?)""",
                                (donor, operation, donor_balance))
            # Recipient part:
            self.cursor.execute("""SELECT balance FROM transactions
                                WHERE department = (?)
                                ORDER BY rowid DESC LIMIT 1""", (recipient,))
            status = self.cursor.fetchone()
            # If the recipient's balance was not yet defined, its balance
            # equals the amount of money added.
            if status is None:
                recipient_balance = money
            # Otherwise, it will be summarized with the money.
            else:
                recipient_balance = status[0] + money
            # Creates an operation description for the row.
            operation = (f"receive {money} € from {donor} department")
            self.cursor.execute("""INSERT INTO transactions VALUES (?,?,?)""",
                                (recipient, operation, recipient_balance))
            self.connection.commit()

    def view_history(self, department='club'):
        """
        Shows the transaction history of a specific department or overall.
        Returns a list of tuples with each operation.
        """
        # If instead of a department 'club' was given, an overall transaction
        # history would be given.
        if department == 'club':
            self.cursor.execute("""SELECT * FROM transactions""")
        # If a specific department is given, only its rows will be selected.
        else:
            self.cursor.execute("""SELECT * FROM transactions
                                WHERE department = (?)""", (department,))
        self.connection.commit()
        return self.cursor.fetchall()


    def save_data(self):
        """
        Saves a current users table as a .csv file. It's not very good-looking
        one though (I'm just being honest, couldn't tame those 'delimiter'
        and shit)...
        The .csv file will be created in the current directory.
        """
        self.cursor.execute("""SELECT * FROM users""")
        info = self.cursor.fetchall()
        columns = ['id', 'login', 'password', 'role', 'department']
        path = "./users.csv"
        with open(path, 'w') as users_file:
            writer = csv.writer(users_file)
            writer.writerow(columns)
            writer.writerows(info)

<<<<<<< HEAD
=======

>>>>>>> 134494e6152806a870d6baa4a7213c4fb6abb47b
    def save_transactions(self):
        """
        Saves a current transaction table as a .csv file. It's just as ugly
        as users' one. The .csv file will be created in the current directory.
        """
        self.cursor.execute("""SELECT * FROM transactions""")
        info = self.cursor.fetchall()
        columns = ['department', 'operation', 'balance']
        path = "./transactions.csv"
        with open(path, 'w') as transactions_file:
            writer = csv.writer(transactions_file)
            writer.writerow(columns)
            writer.writerows(info)

<<<<<<< HEAD
    def current_balance(self, department):
        """
        Saves the current balance table of a sepcified department as a .csv
        file.
        """
=======
>>>>>>> 134494e6152806a870d6baa4a7213c4fb6abb47b

    def current_balance(self, department):
        """
        Finds the last balance status of a specific department.
        Returns None if no balance is found. Otherwise, creates .csv file
        with the current balance of the department.
        """
        self.cursor.execute("""SELECT balance FROM transactions
                            WHERE department = (?)
                            ORDER BY rowid DESC LIMIT 1""", (department,))
        # Saves the last balance status of the department.
        status = self.cursor.fetchone()
        # If it was not found, returns None.
        if status is None:
            return
        info = status[0]
        columns = ['department', 'balance']
        path = f"./current_balance_{department}.csv"
        with open(path, 'w', newline='') as transactions_file:
            writer = csv.writer(transactions_file)
            writer.writerow(columns)
            writer.writerow([department, info])

<<<<<<< HEAD
    def full_balance(self):
        """
        Saves the entire balance table of as a .csv file.
        """
        self.cursor.execute("""SELECT department, balance
                            FROM transactions
                            WHERE rowid IN (
                                SELECT MAX(rowid) FROM transactions
                                GROUP BY department
                            )
                        """)
=======

    def full_balance(self):
        """
        Creates .csv file with the current balance status of all departments.
        If anything was not found, returns None.
        """
        self.cursor.execute("""SELECT department, balance 
                            FROM transactions 
                            WHERE rowid IN (
                            SELECT MAX(rowid) FROM transactions 
                            GROUP BY department)""")
>>>>>>> 134494e6152806a870d6baa4a7213c4fb6abb47b
        results = self.cursor.fetchall()
        # If nothing is in the table, returns None.
        if not results:
            return
        columns = ['department', 'balance']
        path = "./all_departments_balance.csv"
        with open(path, 'w', newline='') as transactions_file:
            writer = csv.writer(transactions_file)
            writer.writerow(columns)
            writer.writerows(results)
