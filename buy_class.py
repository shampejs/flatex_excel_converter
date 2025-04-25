import trade_class

class Buy(trade_class.Trade):
    def __init__(self, data):
        kind_of_transaction = "Kauf"
        name = (next((line.split("Kauf")[-1].split("(")[0].strip() for line in data.split("\n") if
                           line.startswith("Nr.") and "Kauf" in line), ""))

        super().__init__(data, kind_of_transaction, name)

    def __str__(self):
        return "Buy"