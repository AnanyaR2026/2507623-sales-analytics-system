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
            transaction = {}

            transaction['TransactionID'] = parts[0]
            transaction['Date'] = parts[1]
            transaction['ProductID'] = parts[2]
          
            transaction['ProductName'] = parts[3].replace(',', '')

            transaction['Quantity'] = int(parts[4].replace(',', ''))
            transaction['UnitPrice'] = float(parts[5].replace(',', ''))

            transaction['CustomerID'] = parts[6]
            transaction['Region'] = parts[7]

            transactions.append(transaction)

        except ValueError:
            continue

    return transactions
