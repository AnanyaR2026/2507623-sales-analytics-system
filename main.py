from utils.file_handler import read_sales_data, parse_transactions, validate_and_filter
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
from utils.api_client import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data
)
from utils.report_generator import generate_sales_report


def main():
    """
    Main execution function
    """

    try:
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)

        # 1. Read sales data
        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        # 2. Parse and clean
        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        # 3. Show filter options
        regions = sorted({t['Region'] for t in transactions})
        amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]

        print("\n[3/10] Filter Options Available:")
        print("Regions:", ", ".join(regions))
        print(f"Amount Range: ₹{int(min(amounts)):,} - ₹{int(max(amounts)):,}")

        apply_filter = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region_filter = None
        min_amount = None
        max_amount = None

        if apply_filter == 'y':
            region_filter = input("Enter region (or press Enter to skip): ").strip() or None

            try:
                min_amount = input("Enter minimum amount (or press Enter to skip): ")
                min_amount = float(min_amount) if min_amount else None

                max_amount = input("Enter maximum amount (or press Enter to skip): ")
                max_amount = float(max_amount) if max_amount else None
            except ValueError:
                print("Invalid amount entered. Skipping amount filter.")

        # 4. Validate and filter
        print("\n[4/10] Validating transactions...")
        valid_transactions, invalid_count, summary = validate_and_filter(
            transactions,
            region=region_filter,
            min_amount=min_amount,
            max_amount=max_amount
        )

        print(f"✓ Valid: {len(valid_transactions)} | Invalid: {invalid_count}")

        # 5. Analysis
        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_transactions)
        region_wise_sales(valid_transactions)
        top_selling_products(valid_transactions)
        customer_analysis(valid_transactions)
        daily_sales_trend(valid_transactions)
        find_peak_sales_day(valid_transactions)
        low_performing_products(valid_transactions)
        print("✓ Analysis complete")

        # 6. Fetch API data
        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        print(f"✓ Fetched {len(api_products)} products")

        # 7. Enrich sales data
        print("\n[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(valid_transactions, product_mapping)

        enriched_count = sum(1 for t in enriched_transactions if t['API_Match'])
        success_rate = (enriched_count / len(enriched_transactions)) * 100 if enriched_transactions else 0
        print(f"✓ Enriched {enriched_count}/{len(enriched_transactions)} transactions ({success_rate:.1f}%)")

        # 8. Save enriched data
        print("\n[8/10] Saving enriched data...")
        print("✓ Saved to: data/enriched_sales_data.txt")

        # 9. Generate report
        print("\n[9/10] Generating report...")
        generate_sales_report(valid_transactions, enriched_transactions)
        print("✓ Report saved to: output/sales_report.txt")

        # 10. Complete
        print("\n[10/10] Process Complete!")
        print("=" * 40)

    except Exception as e:
        print("\n❌ An error occurred during execution.")
        print("Details:", str(e))

if __name__ == "__main__":
    main()
