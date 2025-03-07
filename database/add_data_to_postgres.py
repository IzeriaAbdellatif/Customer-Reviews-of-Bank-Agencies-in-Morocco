from db_operations import insert_data
import os
import json

from textblob import TextBlob

count = 0

def get_sentiment(text):
    score = TextBlob(text).sentiment.polarity
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

with open("../data/processed/data-of-banks.json", "r", encoding="utf-8") as file:
    try:
        data = json.load(file)  # Load JSON content
        for i in data:
            bank = {
                "id": i.get("id", "N/A"),
                "name": i.get("displayName", {}).get("text", "Unknown Bank"),
                "branch": i.get("displayName", {}).get("text", "Unknown Bank") + ", " + i.get("shortFormattedAddress",
                                                                                              "No Address"),
                "location": i.get("formattedAddress", "No Location"),
                "rating": i.get("rating", 0.0),  # Default rating is 0.0
                "user_rating_count": i.get("userRatingCount", 0),  # Default rating count is 0
            }
            # print("* : " + str(bank))
            insert_data("db1", "banks", bank)
            for j in i.get("reviews", []):  # Ensure "reviews" exists, otherwise use an empty list
                review = {
                    "id": j.get("name", "N/A").replace("places/" + i.get("id", "N/A") + "/reviews/", ""),
                    "bank_id": i.get("id", "N/A"),
                    "author": j.get("authorAttribution", {}).get("displayName", "Anonymous"),
                    "rating": j.get("rating", 0),  # Default review rating is 0
                    "review_date": j.get("publishTime", "Unknown Date"),
                    "original_review_content": j.get("originalText", {}).get("text", "No Review Content"),
                    "review_content_language": j.get("originalText", {}).get("languageCode", "Unknown"),
                    "translated_review_content": j.get("text", {}).get("text", "No Review Content"),
                    "sentiment": get_sentiment(j.get("text", {}).get("text", "Neutral"))
                }
                # print("**** : " + str(review))
                insert_data("db1", "reviews", review)

            count = count + 1
    except json.JSONDecodeError as e:
        print(f"Error reading data-of-banks.json: {e}")

print(count)
