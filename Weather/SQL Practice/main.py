import sqlite3
import pandas as pd

from db_setup import setup

conn = sqlite3.connect(':memory:')

setup(conn)

# Task: Write a query that shows the city_name, reading_type, and value.
# Requirement: You must use an INNER JOIN between fact_measurements and dim_cities.
city_measurement_join_query = ('''
    SELECT 
        city.city_name AS city, 
        fm.reading_type AS type,
        fm.value
    FROM dim_cities AS city
    INNER JOIN fact_measurements AS fm
    ON fm.city_id = city.city_id
''')

result_df = pd.read_sql(city_measurement_join_query, conn)
print('1.\n', result_df, '\n')

# Task: Select all measurements. Create a new column called reading_status.
#   If reading_type is 'temp' and value < 0, then 'Freezing'.
#   If reading_type is 'temp' and value >= 0, then 'Normal'.
#   For everything else, 'N/A'.
measurements_query = '''
    SELECT *, 
        CASE
            WHEN reading_type = "temp" AND value < 0 THEN "Freezing"
            WHEN reading_type = "temp" AND value >= 0 THEN "Normal"
            ELSE "N/A"
        END AS reading_status
    FROM fact_measurements
'''

result_df = pd.read_sql(measurements_query, conn)
print('2.\n',result_df, '\n')


# Task: Find the average value for each city_name and reading_type.
# Requirement: Use JOIN, GROUP BY, and AVG().
grouped_cities_plus_avg_values = '''
    SELECT
        city.city_name,
        fm.reading_type,
        AVG(fm.value) AS avg_value
    FROM fact_measurements fm
    JOIN dim_cities city
    ON fm.city_id = city.city_id
    GROUP BY city.city_name, fm.reading_type
    ORDER BY city.city_name, fm.reading_type
'''

result_df = pd.read_sql(grouped_cities_plus_avg_values, conn)
print('3.\n',result_df, '\n')

# Task: Write a query to find if there are any sensors in dim_sensors that have never reported a measurement.
# Hint: Use a LEFT JOIN and look for where the fact table ID IS NULL
unreported_sensors_query = '''
    SELECT
        s.*
    FROM dim_sensors s
    LEFT JOIN fact_measurements fm
    ON s.sensor_id = fm.sensor_id
    WHERE fm.sensor_id IS NULL;

'''

result_df = pd.read_sql(unreported_sensors_query, conn)
print('4.\n',result_df, '\n')