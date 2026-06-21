import pandas as pd
import numpy as np

PATH = 'data templates'
products_file_name = 'gemini_products_to_join.csv'
orders_file_name = 'gemini_orders_to_join.csv'

df_products = pd.read_csv(PATH + '/' + products_file_name)
df_orders = pd.read_csv(PATH + '/' + orders_file_name)

# print(df_products)
# print(df_orders)

# The Join: Perform an Inner Join between orders and products using the product_id column.
# TODO: orders without product info are ignored
merged_df = pd.merge(df_orders, df_products, on='product_id', how='inner')

# Total Revenue: Create a new column total_order_value by multiplying quantity by base_price.
merged_df['total_order_value'] = merged_df['base_price'].astype(float) * merged_df['quantity'].astype(float)

# Discount Logic: Apply a 10% discount to the total_order_value only if the quantity is greater than 3.
# Create this as a new column final_price
merged_df['final_price'] = np.where(merged_df['quantity'] > 3,
                             merged_df['total_order_value'] * 0.9,
                             merged_df['total_order_value'])

# or native pandas solution
# df['final_price'] = df['total_order_value']
#
# df.loc[df['quantity'] > 3, 'final_price'] = df['total_order_value'] * 0.9


# Top Region: Which customer_region generated the most revenue?
revenue_data = merged_df.groupby('customer_region')['final_price'].sum()
most_revenue = revenue_data.max()

revenue_leaders = revenue_data[revenue_data == most_revenue].index.tolist()
# print('Revenue Leader(s)', str(revenue_leaders) , 'with', most_revenue, value')

# Product Popularity: Find the top 3 most-sold products by total quantity.
product_rating = merged_df.groupby('product_id')['quantity'].sum().sort_values(ascending=False)
top_three_products_by_quantity = product_rating.head(3)
# print(top_three_products_by_quantity)

# Cross-Tabulation: Use pd.crosstab or a Pivot Table to see how many items of each category were sold in each customer_region.
pivot_df = pd.pivot_table(
    merged_df,
    values='quantity',  # counter
    index='customer_region',  # rows
    columns='category',  # columns
    aggfunc='sum',  # aggregation function
    fill_value=0  # Nan handling
)
# print(pivot_df)

# Task: Calculate the percentage contribution of each product to the total revenue.
# Goal: Sort them in descending order and find how many products it takes to reach 50% of your total sales.
total_revenue = merged_df['final_price'].sum()
percent_contribution = (((merged_df.groupby('product_id')['final_price'].sum() / total_revenue) * 100)
                        .sort_values(ascending=False))
# print(percent_contribution)

# Task: Use the .resample() method (or group by week) to find the total revenue and total quantity sold per week.
# Goal: Identify if sales are trending up or down as the month progresses.
merged_df['order_date'] = pd.to_datetime(merged_df['order_date'], format='mixed')

merged_df = merged_df.set_index('order_date')

# Агрегуємо дохід та кількість за місяць
monthly_sales = merged_df.resample('W').agg({
    'final_price': 'sum',
    'quantity': 'sum'
})

# Перейменовуємо для зручності
monthly_sales.columns = ['Monthly Revenue', 'Monthly Quantity']

print(monthly_sales)
