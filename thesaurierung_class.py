import transaction_class

class Thesaurierung(transaction_class.Transaction):
    PATTERN_DATE = r'^\s*[A-Za-zäöüßÄÖÜ\s]+,\s*(\d{2}\.\d{2}\.\d{4})'
    PATTERN_NAME = r'^Nr\.\d+\s+(.*?)(?=\s*\(|$)'
    PATTERN_AMOUNT = r'^St\.\s*:\s*([\d]+)'
    PATTERN_COURSE = r'^\s*pro Stück\s*:\s*(-?[\d,]+)'
    PATTERN_EXCHANGE_RATE = r'^[A-ZA-z\s:.\d]*Devisenkurs\s*:\s*(-?[\d,]+)'
    PATTERN_KEST = r'.*Einbeh\. Steuer\s*:\s*(-?[\d,]+)'
    PATTERN_END_AMOUNT = r'^\s*Endbetrag\s*:\s*(-?[\d,]+)'

    def __init__(self, data):
        kind_of_transaction = "Thesaurierung"
        date = self.evaluate_regex(data, self.PATTERN_DATE)
        name = self.evaluate_regex(data, self.PATTERN_NAME)
        amount = self.to_number(self.evaluate_regex(data, self.PATTERN_AMOUNT))
        course = self.parse_course_with_exchange_rate(data, self.PATTERN_COURSE, self.PATTERN_EXCHANGE_RATE)
        kest = self.to_number(self.evaluate_regex(data, self.PATTERN_KEST))
        end_amount = self.to_number(self.evaluate_regex(data, self.PATTERN_END_AMOUNT))
        winning = None

        super().__init__(data, date, name, amount, kind_of_transaction, course, end_amount, winning, kest)
