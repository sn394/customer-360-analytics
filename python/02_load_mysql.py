import pandas as pd
import mysql.connector
from getpass import getpass

# ---------------------------------
# 1. Read cleaned CSV
# ---------------------------------

file_path = "data/cleaned/retail_sql_import.csv"

print("Reading CSV...")
df = pd.read_csv(file_path)

print("Rows found:", len(df))


# ---------------------------------
# 2. Fix data types
# ---------------------------------

df["InvoiceNo"] = pd.to_numeric(df["InvoiceNo"], errors="coerce")
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["UnitPrice"] = pd.to_numeric(df["UnitPrice"], errors="coerce")
df["CustomerID"] = pd.to_numeric(df["CustomerID"], errors="coerce")
df["Revenue"] = pd.to_numeric(df["Revenue"], errors="coerce")

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)

# Remove rows where essential values are invalid
df = df.dropna(
    subset=[
        "InvoiceNo",
        "Quantity",
        "UnitPrice",
        "InvoiceDate",
        "Revenue"
    ]
)

print("Valid rows:", len(df))


# ---------------------------------
# 3. Connect to MySQL
# ---------------------------------

password = getpass("Enter MySQL password: ")

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="customer_analytics"
)

cursor = conn.cursor()

print("Connected to MySQL!")


# ---------------------------------
# 4. Create table
# ---------------------------------

cursor.execute("DROP TABLE IF EXISTS online_retail")

cursor.execute("""
CREATE TABLE online_retail (
    InvoiceNo INT,
    StockCode VARCHAR(50),
    Description TEXT,
    Quantity INT,
    InvoiceDate DATETIME,
    UnitPrice DOUBLE,
    CustomerID DOUBLE NULL,
    Country VARCHAR(100),
    Revenue DOUBLE,
    Month VARCHAR(20)
)
""")

print("Table created!")


# ---------------------------------
# 5. Insert data
# ---------------------------------

insert_sql = """
INSERT INTO online_retail
(
    InvoiceNo,
    StockCode,
    Description,
    Quantity,
    InvoiceDate,
    UnitPrice,
    CustomerID,
    Country,
    Revenue,
    Month
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


# Convert Pandas/Numpy values into
# normal Python values
def clean_value(value):

    # Missing value
    if pd.isna(value):
        return None

    # Pandas date
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()

    # Numpy number
    if hasattr(value, "item"):
        return value.item()

    return value


print("Starting data import...")


batch_size = 5000

for start in range(0, len(df), batch_size):

    batch = df.iloc[start:start + batch_size]

    rows = []

    for row in batch.itertuples(index=False, name=None):

        cleaned_row = tuple(
            clean_value(value)
            for value in row
        )

        rows.append(cleaned_row)

    cursor.executemany(insert_sql, rows)

    conn.commit()

    loaded = min(start + batch_size, len(df))

    print(f"Loaded {loaded} / {len(df)}")


# ---------------------------------
# 6. Verify
# ---------------------------------

cursor.execute(
    "SELECT COUNT(*) FROM online_retail"
)

count = cursor.fetchone()[0]

print()
print("==============================")
print("IMPORT COMPLETED!")
print("==============================")
print("Rows in MySQL:", count)


# ---------------------------------
# 7. Close connection
# ---------------------------------

cursor.close()
conn.close()

print("MySQL connection closed.")