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

#TODO: Refactor and comment
def create_spend_chart(categories):
    budgets = categories.copy()
    result = ["Percentage spent by category\n"]
    withdrawals, percents = [], []
    first_category_index, second_category_index, third_category_index = 5, 8, 11

    for b in budgets:
        withdrawals.append(abs((b.ledger[1]["amount"])))

    for w in withdrawals:
        percents.append(get_percent(w, withdrawals))

    for i in range(100, -10, -10):
        result.append(f"{str(i).rjust(3, ' ')}|")
        for j in range(4, 14):
            # First category
            if j == first_category_index and percents[0] >= i:
                result.append('o')
            # Second category
            elif j == second_category_index and percents[1] >= i:
                result.append('o')
            # Third category
            elif j == third_category_index and percents[2] >= i:
                result.append('o')
            else:
                result.append(' ')
        result.append('\n')

    result.append('    ' + '-' * 10 + '\n')   # create dash line

    largest_name = max(len(c.name) for c in categories)

    first_name, second_name, third_name = budgets[0].name, budgets[1].name, budgets[2].name

    names = update_names([first_name, second_name, third_name], largest_name)

    for i in range(largest_name):
        for a in range(14):
            if a == first_category_index:
                result.append(names[0][i])
            elif a == second_category_index:
                result.append(names[1][i])
            elif a == third_category_index:
                result.append(names[2][i])
            else:
                result.append(' ')
        result.append("\n")

    return ("".join(result)).rstrip('\n')

def update_names(names, largest):
    result = []
    for name in names:
        if len(name) >= largest:
            result.append(name)
        else:
            result.append(name + (largest - len(name)) * ' ')
    return result

def get_percent(num, list):
    return int(num / sum(list) * 100)