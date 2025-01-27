import tkinter as tk

class Account():
    def __init__(self, department, balance=0):
        self.department = department
        self.balance = float(balance)
        self.history = []

    def check_balance(self, update):
        if update < 0:
            raise ValueError("Not enough money in the account!")

class Treasurer(Account):

    def __init__(self, account):
        self.account = account

    def view_transaction_history(self):
        counter = 1
        for i in self.account.history:
            print(f"{counter}. {i}")
            counter += 1

    def make_deposit(self, money):
        self.account.balance += float(money)
        self.account.history += [f"{money} € were deposited into the account."]

    def make_withdraw(self, money):
        money = float(money)
        self.account.check_balance(self.account.balance - money)

        self.account.balance -= money
        self.account.history += [f"{money} € were withdrawn from the account."]

    def transfer(self, money, recipient):
        money = float(money)
        self.account.check_balance(self.account.balance - money)

        self.account.balance -= money
        self.account.history += [f"{money} € were transferred to {recipient}."]

        recipient.balance += money
        recipient.history += [f"{money} € were received from another "
                              f"department."]

# baseball = Account('baseball', 1000)
# hiking = Account("hiking", 1500)
# Lena = Treasurer(baseball)
# Peter = Treasurer(hiking)

# Peter.transfer(250, baseball)

# print(baseball.balance, hiking.balance)

# Peter.make_withdraw(2000)

class App(tk.Frame):
    def __init__(self, frame):
        super().__init__(frame)
        
        frame.title("Cash Register")
        frame.geometry("500x400")
        
        # window grid
        frame.columnconfigure(0, weight=1)  # Center column
        frame.rowconfigure(0, weight=1)     # Center row
        self.login_page(frame)
        
        self.grid(row=0, column=0, sticky="nsew")
        
    def login_page(self, root):
        
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        
        container.columnconfigure(0, weight=1)  # Column for the label and input
        container.columnconfigure(1, weight=0)  # Column for the button
        container.rowconfigure(0, weight=0)  # Row for the label
        container.rowconfigure(1, weight=0)  # Row for input and button
        container.rowconfigure(2, weight=0)  # Row for the Quit button
        
        # Welcome text
        self.label = tk.Label(container, text="Welcome to the Club's Cash Registry!\nPlease enter your name to proceed!")
        self.label.grid(row=0, column=0, pady=20, columnspan=2)
        
        #box for button and login
        input_frame = tk.Frame(container)
        input_frame.grid(row=1, column=0, pady=10, columnspan=2)
        
        #Login box
        self.name = tk.StringVar()
        self.loginbox = tk.Entry(input_frame, textvariable=self.name)
        self.loginbox.grid(row=0, column=0, padx=5)
        
        # Button widget
        self.button = tk.Button(input_frame, text="Confirm", command=self.get_name)
        self.button.grid(row=0, column=1, padx=5)

        #Exit button
        self.button = tk.Button(text="Quit", command=root.destroy)
        self.button.grid(row=2, column=0, columnspan=2, pady=20)

    def get_name(self):
        '''
        function to retrieve the name used to log into the system
        '''
        
        print("Hello", self.name.get())
        name = self.name.get().lower()
        return name


    
