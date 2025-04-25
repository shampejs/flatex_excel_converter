import trade_class

class Sell(trade_class.Trade):
    def __init__(self, data):
        kind_of_transaction = "Verkauf"
        name = (next((line.split("Verkauf")[-1].split("(")[0].strip() for line in data.split("\n") if
                      line.startswith("Nr.") and "Verkauf" in line), ""))

        super().__init__(data, kind_of_transaction, name)

    def __str__(self):
        return "Sell"
