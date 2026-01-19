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


    print("Available Regions:", sorted(regions))
    print(f"Transaction Amount Range: {min(amounts):.2f} - {max(amounts):.2f}")

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
