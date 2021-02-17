class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.balance = 0

    def deposit(self, amount, description=''):
        self.ledger.append({amount: amount, description: description})

def create_spend_chart(categories):
    pass