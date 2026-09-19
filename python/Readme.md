# Customer 360 Analytics

## Project Overview

Customer 360 Analytics is a data analytics project built using a real Online Retail transaction dataset.

The project analyzes customer behavior, sales performance, products, and revenue trends using Python, SQL, and Power BI.

## Tools & Technologies

- Python
- Pandas
- MySQL
- SQL
- Power BI
- Excel/CSV

## Dataset

The project uses the Online Retail dataset containing real transaction records from a UK-based online retailer.

Source: UCI Machine Learning Repository

## Project Workflow

Raw Data
→ Python Data Cleaning
→ MySQL Database
→ SQL Analysis
→ Power BI Dashboard
→ Business Insights

## Python Analysis

The dataset was cleaned using Pandas.

Tasks performed:

- Removed duplicate transactions
- Identified missing values
- Removed cancelled transactions
- Removed invalid quantities and prices
- Calculated revenue
- Analyzed monthly revenue
- Analyzed products and countries
- Performed RFM customer segmentation

## SQL Analysis

Business questions analyzed using MySQL:

- What is the total revenue?
- How many orders were placed?
- How many customers are there?
- What is the monthly revenue trend?
- Which items generate the highest revenue?

## Power BI Dashboard

The dashboard contains:

- Total Revenue
- Total Orders
- Total Customers
- Monthly Revenue Trend
- Top Revenue Items
- Customer Segmentation

## Key Results

- Total Revenue: approximately £10.63M
- Total Orders: 19,959
- Total Customers: 4,338
- November 2011 recorded the highest monthly revenue.

## Customer Segmentation

RFM analysis was used to segment customers based on:

- Recency
- Frequency
- Monetary Value

Customer segments include:

- High Value
- Potential
- Needs Attention
- Low Value

## Business Insights

The analysis helps identify:

- High-revenue periods
- Important customer segments
- Revenue-generating items
- Customer purchasing behavior
- Opportunities for customer retention and targeted marketing

## Project Structure

```text
Customer 360-Analytics/
│
├── data/
│   ├── raw/
│   └── cleaned/
│
├── python/
│   ├── 01_data_exploration.py
│   └── 02_load_mysql.py
│
├── sql/
│
├── powerbi/
│   └── Customer_360_Analytics.pbix
│
├── screenshots/
│
└── README.md