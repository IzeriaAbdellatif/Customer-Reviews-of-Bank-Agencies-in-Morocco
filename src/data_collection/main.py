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


for region in regions:

    all_results = []

    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_MAP_API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.shortFormattedAddress,places.formattedAddress,places.types,places.primaryType,places.rating,places.userRatingCount,places.reviews,nextPageToken"
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
