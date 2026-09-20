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
