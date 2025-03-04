import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")
PLACE_ID = "ChIJj61dQgK6j4AR4GeTYWZsKWw"
URL = f"https://places.googleapis.com/v1/places/{PLACE_ID}"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": GOOGLE_MAP_API_KEY,
    "X-Goog-FieldMask": "id,displayName,reviews"
}

response = requests.get(URL, headers=headers)

# Print response
if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}, {response.text}")
