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

baseball = Account('baseball', 1000)
hiking = Account("hiking", 1500)
Lena = Treasurer(baseball)
Peter = Treasurer(hiking)

Peter.transfer(250, baseball)

print(baseball.balance, hiking.balance)

Peter.make_withdraw(2000)