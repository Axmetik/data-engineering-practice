import pandas as pd
import numpy as np
import os

# Create a directory for our landing zone
os.makedirs('landing_zone', exist_ok=True)

# Day 1: Standard Data
day1 = pd.DataFrame({
    'sensor_id': ['S01', 'S02', 'S01', 'S03'],
    'ts': ['2026-02-08 08:00', '2026-02-08 08:05', '2026-02-08 09:00', '2026-02-08 09:10'],
    'reading_type': ['temp', 'temp', 'temp', 'energy'],
    'value': [21.5, 22.1, 21.8, 450.0]
})

# Day 2: Duplicates and Malformed Data
day2 = pd.DataFrame({
    'sensor_id': ['S01', 'S02', 'S04', 'S02'], # S04 is a new sensor
    'ts': ['2026-02-08 09:00', '2026-02-09 08:00', '2026-02-09 08:15', '2026-02-09 08:00'], # Dupe S02
    'reading_type': ['temp', 'temp', 'energy', 'temp'],
    'value': [21.8, 23.0, 500.0, 23.0]
})

# Day 3: Schema Drift (New column added)
day3 = pd.DataFrame({
    'sensor_id': ['S01', 'S05'],
    'ts': ['2026-02-10 10:00', '2026-02-10 10:30'],
    'reading_type': ['temp', 'temp'],
    'value': [22.5, 19.8],
    'battery_level': [0.85, 0.92] # The new column
})

# day1.to_csv('landing_zone/day1.csv', index=False)
# day2.to_csv('landing_zone/day2.csv', index=False)
# day3.to_csv('landing_zone/day3.csv', index=False)

print("Landing zone prepared with 3 days of data!")

day4_data = pd.DataFrame({
    'sensor_id': ['S01', np.nan, 'S03', 'S05'],
    'ts': ['2026-02-11 08:00', '2026-02-11 08:05', '2026-02-11 09:00', 'Invalid_Date'],
    'reading_type': ['temp', 'temp', 'energy', 'temp'],
    'value': [500.0, 22.1, -10.0, 20.0], # 500 is impossible, -10 is impossible
    'battery_level': [0.80, 0.75, 0.90, 0.88]
})

day4_data.to_csv('landing_zone/day4_corrupt.csv', index=False)
print("File 'day4_corrupt.csv' generated. Time to test your validation logic!")