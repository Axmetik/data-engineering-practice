import pandas as pd
import numpy as np
import os
from data_processor import process_data

MASTER_FILE = 'verified_transactions.csv'
UNMAPPED_FILE = 'unmapped_transactions.csv'


def run_pipeline(file_path):
    user_df = pd.read_csv('customers.csv')

    print(f"\n--- Ingesting: {file_path} ---")

    try:
        new_batch = process_data(file_path)
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")
        return

    is_mapped = new_batch['cust_id'].isin(user_df['cust_id'])
    unmapped_df = new_batch[~is_mapped].copy()

    valid_batch = pd.merge(new_batch[is_mapped], user_df, how='inner', on='cust_id')

    valid_batch['fee'] = np.where(
        valid_batch['tier'].isin(['Silver', 'Bronze']),
        valid_batch['amount'] * 0.02,
        0
    )

    valid_batch['is_fraud_flag'] = (valid_batch['amount'] >= 5000) | (valid_batch['cust_id'].isna())

    if os.path.exists(MASTER_FILE):
        existing_master = pd.read_csv(MASTER_FILE)

        final_df = pd.concat([existing_master, valid_batch], ignore_index=True)
        final_df = final_df.drop_duplicates(subset=['tx_id'], keep='first')
    else:
        final_df = valid_batch

    final_df.to_csv(MASTER_FILE, index=False)
    print(f"Success: {len(valid_batch)} records verified. Total Master size: {len(final_df)}")


    if not unmapped_df.empty:
        header_needed = not os.path.exists(UNMAPPED_FILE)
        unmapped_df.to_csv(UNMAPPED_FILE, mode='a', index=False, header=header_needed)
        print(f"Logged {len(unmapped_df)} unmapped records to {UNMAPPED_FILE}")


for batch in ['securepay_landing/batch_1.csv', 'securepay_landing/batch_2.csv', 'securepay_landing/batch_3.csv']:
    run_pipeline(batch)