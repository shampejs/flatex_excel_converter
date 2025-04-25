import re
from transaction_class import Transaction

class Dividend(Transaction):
    PATTERN_DATE = r'^\s*[A-Za-zäöüßÄÖÜ\s]+,\s*(\d{2}\.\d{2}\.\d{4})'
    PATTERN_NAME = r'^Nr\.\d+\s+(.*?)(?=\s*\(|$)'
    PATTERN_AMOUNT = r'^St\.\s*:\s*([\d]+)'
    PATTERN_COURSE = r'^\s*pro Stück\s*:\s*(-?[\d,]+)'
    PATTERN_EXCHANGE_RATE = r'^Devisenkurs\s*:\s*(-?[\d,]+)'
    PATTERN_KEST =  r'.*Einbeh\. Steuer\s*:\s*(-?[\d,]+)'
    PATTERN_END_AMOUNT = r'^\s*Endbetrag\s*:\s*(-?[\d,]+)'

    def __init__(self, data):
        self.data = data
        kind_of_transaction = "Dividende"
        date = self.evaluate_regex(data, self.PATTERN_DATE)
        name = self.evaluate_regex(data, self.PATTERN_NAME)
        amount = self.to_number(self.evaluate_regex(data, self.PATTERN_AMOUNT))
        course = self.parse_course_with_exchange_rate(data, self.PATTERN_COURSE, self.PATTERN_EXCHANGE_RATE)
        kest = self.to_number(self.evaluate_regex(data, self.PATTERN_KEST))
        winning = self.to_number(self.evaluate_regex(data, self.PATTERN_END_AMOUNT))

        super().__init__(data, date, name, amount, kind_of_transaction, course, winning, winning, kest)

    def print(self):
        print(self.data.split("Depotinhaber    :")[1].split("* Einbehaltene")[0].strip())

