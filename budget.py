class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.balance = 0

    # TODO: Implement magic method '__str__' for printing a budget object

    def deposit(self, amount, description=''):
        self.ledger.append({"amount": amount, "description": description})
        self.set_balance(amount)

    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({"amount": -abs(amount), "description": description})
            self.set_balance(-abs(amount))
            return True
        return False

    def transfer(self, amount, category):
        if isinstance(category, Category):
            if self.check_funds(amount):
                self.withdraw(amount, f'Transfer to {category.name}')
                category.deposit(amount, f'Transfer from {self.name}')
                return True
            return False

    def set_balance(self, amount):
        self.balance += amount

    def get_balance(self):
        return self.balance

    def check_funds(self, amount):
        return self.get_balance() >= amount


def create_spend_chart(categories):
    pass
