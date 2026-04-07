# 📊 Sales Performance Dashboard

> An end-to-end sales analytics project built to uncover revenue trends, identify top-performing products, and support data-driven business decisions.

---

## 🧩 Business Problem

Sales teams often struggle to identify *which products*, *regions*, and *time periods* are driving or hurting revenue. Without a centralized view of performance metrics, it becomes difficult to prioritize efforts or make timely strategic decisions.

This project simulates the work of a Business Analyst tasked with building a reporting solution to help stakeholders monitor KPIs and take action.

---

## 📁 Dataset

- **Source:** [Superstore Sales Dataset – Kaggle](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- **Size:** ~10,000 rows | Orders from 2019–2022
- **Fields:** Order Date, Region, Category, Sub-Category, Sales, Profit, Discount, Quantity

---

## 🔍 Approach

1. **Data Cleaning** – Removed duplicates, handled nulls, standardized date formats
2. **Exploratory Data Analysis (EDA)** – Identified trends across time, region, and product category
3. **KPI Definition** – Defined key metrics: Total Revenue, Profit Margin, Average Order Value, YoY Growth
4. **Visualization** – Built an interactive dashboard to present findings to a non-technical audience
5. **Recommendations** – Documented actionable business insights based on the analysis

---

## 📈 Key Findings

- **Technology** category generated the highest revenue but had inconsistent profit margins due to heavy discounting
- **West region** outperformed all other regions in both sales volume and profitability
- **Q4 (Oct–Dec)** consistently showed a 30–40% spike in orders — indicating seasonal demand patterns
- Products with discounts above **20%** showed negative profit margins, suggesting a need to revise the discount strategy

---

## 💡 Business Recommendations

| Finding | Recommendation |
|---|---|
| High discount = low profit | Cap discounts at 15% for low-margin sub-categories |
| Q4 sales spike | Pre-stock inventory and increase marketing budget in September |
| Weak South region performance | Investigate regional pricing and distribution gaps |
| Technology margin volatility | Review vendor contracts and bundling strategies |

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|---|---|
| Python (Pandas, NumPy) | Data cleaning and transformation |
| Matplotlib / Seaborn | Static charts and EDA visualizations |
| Plotly / Dash | Interactive dashboard |
| Jupyter Notebook | Analysis and documentation |
| SQL (SQLite) | Data querying |

---

## 📂 Project Structure

```
sales-dashboard/
│
├── data/
│   ├── raw/                  # Original dataset
│   └── cleaned/              # Processed data
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda.ipynb
│   └── 03_dashboard.ipynb
│
├── visuals/                  # Exported charts and dashboard screenshots
├── reports/
│   └── executive_summary.pdf # BA-style summary report
│
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/sales-dashboard.git
cd sales-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Jupyter Notebook
jupyter notebook notebooks/01_data_cleaning.ipynb
```

---

## 📌 Skills Demonstrated

- Business requirements gathering and KPI definition
- Data wrangling and exploratory analysis
- Dashboard design for executive stakeholders
- Translating data insights into business recommendations
- Documentation and reporting

---

## 👤 Author

**Suma Keerthana**  
Master's in Management Information Systems  
[LinkedIn](https://linkedin.com/in/yourprofile) | [GitHub](https://github.com/YOUR_USERNAME)
