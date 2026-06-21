import pandas as pd
import datetime
import os

from data_processor import process_data

# Path to our "Permanent Store"
MASTER_FILE = 'master_iot_data.csv'


def run_pipeline(file_path):
    print(f"--- Starting Ingestion: {file_path} ---")

    try:
        new_data = process_data(file_path)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    if not os.path.exists(MASTER_FILE):
        # First time running: Create the file
        new_data.to_csv(MASTER_FILE, index=False)
        print(f"Created new Master Store with {len(new_data)} records.")
    else:
        # Load existing Master
        master_df = pd.read_csv(MASTER_FILE)
        master_df['ts'] = pd.to_datetime(master_df['ts'])  # Ensure types match for comparison

        # Incremental Load Logic: Check for globally unique records
        combined_df = pd.concat([master_df, new_data], ignore_index=True)

        # Deduplicate across the entire history
        final_df = combined_df.drop_duplicates(subset=['sensor_id', 'ts', 'value'], keep='first')

        # Overwrite Master with the updated, aligned data
        final_df.to_csv(MASTER_FILE, index=False)
        print(f"Updated Master Store. Current total records: {len(final_df)}")

    generate_alerts(file_path)


def generate_alerts(file_path):
    # This is a separate 'consumer' of the data
    df = pd.read_csv(MASTER_FILE)
    temp_alerts = df[(df['reading_type'] == 'temp') & (df['value'] > 25)]
    energy_alerts = df[(df['reading_type'] == 'energy') & (df['value'] > 1000)]

    alerts = pd.concat([temp_alerts, energy_alerts])
    alerts.to_csv('alerts.csv', index=False)
    if not alerts.empty:
        print(f"Alerts generated: {len(alerts)} critical readings found.")


# --- EXECUTION CYCLE ---
# To test your work, run this:
for day_file in ['landing_zone/day1.csv', 'landing_zone/day2.csv', 'landing_zone/day3.csv', 'landing_zone/day4_corrupt.csv']:
    run_pipeline(day_file)