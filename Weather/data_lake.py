import json
import os

# Simulating a complex API response
api_response = {
    "status": "success",
    "metadata": {
        "generated_at": "2026-02-11T10:00:00Z",
        "api_version": "v2.1"
    },
    "data": [
        {
            "city": "London",
            "coordinates": {"lat": 51.5074, "lon": -0.1278},
            "measurements": [
                {"type": "temp", "value": 12, "unit": "C"},
                {"type": "humidity", "value": 82, "unit": "%"}
            ]
        },
        {
            "city": "New York",
            "coordinates": {"lat": 40.7128, "lon": -74.0060},
            "measurements": [
                {"type": "temp", "value": 54, "unit": "F"},
                {"type": "humidity", "value": 60, "unit": "%"}
            ]
        }
    ]
}

nested_api = {
    "data": [
        {
            "city": "London",
            "forecast": {
                "hourly": [
                    {"type": "temp", "value": 12},
                    {"type": "humidity", "value": 82}
                ]
            }
        }
    ]
}

# Save it as a JSON file to simulate an API download
with open('nested_api.json', 'w') as f:
    # json.dump(api_response, f)
    json.dump(nested_api, f)

print("JSON 'API Response' created!")
