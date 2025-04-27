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
        #kest = self.to_number(self.evaluate_regex(data, self.PATTERN_KEST))
        end_amount = -course*amount
        #end_amount = self.to_number(self.evaluate_regex(data, self.PATTERN_END_AMOUNT))

        super().__init__(data=data, date=date, name=name, kind_of_transaction=kind_of_transaction,
                         course=course, amount=amount, course_value=course*amount,
                         provision=0, own_expenses=0, foreign_expenses=0, kest=0,
                         end_amount=end_amount, winning=0)
