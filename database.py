import sqlite3

class Database:
    def __init__(self, connection, cursor):

        self.connection = connection
        self.cursor = cursor

        cursor.execute("CREATE TABLE IF NOT EXISTS users("
                       "id INTEGER PRIMARY KEY,"
                       "login TEXT,"
                       "password TEXT,"
                       "role TEXT)")

        cursor.execute("CREATE TABLE IF NOT EXISTS history("
                       "department TEXT,"
                       "operation TEXT,"
                       "balance REAL)")


    def add_user(self, login, password, role):

        self.cursor.execute("SELECT MAX(id) FROM users")
        last_id = self.cursor.fetchone()[0]
        id = last_id + 1 if last_id is not None else 1

        self.cursor.execute("INSERT INTO users VALUES (?,?,?,?)",
                       (id, login, password, role))
        self.connection.commit()


    def delete_user(self, id):
        """
        id should be given as a string! (It's just how it works...)
        """
        self.cursor.execute("DELETE FROM users WHERE rowid = (?)", id)
        self.connection.commit()


    def get_user(self, login, password):

        try:
            self.cursor.execute("""SELECT role FROM users WHERE login = (?) 
                            AND password = (?)""", (login, password))
            return self.cursor.fetchone()[0]
        except TypeError:
            print('Login or password is incorrect.')
            return None


# '''TESTS'''

# members = [('Mary_Brown', 'NqKX069L', 'admin'),
#            ('John_Elder', 'OnH139sp', 'officer'),
#            ('Wes_Smith', '850QuL96', 'member'),
#            ('Bob_Miller', '0ITF8cO2', 'member'),
#            ('Dan_White', 'tSh8c8j3', 'member'),
#            ('Tim_Smith', 'Yor4T4Z2', 'member'),
#            ('Joe_Black', 'fC584HGq', 'member'),
#            ('Laura_Lie', '3S2k5WYu', 'member'),
#            ('Rico_Salieri', 'c1jV1k4p', 'member'),
#            ('Anton_Kusnezow', '253DzRap', 'member')]

# db = Database(sqlite3.connect('database.db'),
#               sqlite3.connect('database.db').cursor())

# for i in members:
#     db.add_user(*i)

# db.delete_user('8')

# print(db.get_user('Laura_Lie', '3S2k5WYu'))
# print(db.get_user('Joe_Black', 'fC584HGq'))