
def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float
    """
    total_revenue = 0.0

    for txn in transactions:
        total_revenue += txn['Quantity'] * txn['UnitPrice']

    return round(total_revenue, 2)


def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics
    """
    region_data = {}
    overall_sales = calculate_total_revenue(transactions)

    for txn in transactions:
        region = txn['Region']
        amount = txn['Quantity'] * txn['UnitPrice']

        if region not in region_data:
            region_data[region] = {
                'total_sales': 0.0,
                'transaction_count': 0
            }

        region_data[region]['total_sales'] += amount
        region_data[region]['transaction_count'] += 1

    
    for region in region_data:
        percentage = (region_data[region]['total_sales'] / overall_sales) * 100
        region_data[region]['percentage'] = round(percentage, 2)
        region_data[region]['total_sales'] = round(region_data[region]['total_sales'], 2)

 
    sorted_regions = dict(
        sorted(region_data.items(),
               key=lambda item: item[1]['total_sales'],
               reverse=True)
    )

    return sorted_regions


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns: list of tuples
    """
    product_stats = {}

    for txn in transactions:
        product = txn['ProductName']
        qty = txn['Quantity']
        revenue = qty * txn['UnitPrice']

        if product not in product_stats:
            product_stats[product] = {
                'total_quantity': 0,
                'total_revenue': 0.0
            }

        product_stats[product]['total_quantity'] += qty
        product_stats[product]['total_revenue'] += revenue

  
    result = []
    for product, stats in product_stats.items():
        result.append(
            (product,
             stats['total_quantity'],
             round(stats['total_revenue'], 2))
        )

  
    result.sort(key=lambda x: x[1], reverse=True)

    return result[:n]


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns: dictionary of customer statistics
    """
    customer_data = {}

    for txn in transactions:
        customer = txn['CustomerID']
        amount = txn['Quantity'] * txn['UnitPrice']
        product = txn['ProductName']

        if customer not in customer_data:
            customer_data[customer] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_bought': set()
            }

        customer_data[customer]['total_spent'] += amount
        customer_data[customer]['purchase_count'] += 1
        customer_data[customer]['products_bought'].add(product)


    for customer in customer_data:
        total = customer_data[customer]['total_spent']
        count = customer_data[customer]['purchase_count']

        customer_data[customer]['avg_order_value'] = round(total / count, 2)
        customer_data[customer]['total_spent'] = round(total, 2)
        customer_data[customer]['products_bought'] = list(
            customer_data[customer]['products_bought']
        )

  
    sorted_customers = dict(
        sorted(customer_data.items(),
               key=lambda item: item[1]['total_spent'],
               reverse=True)
    )

    return sorted_customers
