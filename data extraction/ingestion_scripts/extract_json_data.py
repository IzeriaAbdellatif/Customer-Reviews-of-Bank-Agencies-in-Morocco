import requests
import os
from pathlib import Path
from dotenv import load_dotenv
import json
import time

# Get the project root directory
PROJECT_ROOT = Path(__file__).parents[2]  # Go up 3 levels to reach project root
ENV_PATH = PROJECT_ROOT / 'config/.env'
print(f"Loading environment variables from: {ENV_PATH}")

load_dotenv(ENV_PATH)

# GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")

# this will not use the api, it is just for testing airflow
GOOGLE_MAP_API_KEY = os.getenv("")


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

regions_path = PROJECT_ROOT / "data extraction/ingestion_scripts/cities.json"

with open(regions_path, 'r') as file:
    regions_dict = json.load(file)

filtered_cities = list(set(city for region in regions_dict.values() for city in region))

places = filtered_cities[:-3] + regions[-3:]

banks = [
    "ARAB BANK",
    "ATTIJARIWAFA BANK",
    "Al Barid Bank",
    "BANQUE POPULAIRE",
    "BANK OF AFRICA",
    "BMCI",
    "credit agricole",
    "CFG BANK",
    "CIH BANK",
    "CREDIT DU MAROC",
    "SOCIETE GENERALE",
    "UMNIA BANK",
    "AL AKHDAR BANK",
    "BANK AL YOUSR",
    "UMNIA BANK"

]

url = "https://places.googleapis.com/v1/places:searchText"


all_results = []

# Create a city to region mapping
city_to_region = {}
for region, cities in regions_dict.items():
    for city in cities:
        city_to_region[city.upper()] = region

# Add regions themselves to the mapping
for region in regions:
    city_to_region[region.upper()] = region

# In your main loop
for place in places:
    print(f"Processing banks in {place}...")
    
    for bank in banks:
        print(f"Fetching data for {bank} in {place}")
        data = {
            "textQuery": f"{bank} near {place}, Morocco"
        }

        headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAP_API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.shortFormattedAddress,places.formattedAddress,places.types,places.primaryType,places.rating,places.userRatingCount,places.reviews,nextPageToken"
        }
        
        while True:
            response = requests.post(url, json=data, headers=headers)
            json_response = response.json()

            if "places" in json_response:
                # Look up the region for each place
                for place_data in json_response["places"]:
                    # Get the region from our mapping, fallback to the original region if not found
                    place_data["region"] = city_to_region.get(place.upper(), place)
                    place_data["bank_name"] = bank
                
                all_results.extend(json_response["places"])
                print(f"Found {len(json_response['places'])} results")

            next_page_token = json_response.get("nextPageToken")
            if not next_page_token:
                break  # No more pages

            time.sleep(2)
            data["pageToken"] = next_page_token

# Save all results to a single JSON file
output_file = PROJECT_ROOT / "data extraction/raw_json/data-of-banks-2.json"

# Create parent directories if they don't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Save JSON to file
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(all_results, json_file, ensure_ascii=False, indent=4)

print(f"All results saved to: {output_file}")
print(f"Total places collected: {len(all_results)}")


#Test API connection
# headers = {
# "Content-Type": "application/json",
# "X-Goog-Api-Key": GOOGLE_MAP_API_KEY,
# "X-Goog-FieldMask": "places.id,places.displayName,places.shortFormattedAddress,places.formattedAddress,places.types,places.primaryType,places.rating,places.userRatingCount,places.reviews,nextPageToken"
# }
# url = "https://places.googleapis.com/v1/places:searchText"
# test_data = {
#     "textQuery": "BMCI near Casablanca, Morocco"
# }

# print(GOOGLE_MAP_API_KEY)
# response = requests.post(url, json=test_data, headers=headers)
# print("API Response Status:", response.status_code)
# print("API Response Content:", response.json())