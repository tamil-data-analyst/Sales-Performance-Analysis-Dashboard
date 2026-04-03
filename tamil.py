import pandas as pd
import numpy as np
df = pd.read_excel(r"C:\Users\tamil\OneDrive\Desktop\Sales_Performance_Raw_Dataset.xlsx",sheet_name="Raw_Sales_Data")
print(df.shape)
print(df.info())
print(df.describe())
print("Duplicates before:",df.duplicated().sum())
df = df.drop_duplicates()
print("Duplicates after:",df.duplicated().sum())
def fix_date(val):
    for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']:
        try:
            return pd.to_datetime(val, format=fmt)
        except:
            pass
    return pd.NaT

df['Order_Date'] = df['Order_Date'].apply(fix_date)
df['Ship_Date'] = pd.to_datetime(df['Ship_Date'], errors='coerce')
df['Sales'] = df['Sales'].astype(str).str.replace('Rs.', '', regex=False)
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

# Negative sales remove
df = df[df['Sales'] > 0]
df['Customer_Name'].fillna('Unknown', inplace=True)
df['Salesperson'].fillna('Unassigned', inplace=True)
df['Region'].fillna(df['Region'].mode()[0], inplace=True)
df['Sales'].fillna(df['Sales'].median(), inplace=True)
df['Category'] = df['Category'].str.strip().str.title()
df['Region'] = df['Region'].str.strip().str.title()
df['Customer_Name'] = df['Customer_Name'].str.strip()
df = df[df['Quantity'] > 0]                         # Zero quantity remove
df = df[df['Discount'] <= 1.0]                       # Invalid discount remove
df['Customer_Rating'] = df['Customer_Rating'].clip(1, 5)  # Rating 1-5 fix
df = df[df['Profit'] < 500000]                       # Outlier remove
df.to_csv(r"C:\Users\tamil\OneDrive\Desktop\cleaned_sales_data.csv",index=False)
print("✅ Cleaning Done! Rows:", len(df))
import sqlite3

conn = sqlite3.connect(r"C:\Users\tamil\OneDrive\Desktop\sales_database.db")

df.to_sql('sales', conn, if_exists='replace', index=False)

print("✅ SQLite Done! Rows:", len(df))
conn.close()