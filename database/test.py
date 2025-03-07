from db_operations import insert_data

bank1 = {
    "id": 1,
    "name": "CIH",
    "branch": "casa",
    "location": "casa, morocco",
    "rating": 3,
    "user_rating_count": 100
}

insert_data("db1", "banks", bank1)

review1 = {
    "id": "1",
    "bank_id": "0",
    "author": "tahiri",
    "rating": "3",
    "review_date": "2021-09-22",
    "original_review_content": "good!",
    "review_content_language": "en",
    "translated_review_content": "good!"
}

insert_data("db1", "reviews", review1)