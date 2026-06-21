import pandas as pd
import datetime
import os

def process_data(file_path):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return


    # Add Audit Metadata
    df['processed_at'] = datetime.datetime.now()
    df['source_batch'] = os.path.basename(file_path)

    # Standardize types
    df['ts'] = pd.to_datetime(df['ts'], format='mixed', errors='coerce')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    df = df.drop_duplicates(subset=['sensor_id', 'ts', 'value'])

    # Delete rows with sensor_id NaN(null) value
    df.dropna(subset=['sensor_id'], inplace=True)

    return df

# process_data('landing_zone/day1.csv')
