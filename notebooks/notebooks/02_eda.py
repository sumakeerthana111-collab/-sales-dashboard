# Sales Dashboard - Step 2: Exploratory Data Analysis (EDA)
# Run this after 01_data_cleaning.py

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import os

# ── Setup ──────────────────────────────────────────────────────────────────────
os.makedirs('../visuals', exist_ok=True)
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'figure.dpi': 120, 'font.size': 11})

df = pd.read_csv('../data/cleaned/superstore_cleaned.csv', parse_dates=['Order Date'])
print(f"Loaded cleaned data: {df.shape}")

# ── 1. Sales by Category ───────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 4))
cat_summary = df.groupby('Category')[['Sales', 'Profit']].sum().sort_values('Sales', ascending=False)
cat_summary.plot(kind='bar', ax=ax, color=['#4C72B0', '#55A868'])
ax.set_title('Total Sales & Profit by Category', fontweight='bold')
ax.set_xlabel('')
ax.set_ylabel('Amount ($)')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('../visuals/01_sales_by_category.png')
plt.show()
print("Saved: 01_sales_by_category.png")

# ── 2. Monthly Sales Trend ─────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(12, 4))
monthly = df.groupby(['Order Year', 'Order Month'])['Sales'].sum().reset_index()
monthly['Period'] = pd.to_datetime(monthly[['Order Year', 'Order Month']].assign(day=1))
ax.plot(monthly['Period'], monthly['Sales'], marker='o', linewidth=2, color='#4C72B0')
ax.fill_between(monthly['Period'], monthly['Sales'], alpha=0.1, color='#4C72B0')
ax.set_title('Monthly Sales Trend', fontweight='bold')
ax.set_ylabel('Sales ($)')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
plt.tight_layout()
plt.savefig('../visuals/02_monthly_sales_trend.png')
plt.show()
print("Saved: 02_monthly_sales_trend.png")

# ── 3. Sales by Region ─────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
region_sales  = df.groupby('Region')['Sales'].sum().sort_values(ascending=True)
region_profit = df.groupby('Region')['Profit'].sum().sort_values(ascending=True)

region_sales.plot(kind='barh', ax=axes[0], color='#4C72B0')
axes[0].set_title('Sales by Region', fontweight='bold')
axes[0].xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

region_profit.plot(kind='barh', ax=axes[1], color='#55A868')
axes[1].set_title('Profit by Region', fontweight='bold')
axes[1].xaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('../visuals/03_sales_by_region.png')
plt.show()
print("Saved: 03_sales_by_region.png")

# ── 4. Discount vs Profit Analysis ────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(df['Discount'], df['Profit'], alpha=0.3, color='#C44E52', s=15)
ax.axhline(0, color='black', linewidth=1, linestyle='--', label='Break-even')
ax.axvline(0.2, color='orange', linewidth=1.5, linestyle='--', label='20% discount threshold')
ax.set_title('Discount vs Profit — Impact Analysis', fontweight='bold')
ax.set_xlabel('Discount Rate')
ax.set_ylabel('Profit ($)')
ax.legend()
plt.tight_layout()
plt.savefig('../visuals/04_discount_vs_profit.png')
plt.show()
print("Saved: 04_discount_vs_profit.png")

# ── 5. Quarterly Sales by Year ─────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 4))
quarterly = df.groupby(['Order Year', 'Order Quarter'])['Sales'].sum().unstack()
quarterly.T.plot(kind='bar', ax=ax)
ax.set_title('Quarterly Sales by Year', fontweight='bold')
ax.set_xlabel('Quarter')
ax.set_ylabel('Sales ($)')
ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f'${x:,.0f}'))
ax.set_xticklabels([f'Q{q}' for q in range(1, 5)], rotation=0)
plt.tight_layout()
plt.savefig('../visuals/05_quarterly_sales.png')
plt.show()
print("Saved: 05_quarterly_sales.png")

# ── Summary Stats ──────────────────────────────────────────────────────────────
print("\n====== KEY BUSINESS METRICS ======")
print(f"Total Revenue:      ${df['Sales'].sum():,.0f}")
print(f"Total Profit:       ${df['Profit'].sum():,.0f}")
print(f"Overall Margin:     {(df['Profit'].sum()/df['Sales'].sum())*100:.1f}%")
print(f"Avg Order Value:    ${df.groupby('Order ID')['Sales'].sum().mean():,.0f}")
print(f"Total Orders:       {df['Order ID'].nunique():,}")
print(f"Top Region:         {df.groupby('Region')['Sales'].sum().idxmax()}")
print(f"Top Category:       {df.groupby('Category')['Sales'].sum().idxmax()}")
print("==================================")
