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

    def __init__(self, data, kind_of_transaction, name):
        date = self.evaluate_regex(data, self.PATTERN_DATE)
        course = self.to_number(self.evaluate_regex(data, self.PATTERN_COURSE))
        amount = self.to_number(self.evaluate_regex(data, self.PATTERN_AMOUNT))
        course_value = self.to_number(self.evaluate_regex(data, self.PATTERN_COURSE_VALUE))
        provision = self.to_number(self.evaluate_regex(data, self.PATTERN_PROVISION))
        own_expenses = self.to_number(self.evaluate_regex(data, self.PATTERN_OWN_EXPRESSION))
        foreign_expenses = self.to_number(self.evaluate_regex(data, self.PATTERN_FOREIGN_EXPRESSION))
        end_amount = self.to_number(self.evaluate_regex(data, self.PATTERN_END_AMOUNT))
        winning = self.to_number(self.evaluate_regex(data, self.PATTERN_WINNING))
        kest = self.to_number(self.evaluate_regex(data, self.PATTERN_KEST))

        super().__init__(data=data, date=date, name=name, kind_of_transaction=kind_of_transaction,
                         course=course, amount=amount, course_value=course_value,
                         provision=provision, own_expenses=own_expenses, foreign_expenses=foreign_expenses, kest=kest,
                         end_amount=end_amount, winning=winning)

    def print(self):
        print(self.data.split("Depotinhaber:")[1].split("*   Enthalten")[0].strip())

    def get_excel_format(self):
        return [self.date, self.name, self.kind_of_transaction, self.course, self.amount, self.course_value,
                self.provision, self.own_expenses, self.foreign_expenses, self.kest, self.end_amount, self.winning]
