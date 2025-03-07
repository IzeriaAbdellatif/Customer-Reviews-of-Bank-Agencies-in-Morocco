from db_operations import insert_data
import os
import json

with open("../data/processed/data-of-banks.json", "r", encoding="utf-8") as file:
    try:
        data = json.load(file)  # Load JSON content
        for i in data:
            bank = {
                "id": i["id"],
                "name": i["displayName"]["text"],
                "branch": i["displayName"]["text"] + ", " + i["shortFormattedAddress"],
                "location": i["formattedAddress"],
                "rating": i["rating"],
                "user_rating_count": i["userRatingCount"],
            }
            print("* : " + str(bank))
            # print(i)
            for j in i["reviews"]:
                review1 = {
                    "id": j["name"].replace("places/" + i["id"] + "/reviews/", ""),
                    "bank_id": i["id"],
                    "author": j["authorAttribution"]["displayName"],
                    "rating": j["rating"],
                    "review_date": j["publishTime"],
                    "original_review_content": j["originalText"]["text"],
                    "review_content_language": j["originalText"]["languageCode"],
                    "translated_review_content": j["text"]["text"],
                }
                print("**** : " + str(review1))
            # insert_data("db1","banks",bank)
    except json.JSONDecodeError as e:
        print("Error reading data-of-banks.json: {e}")