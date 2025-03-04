import requests
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")
# PLACE_ID = "ChIJj61dQgK6j4AR4GeTYWZsKWw"
# URL = f"https://places.googleapis.com/v1/places/{PLACE_ID}"

# headers = {
#     "Content-Type": "application/json",
#     "X-Goog-Api-Key": GOOGLE_MAP_API_KEY,
#     "X-Goog-FieldMask": "id,displayName,reviews"
# }

# response = requests.get(URL, headers=headers)

# # Print response
# if response.status_code == 200:
#     print(response.json())
# else:
#     print(f"Error: {response.status_code}, {response.text}")


regions = ["Tangier-Tetouan-Al Hoceima",
           "L'Oriental",
           "Fez-Meknes",
           "Rabat-Salé-Kénitra",
           "Béni Mellal-Khénifra",
           "Casablanca-Settat",
           "Marrakech-Safi",
           "Drâa-Tafilalet",
           "Souss-Massa",
           "Guelmim-Oued Noun",
           "Laâyoune-Sakia El Hamra",
           "Dakhla-Oued Ed-Dahab"]

# for region in regions :
#     # Step 1: Get bank agencies using Text Search API
#     search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=bank+near+{region}&key={GOOGLE_MAP_API_KEY}"
#     search_response = requests.get(search_url).json()

#     # Check if results are returned
#     places = search_response.get("results", [])
#     if not places:
#         print("No bank agencies found.")
#         exit()

# Step 1: Get bank agencies using Text Search API
# search_url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=bank+near+Rabat-Salé-Kénitra&key={GOOGLE_MAP_API_KEY}"
# search_response = requests.get(search_url).json()

# # Check if results are returned
# places = search_response.get("results", [])
# if not places:
#     print("No bank agencies found.")
#     exit()


#for region in regions:

region = "Rabat-Salé-Kénitra"

all_results = []

url = "https://places.googleapis.com/v1/places:searchText"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": GOOGLE_MAP_API_KEY,
    "X-Goog-FieldMask": "places.id,places.displayName,places.addressComponents,places.types,places.primaryType,places.rating,places.userRatingCount,places.reviews,places.accessibilityOptions,nextPageToken"
}

data = {
    "textQuery": f"bank near {region}, Morocco"
}
while True:
    response = requests.post(url, json=data, headers=headers)
    json_response = response.json()

    all_results.extend(json_response.get("places", []))

    next_page_token = json_response.get("nextPageToken")
    if not next_page_token:
        break  # No more pages

    time.sleep(2)

    data["pageToken"] = next_page_token

    # Define the directory and filename
directory = "./data"
filename = f"{region}-banks.json"

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Define the full path
file_path = os.path.join(directory, filename)

# Save JSON to file
with open(file_path, "w", encoding="utf-8") as json_file:
    json.dump(all_results, json_file, ensure_ascii=False, indent=4)

print(f"JSON file for {region} saved at: {file_path}")
