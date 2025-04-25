import os

import dividend_class
import excel_generater
import sell_class
import thesaurierung_class
import buy_class

from pypdf import PdfReader

def create_transaction_from_file(path):
    reader = PdfReader(path)
    first_page = reader.pages[0].extract_text()
    if path.split("_")[1].startswith("Kauf"):
        transaction = buy_class.Buy(first_page)
    elif path.split("_")[1].startswith("Verkauf"):
        transaction = sell_class.Sell(first_page)
    elif path.split("_")[1] == "Fondsertragsausschuettung":
        transaction = dividend_class.Dividend(first_page)
    elif path.split("_")[1] == "Fondsthesaurierung":
        transaction = thesaurierung_class.Thesaurierung(first_page)
    else:
        transaction = None

    return transaction

# Rows should be colered depending on the name of the transaction.
# Therefore, a map with key = name, value = number starting from 0 is created
# This map is later used to get a color from the colors array
def translate_name_to_number(transactions):
    name_to_number = {}
    next_number = 0
    for transaction in transactions:
        name = transaction.name
        if name and name not in name_to_number:  # Added a check for None/empty typ
            name_to_number[name] = next_number
            next_number += 1
    return name_to_number

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    PATH = "pdfs/"
    file_names = [PATH + f for f in os.listdir(PATH) if f.lower().endswith('.pdf')]
    print(file_names)

    transactions = []
    for file_name in file_names:
        transactions.append(create_transaction_from_file(file_name))

    transaction_name_map = translate_name_to_number(transactions)
    excel_generater.create_excel_file(transactions, transaction_name_map)
