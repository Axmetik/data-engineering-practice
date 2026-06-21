import json
import pandas as pd
import numpy as np

with open("raw_weather_api.json") as f:
    file_content = json.load(f)

data = file_content["data"]
df = pd.json_normalize(
    data,
    record_path=["measurements"],
    meta=[
        "city",
        ["coordinates", "lat"],
        ["coordinates", "lon"]
    ]
)

# A mask for temperatures
temp_mask = df["type"] == "temp"

df["temp_c"] = np.nan

# Only apply the conversion logic to the temperature rows
df.loc[temp_mask, "temp_c"] = np.where(
    df.loc[temp_mask, "unit"] == "C",
    df.loc[temp_mask, "value"],
    ((df.loc[temp_mask, "value"] - 32) * (5 / 9)).round(1)
)

df["generated_at"] = pd.to_datetime(file_content["metadata"]["generated_at"], format="mixed")

df.to_csv("standardized_weather.csv", index=False)

print(df)