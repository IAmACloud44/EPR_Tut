import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users("
               "id INTEGER PRIMARY KEY,"
               "login TEXT,"
               "password TEXT,"
               "role TEXT)")


def add_user(login, password, role):

    cursor.execute("SELECT MAX(id) FROM users")
    last_id = cursor.fetchone()[0]
    id = last_id + 1 if last_id is not None else 1

    cursor.execute("INSERT INTO users VALUES (?,?,?,?)",
                   (id, login, password, role))
    connection.commit()


def delete_user(id):
    """
    id should be given as a string! (It's just how it works...)
    """
    cursor.execute("DELETE FROM users WHERE rowid = (?)", id)
    connection.commit()


def get_user(login, password):

    try:
        cursor.execute("""SELECT role FROM users WHERE login = (?) 
                        AND password = (?)""", (login, password))
        return cursor.fetchone()[0]
    except TypeError:
        print('Login or password is incorrect.')
        return None


'''TESTS'''

members = [('Mary_Brown', 'NqKX069L', 'admin'),
           ('John_Elder', 'OnH139sp', 'officer'),
           ('Wes_Smith', '850QuL96', 'member'),
           ('Bob_Miller', '0ITF8cO2', 'member'),
           ('Dan_White', 'tSh8c8j3', 'member'),
           ('Tim_Smith', 'Yor4T4Z2', 'member'),
           ('Joe_Black', 'fC584HGq', 'member'),
           ('Laura_Lie', '3S2k5WYu', 'member'),
           ('Rico_Salieri', 'c1jV1k4p', 'member'),
           ('Anton_Kusnezow', '253DzRap', 'member')]

for i in members:
    add_user(*i)

delete_user('8')

print(get_user('Laura_Lie', '3S2k5WYu'))
print(get_user('Joe_Black', 'fC584HGq'))