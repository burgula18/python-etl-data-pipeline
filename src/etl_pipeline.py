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
