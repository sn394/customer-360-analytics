import pandas as pd

file_path = "data/raw/Online Retail.xlsx"

df = pd.read_excel(file_path)

print("Dataset loaded successfully!")
print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

print("Duplicate Rows:", df.duplicated().sum())

df = df.drop_duplicates()

print("Rows after removing duplicates:", len(df))


print("\nCancelled Invoices:")
print(df["InvoiceNo"].astype(str).str.startswith("C").sum())

print("\nNegative Quantities:")
print((df["Quantity"] < 0).sum())

print("\nZero Unit Prices:")
print((df["UnitPrice"] == 0).sum())

print("\nNegative Unit Prices:")
print((df["UnitPrice"] < 0).sum())

# Remove cancelled invoices
df_clean = df[~df["InvoiceNo"].astype(str).str.startswith("C")].copy()

# Keep only valid sales
df_clean = df_clean[
    (df_clean["Quantity"] > 0) &
    (df_clean["UnitPrice"] > 0)
].copy()

print("\nOriginal rows:", len(df))
print("Clean rows:", len(df_clean))
print("Rows removed:", len(df) - len(df_clean))

print("\nMissing Customer IDs in clean data:")
print(df_clean["CustomerID"].isnull().sum())

print("\nMissing Descriptions in clean data:")
print(df_clean["Description"].isnull().sum())

print("\nUnique Customers:")
print(df_clean["CustomerID"].nunique())

print("\nUnique Products:")
print(df_clean["StockCode"].nunique())

print("\nCountries:")
print(df_clean["Country"].nunique())


# Create revenue column
df_clean["Revenue"] = df_clean["Quantity"] * df_clean["UnitPrice"]

print("\nRevenue Summary:")
print(df_clean["Revenue"].describe())

print("\nTotal Revenue:")
print(round(df_clean["Revenue"].sum(), 2))


# Save cleaned dataset
output_path = "data/cleaned/online_retail_cleaned.csv"

df_clean.to_csv(output_path, index=False)

print("\nCleaned dataset saved successfully!")
print("File:", output_path)


# Basic business metrics

total_revenue = df_clean["Revenue"].sum()
total_orders = df_clean["InvoiceNo"].nunique()
total_customers = df_clean["CustomerID"].nunique()

print("\n--- BUSINESS METRICS ---")
print("Total Revenue: £", round(total_revenue, 2))
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)

# Monthly revenue analysis

df_clean["Month"] = df_clean["InvoiceDate"].dt.to_period("M")

monthly_revenue = (
    df_clean.groupby("Month")["Revenue"]
    .sum()
    .round(2)
)

print("\n--- MONTHLY REVENUE ---")
print(monthly_revenue)


# Top 10 products by revenue

product_revenue = (
    df_clean.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n--- TOP 10 PRODUCTS BY REVENUE ---")
print(product_revenue)


# Check non-product entries

non_product = df_clean[
    df_clean["Description"].str.contains(
        "POSTAGE|MANUAL|DOTCOM", 
        case=False, 
        na=False
    )
]

print("\n--- NON-PRODUCT ENTRIES ---")
print(non_product["Description"].value_counts())

print("\nTotal non-product rows:", len(non_product))


# Dataset for product-level analysis
df_products = df_clean[
    ~df_clean["Description"].str.contains(
        "POSTAGE|MANUAL|DOTCOM",
        case=False,
        na=False
    )
].copy()

print("\n--- PRODUCT ANALYSIS DATA ---")
print("Rows:", len(df_products))
print("Unique products:", df_products["StockCode"].nunique())


# Revenue by country

country_revenue = (
    df_clean.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n--- TOP 10 COUNTRIES BY REVENUE ---")
print(country_revenue)


# Customer RFM Analysis

customer_df = df_clean.dropna(subset=["CustomerID"]).copy()

analysis_date = customer_df["InvoiceDate"].max() + pd.Timedelta(days=1)

rfm = customer_df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda x: (analysis_date - x.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
)

print("\n--- RFM ANALYSIS ---")
print(rfm.head())

print("\nNumber of customers:", len(rfm))


# Create simple RFM scores
rfm["R_Score"] = pd.qcut(rfm["Recency"], 4, labels=[4, 3, 2, 1])
rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
)
rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    4,
    labels=[1, 2, 3, 4]
)

# Convert scores to numbers
rfm["R_Score"] = rfm["R_Score"].astype(int)
rfm["F_Score"] = rfm["F_Score"].astype(int)
rfm["M_Score"] = rfm["M_Score"].astype(int)

# Overall RFM score
rfm["RFM_Score"] = (
    rfm["R_Score"] +
    rfm["F_Score"] +
    rfm["M_Score"]
)

# Simple customer segmentation
def segment_customer(score):
    if score >= 10:
        return "High Value"
    elif score >= 7:
        return "Potential"
    elif score >= 5:
        return "Needs Attention"
    else:
        return "Low Value"

rfm["Segment"] = rfm["RFM_Score"].apply(segment_customer)

print("\n--- CUSTOMER SEGMENTS ---")
print(rfm["Segment"].value_counts())

print("\n--- TOP 10 HIGH-VALUE CUSTOMERS ---")
print(
    rfm.sort_values("Monetary", ascending=False)
       .head(10)
)


# Save customer RFM analysis

rfm.to_csv(
    "data/cleaned/customer_rfm.csv",
    index=True
)

print("\nRFM analysis saved successfully!")

# Save customer RFM analysis

rfm.to_csv(
    "data/cleaned/customer_rfm.csv",
    index=True
)

print("\nRFM analysis saved successfully!")


# Create a fresh SQL import file
sql_file = "data/cleaned/retail_sql_import.csv"

df_clean.to_csv(
    sql_file,
    index=False,
    encoding="utf-8"
)

print("\nFresh SQL import file created!")
print(sql_file)