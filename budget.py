class Category:
    def __init__(self, name) -> None:
        self.ledger = []
        self.name = name

    def __str__(self):
        title_line = 30 - len(self.name)
        custom_string = (
            "*" * (title_line // 2) + self.name.title() + "*" * (title_line // 2)
        )
        for entries in self.ledger:
            spaces = spaces = (
                ""
                if len(entries["description"][:23]) > 23
                else " " * (23 - len(entries["description"][:23]))
            )
            custom_string += (
                f"\n{entries['description'][:23]}{spaces}{entries['amount']:>7.2f}"
            )

        custom_string += "\nTotal: " + str(self.get_balance())

        return custom_string

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True

        return False

    def transfer(self, amount, new_category):
        if self.check_funds(amount):
            self.ledger.append(
                {
                    "amount": -amount,
                    "description": "Transfer to " + new_category.name.title(),
                }
            )
            new_category.deposit(amount, "Transfer from " + self.name.title())
            return True

        return False

    def get_balance(self):
        balance = 0
        for entries in self.ledger:
            balance += entries["amount"]

        return balance

    def check_funds(self, amount):
        if amount > self.get_balance():
            return False

        return True

    def get_withdrawals(self):
        spent = 0

        for entries in self.ledger:
            if entries["amount"] < 0:
                spent += entries["amount"]

        return spent


def get_totals(categories):
    total = 0
    balances = []
    percentages = []

    for category in categories:
        total += category.get_withdrawals()
        balances.append(category.get_withdrawals())

    for num in balances:
        percentages.append(num / total)

    return percentages


def create_spend_chart(categories):
    # take list of categories as an argument. It should return a string that is a bar chart showing what percentage of spending each category represents

    custom_string = "Percentage spent by category\n"

    i = 100
    totals = get_totals(categories)
    while i >= 0:
        spaces = " "
        for percent in totals:
            if percent * 100 >= i:
                spaces += "o  "
            else:
                spaces += "   "

        custom_string += str(i).rjust(3) + "|" + spaces + "\n"
        i -= 10

    dashes = "-" + "---" * len(categories)
    names = []
    x_axis = ""

    for category in categories:
        names.append(category.name.title())

    # search names list for longest category name
    longest = max(names, key=len)

    for x in range(len(longest)):
        name_str = "     "

        # loop through names, print character in name at index x, if we have already higher than length of the name we just add buffer space
        for name in names:
            if x >= len(name):
                name_str += "   "
            else:
                name_str += name[x] + "  "

        if x != len(longest) - 1:
            name_str += "\n"

        x_axis += name_str

    custom_string += dashes.rjust(len(dashes) + 4) + "\n" + x_axis
    return custom_string
