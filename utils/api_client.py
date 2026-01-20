def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """

    enriched_transactions = []

    for txn in transactions:
        enriched_txn = txn.copy()

        try:
            product_id_str = txn.get('ProductID', '')
            numeric_id = int(''.join(filter(str.isdigit, product_id_str)))

            api_product = product_mapping.get(numeric_id)

            if api_product:
                enriched_txn['API_Category'] = api_product.get('category')
                enriched_txn['API_Brand'] = api_product.get('brand')
                enriched_txn['API_Rating'] = api_product.get('rating')
                enriched_txn['API_Match'] = True
            else:
                enriched_txn['API_Category'] = None
                enriched_txn['API_Brand'] = None
                enriched_txn['API_Rating'] = None
                enriched_txn['API_Match'] = False

        except Exception:
            enriched_txn['API_Category'] = None
            enriched_txn['API_Brand'] = None
            enriched_txn['API_Rating'] = None
            enriched_txn['API_Match'] = False

        enriched_transactions.append(enriched_txn)


import os
def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file
    """

   
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    headers = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region',
        'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
    ]

    with open(filename, 'w', encoding='utf-8') as file:
        file.write('|'.join(headers) + '\n')

        for txn in enriched_transactions:
            row = []
            for field in headers:
                value = txn.get(field)
                row.append(str(value) if value is not None else '')
            file.write('|'.join(row) + '\n')


 
    save_enriched_data(enriched_transactions)

    return enriched_transactions
