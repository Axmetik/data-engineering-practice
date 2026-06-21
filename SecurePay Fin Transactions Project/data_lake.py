import pandas as pd
import numpy as np
import os

os.makedirs('securepay_landing', exist_ok=True)

# 1. Customer Dimension (The Source of Truth)
customers = pd.DataFrame({
    'cust_id': ['C01', 'C02', 'C03', 'C04', 'C05'],
    'country': ['UK', 'USA', 'Germany', 'UK', 'USA'],
    'tier': ['Gold', 'Silver', 'Gold', 'Bronze', 'Silver']
})
customers.to_csv('customers.csv', index=False)

# 2. Hourly Transaction Batches
# Batch 1: Standard transactions
batch_1 = pd.DataFrame({
    'tx_id': ['TX101', 'TX102', 'TX103'],
    'cust_id': ['C01', 'C02', 'C03'],
    'amount': [500.0, 20.0, 1500.0],
    'timestamp': ['2026-02-10 14:00', '2026-02-10 14:05', '2026-02-10 14:10']
})

# Batch 2: The "Dirty" Batch (Missing ID, duplicated TX, invalid amount)
batch_2 = pd.DataFrame({
    'tx_id': ['TX104', 'TX104', 'TX105', 'TX106'], # TX104 is a double-submission
    'cust_id': ['C01', 'C04', np.nan, 'C99'], # C99 doesn't exist in our customer list
    'amount': [1200.0, 1200.0, 50.0, 300.0],
    'timestamp': ['2026-02-10 15:00', '2026-02-10 15:00', '2026-02-10 15:10', '2026-02-10 15:15']
})

# Batch 3: High-Value Batch (For testing fraud logic)
batch_3 = pd.DataFrame({
    'tx_id': ['TX107', 'TX108'],
    'cust_id': ['C05', 'C01'],
    'amount': [10000.0, 5.0], # 10,000 is a "whale" transaction
    'timestamp': ['2026-02-10 16:00', '2026-02-10 16:30']
})

batch_1.to_csv('securepay_landing/batch_1.csv', index=False)
batch_2.to_csv('securepay_landing/batch_2.csv', index=False)
batch_3.to_csv('securepay_landing/batch_3.csv', index=False)

print("Financial Landing Zone is ready.")