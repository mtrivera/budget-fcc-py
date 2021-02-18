class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.balance = 0

    def __str__(self):
        char_limit, left_char_limit, right_char_limit = 30, 23, 7
        ledger = self.ledger.copy()
        result = [self.name.center(char_limit, '*')]
        while len(ledger) > 0:
            transaction = ledger.pop(0)
            result.append(
                transaction["description"][:left_char_limit].ljust(left_char_limit) +
                format(transaction["amount"], '.2f').rjust(right_char_limit)
            )
        result.append("Total: " + str(self.get_balance()))
        return "\n".join(result)

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
