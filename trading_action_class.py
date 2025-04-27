import script
from transaction_class import Transaction
import os


def convert_data_format_to_basic_iso_8601_format(value):
    day, month, year = value.split('.')
    return f"{year}{month}{day}"


class TradingAction(Transaction):
    def __init__(self, transaction: Transaction):
        super().__init__(data=None, date="Zwischenergebnis", name=None, kind_of_transaction=None,
                         course=transaction.course, amount=transaction.amount, course_value=transaction.course_value,
                         provision=transaction.provision, own_expenses=transaction.own_expenses,
                         foreign_expenses=transaction.foreign_expenses, kest=transaction.kest,
                         end_amount=transaction.end_amount, winning=transaction.winning)

    def update_transaction(self, transaction):

        if transaction.kind_of_transaction == "Thesaurierung":
            self.update_expenses(transaction)
            self.course = (self.course_value + transaction.course_value) / self.amount
            self.end_amount = self.end_amount + transaction.end_amount
            self.course_value = self.course_value + transaction.course_value
        if transaction.kind_of_transaction == "Kauf":
            self.update_expenses(transaction)
            self.course = (self.course_value + transaction.course_value) / (self.amount + transaction.amount)
            self.amount = self.amount + transaction.amount
            self.end_amount = self.end_amount + transaction.end_amount
            self.course_value = self.course_value + transaction.course_value
        if transaction.kind_of_transaction == "Verkauf":
            old_amount = self.amount
            old_course_value = self.course_value
            self.amount -= transaction.amount
            if self.amount == 0:
                self.course = 0
            self.course_value = self.course * self.amount
            self.provision *= (self.amount / old_amount)
            self.own_expenses *= (self.amount / old_amount)
            self.foreign_expenses *= (self.amount / old_amount)
            self.kest *= (self.amount / old_amount)
            self.end_amount += old_course_value - self.course_value
        if transaction.kind_of_transaction == "Dividende":
            manual_correction = self.get_manual_correction(transaction)
            old_course_value = self.course_value
            if manual_correction:
                self.course = manual_correction
            else:
                self.course -= transaction.course
            self.course_value = self.course * self.amount
            change = round(old_course_value - self.course_value, 2)
            self.end_amount += change

    def update_expenses(self, transaction):
        self.provision += transaction.provision
        self.own_expenses += transaction.own_expenses
        self.foreign_expenses += transaction.foreign_expenses
        self.kest += transaction.kest

    def pre_selling_calculation(self, transaction):
        old_amount = self.amount
        self.date = ""
        self.update_expenses(transaction)
        self.amount = transaction.amount
        self.course_value = self.course * self.amount
        self.end_amount *= (self.amount / old_amount)

    def selling_result(self, transaction):
        old_amount = self.amount
        self.date = "Ergebnis"
        self.course = transaction.course - self.course
        self.amount = transaction.amount
        self.course_value = round(self.course * self.amount, 2)
        self.provision *= (old_amount / self.amount)
        self.own_expenses *= (old_amount / self.amount)
        self.foreign_expenses *= (old_amount / self.amount)
        self.kest *= (old_amount / self.amount)
        self.end_amount = self.end_amount + transaction.end_amount

    def get_manual_correction(self, transaction):
        date_of_transaction = convert_data_format_to_basic_iso_8601_format(transaction.date)
        file_names = [script.PATH + f for f in os.listdir(script.PATH) if
                      f.startswith(date_of_transaction) and f.lower().endswith('.txt')]
        if len(file_names) != 1:
            return None
        with open(file_names[0]) as f:

            for line in f.read().split("\n"):
                name, new_course = line.split(";")
                if transaction.name == name:
                    return self.to_number(new_course)

        return None
