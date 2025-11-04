import requests
import json

url = "http://localhost:8001/ingest"
payload = {"topic": "London Rental Market"}
headers = {"Content-Type": "application/json"}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    response.raise_for_status()  # Raise an exception for bad status codes
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
