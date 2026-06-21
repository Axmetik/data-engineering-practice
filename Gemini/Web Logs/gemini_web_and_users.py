import pandas as pd
import json
from datetime import datetime

PATH = 'data templates'
web_logs = 'gemini_web_logs_raw.csv'
users = 'gemini_users_dim.csv'

df_logs = pd.read_csv(PATH + '/' + web_logs)
df_users = pd.read_csv(PATH + '/' + users)

# print(df_logs.head())
# print(df_users.head())

# In Data Engineering, we often follow the Medallion Architecture (Bronze > Silver > Gold)
# 1. Schema Enforcement & Type Casting (Bronze to Silver)
# Integer Validation: The uid in the logs is a mix of integers, strings, and "null".
# Convert this to a proper Integer type (using Int64 to allow for NaNs)
df_logs['uid'] = df_logs['uid'].fillna(0).astype(int)
# print(df_logs['uid'])

# Date Sanitization: The log ts column has an "impossible" date (31-02-2026).
# Identify these "corrupt" rows and move them to a separate DataFrame called quarantine_logs_df
df_logs['ts'] = pd.to_datetime(df_logs['ts'], dayfirst=False, format='mixed', errors='coerce')
quarantine_logs_df = df_logs[df_logs['ts'].isna()].copy()

df_logs = df_logs[df_logs['ts'].notna()].copy()
# print(df_logs)
# print(quarantine_logs_df)

# Deduplication: Ensure event_id is unique. If there are duplicates, keep the one with the latest timestamp
df_logs.sort_values(by=['event_id', 'ts'], ascending=True, inplace=True)
df_logs.drop_duplicates(subset='event_id', keep='last', inplace=True)
# print(df_logs)

# 2. JSON Parsing (Semi-Structured Data)
# Flattening: The info column contains JSON strings.
# Expand these strings into separate columns (e.g., action, page, amount)
# Hint: Use json.loads and pd.json_normalize
def safe_json_loads(x):
    try:
        return json.loads(x)
    except (ValueError, TypeError):
        # Error Handling: One log contains the string "INVALID_LOG_STRING".
        # Ensure your parser doesn't crash—catch the error and mark the action as "CORRUPT"
        return {"action": "CORRUPT"}

dicts = df_logs['info'].apply(safe_json_loads).tolist()
info_flattened = pd.json_normalize(dicts)

df_logs = pd.concat([df_logs.reset_index(drop=True), info_flattened], axis=1)
# print(df_logs)

# 3. Data Integrity & Relationships
# Orphan Records: Find logs with a uid that does not exist in the users_dim.csv file
uids = df_users['user_id'].tolist()

non_existent_logs = df_logs[~df_logs['uid'].isin(uids)].copy()

quarantine_logs_df = pd.concat([quarantine_logs_df, non_existent_logs], ignore_index=True)
quarantine_logs_df.drop_duplicates(subset='event_id', keep='last', inplace=True)
# print(quarantine_logs_df)


df_logs = df_logs[~df_logs['event_id'].isin(quarantine_logs_df['event_id'])] # drop inconsistent data from the main df
# print(df_logs)

# User Status Check: Join the logs with the user table and filter out any events triggered by users who are is_active = False
df_merged = pd.merge(df_logs, df_users, how='inner', left_on='uid', right_on='user_id')
non_active_user_events = df_merged[df_merged['is_active'] == False]
# print(non_active_user_events)

# 4. System Metadata (The Audit Trail)
# Ingestion Metrics: Add two metadata columns to your final DataFrame:
#       ingested_at: The current system time when you ran the script.
#       source_file: The name of the file the data came from.

df_merged['ingested_at'] = datetime.now()
df_merged['source_file'] = str(PATH + '/' + web_logs)

# Task: Incremental Load Simulation
# Imagine you run this script every day. You don't want to re-process the whole history.
# Create a function called get_new_records(existing_df, new_df) that compares the two based on event_id
# and only returns the records that are actually new.

def get_new_records(existing_df, new_df):
    return new_df[~new_df['event_id'].isin(existing_df['event_id'])]

web_logs_2 = 'gemini_web_logs_raw_day2.csv'
df_logs_2 = pd.read_csv(PATH + '/' + web_logs_2)

df_logs_2 = get_new_records(df_logs, df_logs_2)

# print(df_logs_2)

df_logs.to_csv('data templates/gemini_web_logs_archive.csv', mode='a', index=False, header=True) # a - append