import pandas as pd
from datetime import datetime

PATH = '../data templates'
file_name = 'gemini_support_tickets_data.csv'

df = pd.read_csv(PATH + '/' + file_name)

print(df)

# Fix IDs: Fill the missing ticket_id with a logical sequence number (e.g., 1003).
prev = df['ticket_id'].shift(1)
next = df['ticket_id'].shift(-1)
df['ticket_id'] = df['ticket_id'].fillna((prev + next) / 2)

# Remove Duplicates: Identify and remove the duplicate entry for ticket_id 1001.
df = df.drop_duplicates(subset=['ticket_id'], keep='first')

# Standardize Strings: * customer_name has inconsistent casing (e.g., "John Doe" vs "john doe").
# Make them all Proper Case.
df['customer_name'] = df['customer_name'].str.title() # Capitalize Each New Word

# issue_category has "TECH" and "Technical". Group them both under "Technical".
# Also fix the casing for "shipping".
df['issue_category'] = df['issue_category'].replace('TECH', 'Technical').str.title()

# Handle Junk Data: The resolution_time_hrs column contains the string "unknown".
# Replace "unknown" with NaN.
# Convert the whole column to a numeric type (float).
# Fill the NaN values with the mean resolution time of the entire dataset.
df['resolution_time_hrs'] = df['resolution_time_hrs'].replace('unknown', None).astype(float)
mean_value = df['resolution_time_hrs'].astype(float).mean()
df['resolution_time_hrs'] = df['resolution_time_hrs'].fillna(mean_value).round(2)

# Uniform Formats: The ticket_date column uses /, -, and . as separators.
# Convert this column into a standard Python datetime format.
def try_parsing_date(text):
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%d-%m-%Y', '%Y/%m/%d', '%Y.%m.%d'):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')

# df['ticket_date'] = df['ticket_date'].apply(try_parsing_date)# TODO to potentially solve
df['ticket_date'] = pd.to_datetime(df['ticket_date'], format='mixed')

# Time Features: Create a new column called month extracted from the ticket_date
df['month'] = df['ticket_date'].dt.month_name()

# print(df[['ticket_date', 'month']])


# High Priority Filter: Create a sub-list of all tickets that are "High" or "Urgent" priority AND took more than 10 hours to resolve.
high_effort_tickets = df[
    (df['priority'].isin(['High', 'Urgent'])) &
    (df['resolution_time_hrs'] > 10)
]
# Category Performance: Group the data by issue_category and calculate the average resolution time for each.
category_performance = df.groupby('issue_category')['resolution_time_hrs'].mean()

# Customer Loyalty: Find which customer has submitted the most tickets.
customer_loyalty = df.groupby('customer_name')['ticket_id'].count()
loyalty_leader_count = customer_loyalty.max()

top_customers = customer_loyalty[customer_loyalty == loyalty_leader_count].index.tolist()
# print('Customer Loyalty Leaders are', str(top_customers) , 'with', loyalty_leader_count, 'tickets')

# Create a pivot table that shows the count of tickets for each priority level, broken down by issue_category
pivot_df = pd.pivot_table(
    df,
    values='ticket_id',        # counter
    index='issue_category',    # rows
    columns='priority',        # columns
    aggfunc='count',           # aggregation function
    fill_value=0               # Nan handling
)

# print(pivot_df)