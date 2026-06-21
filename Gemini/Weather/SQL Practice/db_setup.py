def setup(conn):
    cursor = conn.cursor()

    # 1. Dimension: Cities
    cursor.execute("""
                   CREATE TABLE dim_cities
                   (
                       city_id   INTEGER PRIMARY KEY,
                       city_name TEXT,
                       country   TEXT
                   )""")

    # 2. Dimension: Sensors
    cursor.execute("""
                   CREATE TABLE dim_sensors
                   (
                       sensor_id TEXT PRIMARY KEY,
                       model     TEXT,
                       status    TEXT
                   )""")

    # 3. Fact Table: Measurements
    cursor.execute("""
                   CREATE TABLE fact_measurements
                   (
                       id           INTEGER PRIMARY KEY AUTOINCREMENT,
                       city_id      INTEGER,
                       sensor_id    TEXT,
                       reading_type TEXT,
                       value        FLOAT,
                       ts           DATETIME,
                       FOREIGN KEY (city_id) REFERENCES dim_cities (city_id),
                       FOREIGN KEY (sensor_id) REFERENCES dim_sensors (sensor_id)
                   )""")

    # Populating Data
    cursor.execute("INSERT INTO dim_cities VALUES (1, 'London', 'UK'), (2, 'Kyiv', 'Ukraine')")
    cursor.execute(
        "INSERT INTO dim_sensors VALUES ('S_001', 'EcoTemp-v2', 'Active'), ('S_002', 'HydroSense', 'Maintenance'), ('S_003', 'HydroSense', 'Maintenance')")
    cursor.execute("""
                   INSERT INTO fact_measurements (city_id, sensor_id, reading_type, value, ts)
                   VALUES (1, 'S_001', 'temp', 15.5, '2026-02-14 10:00:00'),
                          (1, 'S_001', 'temp', 16.2, '2026-02-14 11:00:00'),
                          (2, 'S_002', 'humidity', 75.0, '2026-02-14 10:05:00'),
                          (2, 'S_002', 'temp', -2.5, '2026-02-14 10:10:00')
                   """)
    conn.commit()
    print("SQL Star Schema Ready!")