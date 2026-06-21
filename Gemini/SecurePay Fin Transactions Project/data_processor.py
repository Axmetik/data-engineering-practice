import pandas as pd


def process_data(file_name):
    df = pd.read_csv(file_name)

    df.dropna(subset=['tx_id'], inplace=True)

    # DE Requirement: Standardization
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='mixed', errors='coerce')
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0.0)
    df['cust_id'] = df['cust_id'].astype(str)

    return df