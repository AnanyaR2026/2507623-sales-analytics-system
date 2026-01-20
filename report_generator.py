import os
from datetime import datetime
from collections import defaultdict

from utils.data_processor import (
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis
)

from utils.analysis import (
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products
)


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report
    """

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    total_records = len(transactions)
    total_revenue = calculate_total_revenue(transactions)
    avg_order_value = total_revenue / total_records if total_records else 0

    dates = [t['Date'] for t in transactions]
    date_range = f"{min(dates)} to {max(dates)}"

    region_stats = region_wise_sales(transactions)
    top_products = top_selling_products(transactions, n=5)
    customers = customer_analysis(transactions)
    daily_trend = daily_sales_trend(transactions)
    peak_day = find_peak_sales_day(transactions)
    low_products = low_performing_products(transactions)

    # API summary
    enriched_success = [t for t in enriched_transactions if t.get('API_Match')]
    enrichment_rate = (len(enriched_success) / len(enriched_transactions)) * 100 if enriched_transactions else 0

    failed_products = sorted({
        t['ProductName']
        for t in enriched_transactions
        if not t.get('API_Match')
    })

    # Average transaction value per region
    region_avg = {}
    for region, stats in region_stats.items():
        region_avg[region] = stats['total_sales'] / stats['transaction_count']

    with open(output_file, 'w', encoding='utf-8') as file:

        # 1. HEADER
        file.write("=" * 44 + "\n")
        file.write("           SALES ANALYTICS REPORT\n")
        file.write(f"     Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"     Records Processed: {total_records}\n")
        file.write("=" * 44 + "\n\n")

        # 2. OVERALL SUMMARY
        file.write("OVERALL SUMMARY\n")
        file.write("-" * 44 + "\n")
        file.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions:   {total_records}\n")
        file.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        file.write(f"Date Range:           {date_range}\n\n")

        # 3. REGION-WISE PERFORMANCE
        file.write("REGION-WISE PERFORMANCE\n")
        file.write("-" * 44 + "\n")
        file.write("Region    Sales         % of Total  Transactions\n")
        for region, stats in region_stats.items():
            file.write(
                f"{region:<9} ₹{stats['total_sales']:>10,.0f}     "
                f"{stats['percentage']:>6.2f}%      {stats['transaction_count']}\n"
            )
        file.write("\n")

        # 4. TOP 5 PRODUCTS
        file.write("TOP 5 PRODUCTS\n")
        file.write("-" * 44 + "\n")
        file.write("Rank  Product Name        Qty Sold   Revenue\n")
        for i, (name, qty, rev) in enumerate(top_products, 1):
            file.write(f"{i:<5} {name:<18} {qty:<10} ₹{rev:,.2f}\n")
        file.write("\n")

        # 5. TOP 5 CUSTOMERS
        file.write("TOP 5 CUSTOMERS\n")
        file.write("-" * 44 + "\n")
        file.write("Rank  Customer ID   Total Spent   Orders\n")
        for i, (cid, data) in enumerate(list(customers.items())[:5], 1):
            file.write(
                f"{i:<5} {cid:<13} ₹{data['total_spent']:,.2f}   {data['purchase_count']}\n"
            )
        file.write("\n")

        # 6. DAILY SALES TREND
        file.write("DAILY SALES TREND\n")
        file.write("-" * 44 + "\n")
        file.write("Date         Revenue       Txns   Customers\n")
        for date, data in daily_trend.items():
            file.write(
                f"{date}  ₹{data['revenue']:>10,.2f}   "
                f"{data['transaction_count']:<5}   {data['unique_customers']}\n"
            )
        file.write("\n")

        # 7. PRODUCT PERFORMANCE ANALYSIS
        file.write("PRODUCT PERFORMANCE ANALYSIS\n")
        file.write("-" * 44 + "\n")
        file.write(f"Best Selling Day: {peak_day[0]} "
                   f"(₹{peak_day[1]:,.2f}, {peak_day[2]} transactions)\n\n")

        if low_products:
            file.write("Low Performing Products:\n")
            for name, qty, rev in low_products:
                file.write(f"- {name}: {qty} units, ₹{rev:,.2f}\n")
        else:
            file.write("No low performing products found.\n")

        file.write("\nAverage Transaction Value per Region:\n")
        for region, value in region_avg.items():
            file.write(f"- {region}: ₹{value:,.2f}\n")
        file.write("\n")

        # 8. API ENRICHMENT SUMMARY
        file.write("API ENRICHMENT SUMMARY\n")
        file.write("-" * 44 + "\n")
        file.write(f"Total Records Enriched: {len(enriched_success)}\n")
        file.write(f"Success Rate: {enrichment_rate:.2f}%\n")

        if failed_products:
            file.write("Products Not Enriched:\n")
            for p in failed_products:
                file.write(f"- {p}\n")
        else:
            file.write("All products enriched successfully.\n")

    print(f"Sales report generated successfully at: {output_file}")
