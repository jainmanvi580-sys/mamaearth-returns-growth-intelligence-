import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# -----------------------------
# Paths
# -----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "visualizations"

OUTPUT_DIR.mkdir(exist_ok=True)


# -----------------------------
# Load raw CSV files
# -----------------------------
customers = pd.read_csv(DATA_DIR / "customers.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
products = pd.read_csv(DATA_DIR / "products.csv")


# ============================================================
# REPRODUCE REQUIRED CLEANING FROM TASKS 2–6
# ============================================================

# Task 2: Standardize payment method
orders["payment_method"] = (
    orders["payment_method"]
    .str.strip()
    .str.upper()
)

orders["payment_method"] = orders["payment_method"].replace({
    "COD": "CASH ON DELIVERY",
    "CASH ON DELIVERY": "CASH ON DELIVERY",
    "CARD": "CARD",
    "CRD": "CARD",
    "UPI": "UPI"
})


# Task 3: Remove duplicate orders
natural_key = [
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "discount_pct",
    "payment_method",
    "rating",
    "returned"
]

orders_clean = orders.drop_duplicates(
    subset=natural_key,
    keep="first"
).copy()


# Task 4: Impute missing values
orders_clean["discount_pct"] = (
    orders_clean["discount_pct"].fillna(0)
)

rating_median = orders_clean["rating"].median()

orders_clean["rating"] = (
    orders_clean["rating"].fillna(rating_median)
)


# Task 5: Merge products and customers
orders_clean = orders_clean.merge(
    products,
    on="product_id",
    how="left"
)

orders_clean = orders_clean.merge(
    customers,
    on="customer_id",
    how="left"
)


# Calculate order value
orders_clean["order_value"] = (
    orders_clean["quantity"]
    * orders_clean["price"]
    * (1 - orders_clean["discount_pct"] / 100)
)


# Task 6: Flag quantity outliers
Q1 = orders_clean["quantity"].quantile(0.25)
Q3 = orders_clean["quantity"].quantile(0.75)

IQR = Q3 - Q1

lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

orders_clean["is_outlier"] = (
    (orders_clean["quantity"] < lower)
    | (orders_clean["quantity"] > upper)
)


# ============================================================
# 1. RETURN RATE BY PAYMENT METHOD
# ============================================================

return_rate = (
    orders_clean
    .groupby("payment_method")["returned"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

plt.figure(figsize=(8, 5))

bars = plt.bar(
    return_rate.index,
    return_rate.values
)

# Exact percentage labels
for bar, value in zip(bars, return_rate.values):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.1f}%",
        ha="center",
        va="bottom"
    )

plt.title("COD Returns at 44.4% — 3x Card")
plt.xlabel("Payment Method")
plt.ylabel("Return Rate (%)")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "return_rate_by_payment.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# 2. OUTLIER-CORRECTED MONTHLY REVENUE TREND
# ============================================================

orders_clean["order_date"] = pd.to_datetime(
    orders_clean["order_date"]
)

orders_clean["year_month"] = (
    orders_clean["order_date"].dt.to_period("M")
)

# Exclude the two flagged outliers
monthly_revenue = (
    orders_clean[~orders_clean["is_outlier"]]
    .groupby("year_month")["order_value"]
    .sum()
)

# Find actual peak month
peak_month = monthly_revenue.idxmax()

peak_value = monthly_revenue.max()

# Convert period to string for plotting
months = monthly_revenue.index.astype(str)

plt.figure(figsize=(9, 5))

plt.plot(
    months,
    monthly_revenue.values,
    marker="o"
)

plt.xlabel("Month")
plt.ylabel("Revenue")
plt.title(
    f"Outlier-Corrected Monthly Revenue — Peak: {peak_month}"
)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "monthly_revenue_trend.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("Visualizations created successfully.")
print("Saved:", OUTPUT_DIR / "return_rate_by_payment.png")
print("Saved:", OUTPUT_DIR / "monthly_revenue_trend.png")
print(f"Actual peak month: {peak_month}")
print(f"Peak revenue: ₹{peak_value:.2f}")

