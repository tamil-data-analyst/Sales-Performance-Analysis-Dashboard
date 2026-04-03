import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import sqlite3

# Style settings
plt.rcParams['figure.facecolor'] = '#0D1B2A'
plt.rcParams['axes.facecolor'] = '#1E2A3A'
plt.rcParams['text.color'] = 'white'
plt.rcParams['axes.labelcolor'] = 'white'
plt.rcParams['xtick.color'] = 'white'
plt.rcParams['ytick.color'] = 'white'

conn = sqlite3.connect(r"C:\Users\tamil\OneDrive\Desktop\sales_database.db")

# ====== 1. Category Bar Chart ======
q1 = pd.read_sql_query("""
    SELECT Category, ROUND(SUM(Sales)/1000000,2) AS Revenue_M
    FROM sales GROUP BY Category
    ORDER BY Revenue_M DESC""", conn)

fig, ax = plt.subplots(figsize=(10,6))
colors = ['#00B4D8','#0077B6','#48CAE4','#90E0EF','#ADE8F4']
bars = ax.barh(q1['Category'], q1['Revenue_M'], color=colors, edgecolor='white', linewidth=0.5)
ax.set_title('💼 Sales by Category', fontsize=16, fontweight='bold', color='white', pad=20)
ax.set_xlabel('Revenue (Millions ₹)', fontsize=12)
for bar, val in zip(bars, q1['Revenue_M']):
    ax.text(bar.get_width()+0.05, bar.get_y()+bar.get_height()/2,
            f'₹{val}M', va='center', color='white', fontweight='bold')
plt.tight_layout()
plt.savefig(r"C:\Users\tamil\OneDrive\Desktop\category_chart.png", dpi=150, bbox_inches='tight')
plt.show()

# ====== 2. Monthly Trend ======
q2 = pd.read_sql_query("""
    SELECT SUBSTR(Order_Date,1,7) AS Month,
           ROUND(SUM(Sales)/1000000,2) AS Revenue_M
    FROM sales WHERE Order_Date != 'NaT'
    GROUP BY Month ORDER BY Month""", conn)

fig, ax = plt.subplots(figsize=(12,6))
ax.plot(q2['Month'], q2['Revenue_M'], color='#00B4D8', linewidth=2.5, marker='o', markersize=6)
ax.fill_between(range(len(q2)), q2['Revenue_M'], alpha=0.3, color='#00B4D8')
ax.set_xticks(range(len(q2)))
ax.set_xticklabels(q2['Month'], rotation=45, ha='right', fontsize=8)
ax.set_title('📈 Monthly Sales Trend', fontsize=16, fontweight='bold', color='white', pad=20)
ax.set_ylabel('Revenue (Millions ₹)', fontsize=12)
plt.tight_layout()
plt.savefig(r"C:\Users\tamil\OneDrive\Desktop\monthly_trend.png", dpi=150, bbox_inches='tight')
plt.show()

# ====== 3. Salesperson Performance ======
q3 = pd.read_sql_query("""
    SELECT Salesperson,
           ROUND(SUM(Sales)/1000000,2) AS Sales_M,
           ROUND(SUM(Target_Sales)/1000000,2) AS Target_M
    FROM sales GROUP BY Salesperson
    ORDER BY Sales_M DESC LIMIT 8""", conn)

fig, ax = plt.subplots(figsize=(10,6))
x = range(len(q3))
ax.bar([i-0.2 for i in x], q3['Sales_M'], width=0.4, label='Actual', color='#00B4D8')
ax.bar([i+0.2 for i in x], q3['Target_M'], width=0.4, label='Target', color='#FF6B6B')
ax.set_xticks(x)
ax.set_xticklabels(q3['Salesperson'], rotation=45, ha='right', fontsize=9)
ax.set_title('🏆 Salesperson Performance vs Target', fontsize=16, fontweight='bold', color='white', pad=20)
ax.legend(fontsize=12)
plt.tight_layout()
plt.savefig(r"C:\Users\tamil\OneDrive\Desktop\salesperson_chart.png", dpi=150, bbox_inches='tight')
plt.show()

# ====== 4. Correlation Heatmap ======
df = pd.read_sql_query("SELECT Sales, Profit, Quantity, Discount, Unit_Price FROM sales", conn)
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

fig, ax = plt.subplots(figsize=(8,6))
sns.heatmap(df.corr(), annot=True, fmt='.2f', cmap='coolwarm',
            linewidths=0.5, ax=ax, cbar_kws={'label': 'Correlation'})
ax.set_title('🔥 Correlation Heatmap', fontsize=16, fontweight='bold', color='white', pad=20)
plt.tight_layout()
plt.savefig(r"C:\Users\tamil\OneDrive\Desktop\heatmap.png", dpi=150, bbox_inches='tight')
plt.show()

conn.close()
print("✅ All Professional Charts Saved!")