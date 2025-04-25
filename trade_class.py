import re

import transaction_class


class Trade(transaction_class.Transaction):
    PATTERN_COURSE_VALUE = r'.*Kurswert\s*:\s*(-?[\d.,]+)'
    PATTERN_PROVISION = r'.*Provision\s*:\s*(-?[\d.,]+)'
    PATTERN_END_AMOUNT = r'^\s*Endbetrag\s*:\s*(-?[\d.,]+)'
    PATTERN_REGULATION = r'.*Regulierung\s*:\s*(-?[\d.,]+)'
    PATTERN_OWN_EXPRESSION = r'.*Eigene Spesen\s*:\s*(-?[\d.,]+)'
    PATTERN_FOREIGN_EXPRESSION = r'.*Fremde Spesen\s*:\s*(-?[\d.,]+)'
    PATTERN_DATE = r'^Handelstag\s*(\d{2}\.\d{2}\.\d{4})'
    PATTERN_AMOUNT = r'^Ausgeführt\s*:\s*([\d]+)'
    PATTERN_COURSE = r'^Kurs\s*:\s*(-?[\d.,]+)'
    PATTERN_WINNING = r'^Gewinn/Verlust:\s*(-?[\d.,]+)'
    PATTERN_KEST = r'.*Einbeh\. KESt\s*:\s*(-?[\d.,]+)'

    def __init__(self, data,  kind_of_transaction, name):
        self.course_value = self.to_number(self.evaluate_regex(data, self.PATTERN_COURSE_VALUE))
        self.end_amount = self.to_number(self.evaluate_regex(data, self.PATTERN_END_AMOUNT))
        # in some cases these properties should be empty
        if kind_of_transaction:
            self.provision = self.to_number(self.evaluate_regex(data, self.PATTERN_PROVISION))
            self.regulation = self.to_number(self.evaluate_regex(data, self.PATTERN_REGULATION))
            self.own_expenses = self.to_number(self.evaluate_regex(data, self.PATTERN_OWN_EXPRESSION))
            self.foreign_expenses = self.to_number(self.evaluate_regex(data, self.PATTERN_FOREIGN_EXPRESSION))
            date = self.evaluate_regex(data, self.PATTERN_DATE)
        else:
            self.provision = None
            self.regulation = None
            self.own_expenses = None
            self.foreign_expenses = None
            date = "Zwischenergebnis"

        name = name
        kind_of_transaction = kind_of_transaction

        amount = self.to_number(self.evaluate_regex(data, self.PATTERN_AMOUNT))
        course = self.to_number(self.evaluate_regex(data, self.PATTERN_COURSE))
        end_amount = self.to_number(self.evaluate_regex(data, self.PATTERN_END_AMOUNT))
        winning = self.to_number(self.evaluate_regex(data, self.PATTERN_WINNING))
        kest = self.to_number(self.evaluate_regex(data, self.PATTERN_KEST))

        super().__init__(data=data, date=date, name=name, amount=amount, kind_of_transaction=kind_of_transaction,
                         course=course, end_amount=end_amount, winning=winning, kest=kest)


    @classmethod
    def init_for_billing(self, transaction: 'Transaction'):
        return self(
            data=transaction.data,
            kind_of_transaction=None,
            name=None
        )

    def print(self):
        print(self.data.split("Depotinhaber:")[1].split("*   Enthalten")[0].strip())

    def get_excel_format(self):
        return [self.date, self.name, self.kind_of_transaction, self.course, self.amount, self.course_value,
                self.provision, self.own_expenses, self.foreign_expenses, self.kest, self.end_amount, self.winning]

    def update_transaction(self, transaction):
        if transaction.kind_of_transaction == "Thesaurierung":
            self.course = self.course + transaction.kest / transaction.amount
            self.end_amount = self.end_amount + transaction.end_amount
            self.course_value = self.course_value + transaction.kest
        if transaction.kind_of_transaction == "Kauf":
            self.course = (self.course_value + transaction.course_value) / (self.amount + transaction.amount)
            self.amount = self.amount + transaction.amount
            self.end_amount = self.end_amount + transaction.end_amount
            self.course_value = self.course_value + transaction.course_value



