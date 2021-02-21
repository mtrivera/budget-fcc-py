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
    result = ["Percentage spent by category\n"]
    withdrawals = [abs(c.ledger[1]["amount"]) for c in categories]
    percents = [get_percent(w, withdrawals) for w in withdrawals]
    category_names = [c.name for c in categories]
    first_category_index, second_category_index, third_category_index = 5, 8, 11
    col_limit = 14

    # Draw legend and plot bar charts
    for i in range(100, -10, -10):
        result.append(f"{str(i).rjust(3, ' ')}|")
        for j in range(4, col_limit):
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
    largest_name = max(len(name) for name in category_names)
    new_category_names = update_names(category_names, largest_name)

    # Draw category names
    for i in range(largest_name):
        for a in range(col_limit):
            if a == first_category_index:
                result.append(new_category_names[0][i])
            elif a == second_category_index:
                result.append(new_category_names[1][i])
            elif a == third_category_index:
                result.append(new_category_names[2][i])
            else:
                result.append(' ')
        result.append('\n')

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