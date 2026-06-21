import json
import pandas as pd

with open('nested_api.json') as f:
    response = json.load(f)

data = response["data"]
df = pd.json_normalize(data, ["forecast", "hourly"], ["city",])

print(df)