import sqlite3
import pandas as pd

conn = sqlite3.connect(r"C:\Users\tamil\OneDrive\Desktop\sales_database.db")

# 1. Total KPIs
q1 = pd.read_sql_query("""
    SELECT ROUND(SUM(Sales),2) AS Total_Revenue,
           ROUND(SUM(Profit),2) AS Total_Profit,
           COUNT(*) AS Total_Orders
    FROM sales""", conn)
print("=== TOTAL KPIs ===")
print(q1)

# 2. Region wise
q2 = pd.read_sql_query("""
    SELECT Region, ROUND(SUM(Sales),2) AS Revenue,
           COUNT(*) AS Orders
    FROM sales GROUP BY Region 
    ORDER BY Revenue DESC""", conn)
print("\n=== REGION WISE ===")
print(q2)

# 3. Top Salesperson
q3 = pd.read_sql_query("""
    SELECT Salesperson, ROUND(SUM(Sales),2) AS Total_Sales
    FROM sales GROUP BY Salesperson
    ORDER BY Total_Sales DESC LIMIT 5""", conn)
print("\n=== TOP SALESPERSONS ===")
print(q3)

# 4. Category wise
q4 = pd.read_sql_query("""
    SELECT Category, ROUND(SUM(Sales),2) AS Revenue
    FROM sales GROUP BY Category
    ORDER BY Revenue DESC""", conn)
print("\n=== CATEGORY WISE ===")
print(q4)

conn.close()