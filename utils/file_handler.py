"""
utils/file_handler.py

Implements:
- Task 1.1: Read sales data with encoding handling
- Task 1.2: Parse and clean data
- Task 1.3: Validate and filter data
"""


def read_sales_data(filename):

    encodings = ['utf-8', 'latin-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                lines = file.readlines()

               
                raw_lines = [
                    line.strip()
                    for line in lines[1:]
                    if line.strip()
                ]

               
                if 50 <= len(raw_lines) <= 100:
                    return raw_lines
                else:
                    print(f"Warning: {len(raw_lines)} records read using {encoding}")

        except UnicodeDecodeError:
            continue

        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    print("Error: Unsupported file encoding.")
    return []



def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries
    """

    transactions = []

    headers = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region'
    ]

    for line in raw_lines:
        parts = line.split('|')

        
        if len(parts) != len(headers):
            continue

        try:
            transaction = {
                'TransactionID': parts[0],
                'Date': parts[1],
                'ProductID': parts[2],
                'ProductName': parts[3].replace(',', ''),
                'Quantity': int(parts[4].replace(',', '')),
                'UnitPrice': float(parts[5].replace(',', '')),
                'CustomerID': parts[6],
                'Region': parts[7]
            }

            transactions.append(transaction)

        except ValueError:
           
            continue

    return transactions


def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters
    """

    valid_transactions = []
    invalid_count = 0

    regions = set()
    amounts = []

    for txn in transactions:
        try:
            if (
                txn['Quantity'] <= 0 or
                txn['UnitPrice'] <= 0 or
                not txn['TransactionID'].startswith('T') or
                not txn['ProductID'].startswith('P') or
                not txn['CustomerID'].startswith('C')
            ):
                invalid_count += 1
                continue

            amount = txn['Quantity'] * txn['UnitPrice']
            txn['Amount'] = amount

            regions.add(txn['Region'])
            amounts.append(amount)

            valid_transactions.append(txn)

        except KeyError:
            invalid_count += 1

 
    if amounts:
        print("Available Regions:", sorted(regions))
        print(f"Transaction Amount Range: {min(amounts):.2f} – {max(amounts):.2f}")

    filtered_by_region = 0
    filtered_by_amount = 0


    if region:
        before = len(valid_transactions)
        valid_transactions = [
            txn for txn in valid_transactions
            if txn['Region'] == region
        ]
        filtered_by_region = before - len(valid_transactions)
        print(f"After region filter ({region}): {len(valid_transactions)}")

    if min_amount is not None:
        before = len(valid_transactions)
        valid_transactions = [
            txn for txn in valid_transactions
            if txn['Amount'] >= min_amount
        ]
        filtered_by_amount += before - len(valid_transactions)

    if max_amount is not None:
        before = len(valid_transactions)
        valid_transactions = [
            txn for txn in valid_transactions
            if txn['Amount'] <= max_amount
        ]
        filtered_by_amount += before - len(valid_transactions)

    print(f"After amount filter: {len(valid_transactions)}")


    filter_summary = {
        'total_input': len(transactions),
        'invalid': invalid_count,
        'filtered_by_region': filtered_by_region,
        'filtered_by_amount': filtered_by_amount,
        'final_count': len(valid_transactions)
    }

    return valid_transactions, invalid_count, filter_summary
