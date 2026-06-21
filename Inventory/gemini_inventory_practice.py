import pandas as pd

PATH = 'data templates'
file_name = 'gemini_inventory_data.csv'

df = pd.read_csv(PATH + '/' + file_name)

print(df)

# Fix Inconsistent Casing: "Laptop - Pro 15" and "LAPTOP - PRO 15" should be treated as the same product.
# Convert all product_name values to Title Case or Upper Case.
df['product_name'] = df['product_name'].apply(lambda elem: elem.upper())

# Missing Values: * Find the row with the missing category and fill
# it based on similar products (e.g., if it's a "Monitor", it's "Electronics").
df['category'] = df.groupby('product_name')['category'].transform(
    lambda x: x.fillna(x.mode()[0] if not x.mode().empty else "Unknown")
)

# Find rows where stock_count is "not_available" or empty and replace them with 0.
# Convert stock_count to an actual integer type.
df['stock_count'] = df['stock_count'].replace(['not_available', None], 0).astype(int)

# Handle Non-Numeric Data: The price column has an "N/A" value.
# Find exact product price or replace it with the median price of the other electronics.

# Step 1: Fill based on the exact Product
# This finds other rows with the same product name and takes their average/first price
df['price'] = df['price'].fillna(
    df.groupby('product_name')['price'].transform('median')
)

# Step 2: Fill remaining NaNs based on the Category median
# This handles cases where the product has NO price data anywhere,
# but we know its category median.
df['price'] = df['price'].fillna(
    df.groupby('category')['price'].transform('median')
)

# Date Conversion: Convert last_restock_date to a proper datetime object.
df['last_restock_date'] = pd.to_datetime(df['last_restock_date'])

# Filtering: Create a new DataFrame containing only "Electronics" that have a price higher than $200.
electronics_200_plus_df = df[(df['category'] == 'Electronics') & (df['price'] > 200)]

# New Column: Create a column called inventory_value by multiplying price by stock_count.
df['inventory_value'] = df['price'] * df['stock_count']

#print(df[['product_name', 'category', 'price', 'stock_count', 'inventory_value', 'last_restock_date']])

# Group By: Which category has the highest total inventory value?
category_totals = df.groupby('category')['inventory_value'].sum() # Sum inventory value per category

highest_val_category = category_totals.idxmax()
highest_value = category_totals.max()

print(f"The category with the highest total value is {highest_val_category} (${highest_value:,.2f})")

# Supplier Analysis: How many unique products does each supplier_contact provide?
supplier_product_counts = df.groupby('supplier_contact')['product_name'].nunique()

print(supplier_product_counts.sort_values(ascending=False))

# Low Stock Alert: List all products where stock_count is less than 10.
print(df[df['stock_count'] < 10])
