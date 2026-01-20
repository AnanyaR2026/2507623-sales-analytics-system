def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns: dictionary sorted by date
    """

    daily_data = defaultdict(lambda: {
        'revenue': 0.0,
        'transaction_count': 0,
        'unique_customers': set()
    })

    for txn in transactions:
        date = txn.get('Date')
        customer = txn.get('CustomerID')
        amount = txn['Quantity'] * txn['UnitPrice']

        daily_data[date]['revenue'] += amount
        daily_data[date]['transaction_count'] += 1
        daily_data[date]['unique_customers'].add(customer)

   
    sorted_daily_data = {}

    for date in sorted(daily_data.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d")):
        sorted_daily_data[date] = {
            'revenue': round(daily_data[date]['revenue'], 2),
            'transaction_count': daily_data[date]['transaction_count'],
            'unique_customers': len(daily_data[date]['unique_customers'])
        }

    return sorted_daily_data


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns: tuple (date, revenue, transaction_count)
    """

    daily_revenue = defaultdict(lambda: {
        'revenue': 0.0,
        'transaction_count': 0
    })

    for txn in transactions:
        date = txn['Date']
        amount = txn['Quantity'] * txn['UnitPrice']

        daily_revenue[date]['revenue'] += amount
        daily_revenue[date]['transaction_count'] += 1

    peak_date = None
    max_revenue = 0.0
    peak_txn_count = 0

    for date, data in daily_revenue.items():
        if data['revenue'] > max_revenue:
            max_revenue = data['revenue']
            peak_date = date
            peak_txn_count = data['transaction_count']

    return (peak_date, round(max_revenue, 2), peak_txn_count)



def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns: list of tuples
    (ProductName, TotalQuantity, TotalRevenue)
    """

    product_stats = defaultdict(lambda: {
        'quantity': 0,
        'revenue': 0.0
    })

    for txn in transactions:
        product = txn['ProductName']
        quantity = txn['Quantity']
        revenue = quantity * txn['UnitPrice']

        product_stats[product]['quantity'] += quantity
        product_stats[product]['revenue'] += revenue

    low_performers = []

    for product, stats in product_stats.items():
        if stats['quantity'] < threshold:
            low_performers.append(
                (
                    product,
                    stats['quantity'],
                    round(stats['revenue'], 2)
                )
            )


    low_performers.sort(key=lambda x: x[1])

    return low_performers
