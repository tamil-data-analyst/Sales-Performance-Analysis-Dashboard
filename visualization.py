import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect(r"C:\Users\tamil\OneDrive\Desktop\sales_database.db")

# 1. Category wise Bar Chart
q1 = pd.read_sql_query("""
    SELECT Category, ROUND(SUM(Sales),2) AS Revenue
    FROM sales GROUP BY Category
    ORDER BY Revenue DESC""", conn)

plt.figure(figsize=(8,5))
plt.bar(q1['Category'], q1['Revenue'], color=['#2196F3','#4CAF50','#FF9800','#E91E63','#9C27B0'])
plt.title('Category wise Revenue')
plt.xlabel('Category')
plt.ylabel('Revenue (INR)')
plt.tight_layout()
plt.savefig('category_revenue.png')
plt.show()

# 2. Region wise Pie Chart
q2 = pd.read_sql_query("""
    SELECT Region, ROUND(SUM(Sales),2) AS Revenue
    FROM sales GROUP BY Region""", conn)

plt.figure(figsize=(7,7))
plt.pie(q2['Revenue'], labels=q2['Region'], autopct='%1.1f%%')
plt.title('Region wise Sales Distribution')
plt.savefig('region_pie.png')
plt.show()

# 3. Monthly Trend Line Chart
q3 = pd.read_sql_query("""
    SELECT SUBSTR(Order_Date,1,7) AS Month,
           ROUND(SUM(Sales),2) AS Revenue
    FROM sales WHERE Order_Date != 'NaT'
    GROUP BY Month ORDER BY Month""", conn)

plt.figure(figsize=(12,5))
plt.plot(q3['Month'], q3['Revenue'], marker='o', color='blue')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Revenue')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_trend.png')
plt.show()

conn.close()
print("✅ Charts saved!")