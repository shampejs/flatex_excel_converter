import re

class Transaction:
    def __init__(self, data, date, name, amount, kind_of_transaction, course,course_value,provision,own_expenses,foreign_expenses, end_amount, winning, kest):
        self.data = data
        self.date = date
        self.name = name
        self.kind_of_transaction = kind_of_transaction
        self.course = course
        self.amount = amount
        self.course_value = course_value
        self.provision = provision
        self.own_expenses = own_expenses
        self.foreign_expenses = foreign_expenses
        self.end_amount = end_amount
        self.winning = winning
        self.kest = kest



    def print(self):
        print("Generic Transaction print !")

    def get_excel_format(self):
        return [self.date, self.name, self.kind_of_transaction, self.course, self.amount, self.course_value,
                self.provision, self.own_expenses, self.foreign_expenses, self.kest, self.end_amount, self.winning]

    def evaluate_regex(self, content, regex):
        return next((match.group(1) for line in content.split("\n") if (match := re.match(regex, line))), "")

    def to_number(self, value):
        return float(value.replace(".", "").replace(',', '.'))

    def parse_course_with_exchange_rate(self, data, pattern_course, pattern_exchange_rate):
        value = self.evaluate_regex(data, pattern_course)
        exchange_rate = self.evaluate_regex(data, pattern_exchange_rate)
        return round(self.to_number(value) / self.to_number(exchange_rate), 4)


