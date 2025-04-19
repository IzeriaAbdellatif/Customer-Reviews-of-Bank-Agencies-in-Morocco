import requests
import os
from dotenv import load_dotenv
import json
import time

load_dotenv()

GOOGLE_MAP_API_KEY = os.getenv("GOOGLE_MAP_API_KEY")

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

regions_path = "/home/aizeria/Documents/Customer-Reviews-of-Bank-Agencies-in-Morocco/cities.json"

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
                # Add region and bank information to each place
                for place_data in json_response["places"]:
                    place_data["region"] = place
                    place_data["bank_name"] = bank
                
                all_results.extend(json_response["places"])
                print(f"Found {len(json_response['places'])} results")

            next_page_token = json_response.get("nextPageToken")
            if not next_page_token:
                break  # No more pages

            time.sleep(2)
            data["pageToken"] = next_page_token

# Save all results to a single JSON file
output_file = "./data-of-banks.json"

# Create parent directories if they don't exist
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# Save JSON to file
with open(output_file, "w", encoding="utf-8") as json_file:
    json.dump(all_results, json_file, ensure_ascii=False, indent=4)

print(f"All results saved to: {output_file}")
print(f"Total places collected: {len(all_results)}")


# Test API connection
# test_data = {
#     "textQuery": "BMCI near Casablanca, Morocco"
# }

# print(GOOGLE_MAP_API_KEY)
# response = requests.post(url, json=test_data, headers=headers)
# print("API Response Status:", response.status_code)
# print("API Response Content:", response.json())