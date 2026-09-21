# Python ETL Data Pipeline

An end-to-end ETL (Extract, Transform, Load) data engineering project built using **Python and Pandas**.

The project demonstrates how raw customer, order, and product datasets can be extracted, cleaned, transformed, joined, validated, and loaded into a processed dataset for downstream analytics and reporting.

## Project Architecture

Raw CSV Files  
↓  
Extract Data  
↓  
Clean Data  
↓  
Transform Data  
↓  
Join / Merge Datasets  
↓  
Data Validation  
↓  
Load Processed Dataset

## Project Structure

python-etl-data-pipeline/

    data/
        raw/
            customers.csv
            orders.csv
            products.csv

        processed/
            enriched_orders.csv

    src/
        etl_pipeline.py

    requirements.txt
    README.md

## Technologies Used

- Python
- Pandas
- CSV
- Git
- GitHub
- GitHub Codespaces

## Source Data

The pipeline processes three source datasets.

### customers.csv

Contains customer information used to enrich order records.

Example attributes include:

- customer_id
- customer name information
- customer attributes

### orders.csv

Contains transactional order information including:

- order_id
- customer_id
- product_id
- order_date
- product_category
- quantity
- unit_price
- status

### products.csv

Contains product reference information used to enrich orders.

Example attributes include:

- product_id
- product details
- product category information

## ETL Pipeline

The complete ETL workflow is implemented in:

`src/etl_pipeline.py`

### 1. Extract

The pipeline reads the raw CSV datasets using Pandas.

The extraction stage loads:

- Customers
- Orders
- Products

### 2. Clean

The cleaning stage prepares the raw data for transformation and analysis.

Typical operations include:

- Handling missing values
- Removing unnecessary whitespace
- Standardizing column values
- Converting dates to appropriate data types
- Preparing fields for downstream processing

### 3. Transform

Business transformations are applied to the datasets.

The pipeline calculates the order amount:

`order_amount = quantity × unit_price`

It also:

- Standardizes order status
- Creates order year
- Creates order month
- Creates customer full name when first and last name fields are available
- Standardizes customer and product IDs for reliable joins

### 4. Join / Merge

The pipeline combines the three datasets using Pandas merge operations.

First:

`Orders + Customers`

using:

`customer_id`

Then:

`Customer Orders + Products`

using:

`product_id`

The result is a consolidated analytical dataset containing order, customer, and product information.

## Data Validation

Before loading the final dataset, the pipeline performs data-quality checks.

Validation includes:

- Duplicate order IDs
- Missing order IDs
- Missing customer IDs
- Missing product IDs
- Invalid quantities
- Invalid unit prices
- Invalid calculated order amounts
- Invalid order dates

The pipeline reports the number of validation issues found.

A successful run produces:

`Data validation PASSED.`

## Load

After successful processing, the final enriched dataset is written to:

`data/processed/enriched_orders.csv`

This dataset can be used for downstream analytics, reporting, dashboards, or additional data engineering workflows.

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/burgula18/python-etl-data-pipeline.git
