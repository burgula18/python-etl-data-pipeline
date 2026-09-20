import pandas as pd
import logging
from pathlib import Path


# -----------------------------
# File Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

CUSTOMERS_FILE = RAW_DATA_DIR / "customers.csv"
ORDERS_FILE = RAW_DATA_DIR / "orders.csv"
PRODUCTS_FILE = RAW_DATA_DIR / "products.csv"


# -----------------------------
# Extract
# -----------------------------

def extract_data():
    """Read raw CSV files into Pandas DataFrames."""

    customers = pd.read_csv(CUSTOMERS_FILE)
    orders = pd.read_csv(ORDERS_FILE)
    products = pd.read_csv(PRODUCTS_FILE)

    print("Customers loaded:", len(customers))
    print("Orders loaded:", len(orders))
    print("Products loaded:", len(products))

    return customers, orders, products

# -----------------------------
# Clean
# -----------------------------

def clean_data(customers, orders, products):
    """Clean raw datasets before transformation."""

    # Remove duplicate records
    customers = customers.drop_duplicates()
    orders = orders.drop_duplicates()
    products = products.drop_duplicates()

    # Clean column names
    customers.columns = customers.columns.str.strip().str.lower()
    orders.columns = orders.columns.str.strip().str.lower()
    products.columns = products.columns.str.strip().str.lower()

    # Handle missing customer values
    if "state" in customers.columns:
        customers["state"] = customers["state"].fillna("Unknown")

    # Convert order date to datetime
    orders["order_date"] = pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    # Ensure numeric columns contain numeric values
    orders["quantity"] = pd.to_numeric(
        orders["quantity"],
        errors="coerce"
    )

    orders["unit_price"] = pd.to_numeric(
        orders["unit_price"],
        errors="coerce"
    )

    # Remove records missing critical identifiers
    customers = customers.dropna(subset=["customer_id"])
    orders = orders.dropna(
        subset=["order_id", "customer_id", "product_id"]
    )
    products = products.dropna(subset=["product_id"])

    print("Data cleaning completed.")

    return customers, orders, products

# -----------------------------
# Transform
# -----------------------------

def transform_data(customers, orders, products):
    """Apply business transformations to the datasets."""

    # Calculate total amount for each order
    orders["order_amount"] = (
        orders["quantity"] * orders["unit_price"]
    )

    # Standardize order status
    orders["status"] = (
        orders["status"]
        .str.strip()
        .str.title()
    )

    # Create order year and month for reporting
    orders["order_year"] = orders["order_date"].dt.year
    orders["order_month"] = orders["order_date"].dt.month

    # Create a customer full name if first/last name columns exist
    if {"first_name", "last_name"}.issubset(customers.columns):
        customers["customer_name"] = (
            customers["first_name"].fillna("").str.strip()
            + " "
            + customers["last_name"].fillna("").str.strip()
        ).str.strip()

    print("Data transformation completed.")

    return customers, orders, products

# -----------------------------
# Join / Merge
# -----------------------------

def join_data(customers, orders, products):
    """Join customer, order, and product datasets."""

    # Join orders with customer information
    customer_orders = orders.merge(
        customers,
        on="customer_id",
        how="left"
    )

    # Join the result with product information
    enriched_orders = customer_orders.merge(
        products,
        on="product_id",
        how="left",
        suffixes=("_order", "_product")
    )

    print("Data joins completed.")
    print("Enriched order records:", len(enriched_orders))

    return enriched_orders

# -----------------------------
# Data Validation
# -----------------------------

def validate_data(enriched_orders):
    """Validate the transformed and joined dataset."""

    print("Starting data validation...")

    # 1. Check for duplicate orders
    duplicate_orders = enriched_orders["order_id"].duplicated().sum()

    # 2. Check for missing critical values
    missing_order_ids = enriched_orders["order_id"].isna().sum()
    missing_customer_ids = enriched_orders["customer_id"].isna().sum()
    missing_product_ids = enriched_orders["product_id"].isna().sum()

    # 3. Validate quantity and price
    invalid_quantity = (enriched_orders["quantity"] <= 0).sum()
    invalid_price = (enriched_orders["unit_price"] < 0).sum()

    # 4. Validate calculated order amount
    invalid_order_amount = (enriched_orders["order_amount"] < 0).sum()

    # 5. Check for invalid order dates
    invalid_dates = enriched_orders["order_date"].isna().sum()

    # Display validation results
    print("Validation Results")
    print("------------------")
    print("Duplicate orders:", duplicate_orders)
    print("Missing order IDs:", missing_order_ids)
    print("Missing customer IDs:", missing_customer_ids)
    print("Missing product IDs:", missing_product_ids)
    print("Invalid quantities:", invalid_quantity)
    print("Invalid unit prices:", invalid_price)
    print("Invalid order amounts:", invalid_order_amount)
    print("Invalid order dates:", invalid_dates)

    # Overall validation result
    total_errors = (
        duplicate_orders
        + missing_order_ids
        + missing_customer_ids
        + missing_product_ids
        + invalid_quantity
        + invalid_price
        + invalid_order_amount
        + invalid_dates
    )

    if total_errors == 0:
        print("Data validation PASSED.")
    else:
        print(f"Data validation found {total_errors} issue(s).")

    return total_errors

# -----------------------------
# Load
# -----------------------------

def load_data(enriched_orders):
    """Load the final processed dataset to the processed data folder."""

    # Create processed directory if it does not exist
    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Define output file
    output_file = PROCESSED_DATA_DIR / "enriched_orders.csv"

    # Write processed DataFrame to CSV
    enriched_orders.to_csv(
        output_file,
        index=False
    )

    print("Data load completed.")
    print(f"Processed file created: {output_file}")

    return output_file

# ------------------------------
# Step 7: Run ETL Pipeline
# ------------------------------

def run_pipeline():
    """Run the complete ETL pipeline."""

    print("Starting Python ETL Pipeline...")

    # Step 1 - Extract
    customers, orders, products = extract_data()

    # Step 2 - Clean
    customers, orders, products = clean_data(
        customers,
        orders,
        products
    )   
    
    # Step 3 - Transform
    customers, orders, products = transform_data(
        customers,
        orders,
        products
    )

    # Step 4 - Join datasets
    enriched_orders = join_data(
        orders,
        customers,
        products
    )

    # Step 5 - Validate
    validate_data(enriched_orders)

    # Step 6 - Load
    output_file = load_data(enriched_orders)

    print("ETL Pipeline completed successfully.")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    run_pipeline()
