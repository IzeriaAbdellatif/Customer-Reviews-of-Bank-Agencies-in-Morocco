import json
import psycopg2
from dotenv import load_dotenv
import os
from pathlib import Path
from transformers import pipeline
from typing import Optional
import re

# Add new imports for models
sentiment_analyzer = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
topic_classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define topics for classification
TOPICS = [
    "security",
    "customer service",
    "staff behavior",
    "account management",
    "ATM issues",
    "mobile banking",
    "billing",
    "wait times",
    "loans",
    "other"
    ]

def clean_text(text: Optional[str]) -> Optional[str]:
    """Remove emojis and special characters from text"""
    if not text:
        return None
    
    # Remove emojis and special characters
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    
    # Clean the text
    text = emoji_pattern.sub(r'', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text.strip() if text.strip() else None

def get_sentiment(text: Optional[str]) -> Optional[str]:
    """Get sentiment from text"""
    # Clean the text first
    cleaned_text = clean_text(text)
    
    if not cleaned_text:
        return None
        
    try:
        result = sentiment_analyzer(cleaned_text)
        # Convert 5-class sentiment to three classes
        score = float(result[0]['label'].split()[0])
        if score > 3:
            return "positive"
        elif score < 3:
            return "negative"
        else:
            return "neutral"
    except Exception as e:
        print(f"Error in sentiment analysis: {str(e)}")
        return None

def get_topic(text: Optional[str]) -> str:
    """Get topic from text"""
    if not text:
        return None
    try:

        result = topic_classifier(
            text, 
            TOPICS,
            multi_label=False,
            hypothesis_template="This text is about {}."
        )
        # Add confidence threshold
        if result['scores'][0] < 0.3:
            return "other"
        return result['labels'][0]
    except Exception as e:
        print(f"Error in topic classification: {str(e)}")
        return None

# Get the project root directory
PROJECT_ROOT = Path(__file__).parents[1]  # Go up 3 levels to reach project root
ENV_PATH = PROJECT_ROOT / 'config/.env'
print(f"Loading environment variables from: {ENV_PATH}")

load_dotenv(ENV_PATH)

# Database connection parameters
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Connect and create cursor
try:
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    print("Successfully connected to PostgreSQL")
except Exception as e:
    print(f"Error connecting to PostgreSQL: {e}")
    exit(1)

# Create the SQL table
create_table_query ='''
CREATE TABLE IF NOT EXISTS new_bank_branches (
    id TEXT PRIMARY KEY,
    branch_name TEXT,
    primary_type TEXT,
    bank_name TEXT,
    region TEXT,
    address TEXT,      
    rating REAL,
    user_rating_count INTEGER,
    review_1 TEXT,
    rating_1 INTEGER,
    person_id_1 TEXT,
    time_1 TIMESTAMP,
    review_2 TEXT,
    rating_2 INTEGER,
    person_id_2 TEXT,
    time_2 TIMESTAMP,
    review_3 TEXT,
    rating_3 INTEGER,
    person_id_3 TEXT,
    time_3 TIMESTAMP,
    review_4 TEXT,
    rating_4 INTEGER,
    person_id_4 TEXT,
    time_4 TIMESTAMP,
    review_5 TEXT,
    rating_5 INTEGER,
    person_id_5 TEXT,
    time_5 TIMESTAMP,
    review_1_sentiment TEXT,
    review_1_topic TEXT,
    review_2_sentiment TEXT,
    review_2_topic TEXT,
    review_3_sentiment TEXT,
    review_3_topic TEXT,
    review_4_sentiment TEXT,
    review_4_topic TEXT,
    review_5_sentiment TEXT,
    review_5_topic TEXT
)
'''
# Create table
try:
    cursor.execute(create_table_query)
    conn.commit()
    print("Table created successfully")
except Exception as e:
    print(f"Error creating table: {str(e)}")
    conn.rollback()

# Path to the JSON file
json_path = PROJECT_ROOT / 'data extraction/raw_json/data-of-banks-2.json'
# Load the JSON data
with open(json_path, 'r') as file:
    data = json.load(file)

# Process the JSON data and insert into the database
for bank in data:
    try:
        id = bank.get('id', None)
        display_name = bank.get('displayName', {}).get('text', None)
        address = bank.get('shortFormattedAddress', None)
        full_address = bank.get('formattedAddress', None)
        region = bank.get('region', None)
        primary_type = bank.get('primaryType', None)
        bank_name = bank.get('bank_name',None)
        rating = bank.get('rating', None)
        user_rating_count = bank.get('userRatingCount', 0)

        reviews = bank.get('reviews', [])
        review_data = []
        sentiment_topic_data = []

        for i in range(5):
            if i < len(reviews):
                review = reviews[i]
                review_text = review.get('text', {}).get('text', None)
                review_rating = review.get('rating', None)
                person_id = review.get('authorAttribution', {}).get('displayName', None)
                time = review.get('publishTime', None)
                
                # Get sentiment and topic
                sentiment = get_sentiment(review_text)
                topic = get_topic(review_text)
            else:
                review_text = review_rating = person_id = time = sentiment = topic = None
            
            review_data.extend([review_text, review_rating, person_id, time])
            sentiment_topic_data.extend([sentiment, topic])

        # First try to delete any existing record with the same ID
        cursor.execute('DELETE FROM new_bank_branches WHERE id = %s', (id,))

        cursor.execute('''
        INSERT INTO new_bank_branches (id, branch_name, primary_type, bank_name, region, address, rating, user_rating_count,
                                    review_1, rating_1, person_id_1, time_1,
                                    review_2, rating_2, person_id_2, time_2,
                                    review_3, rating_3, person_id_3, time_3,
                                    review_4, rating_4, person_id_4, time_4,
                                    review_5, rating_5, person_id_5, time_5,
                                    review_1_sentiment, review_1_topic,
                                    review_2_sentiment, review_2_topic,
                                    review_3_sentiment, review_3_topic,
                                    review_4_sentiment, review_4_topic,
                                    review_5_sentiment, review_5_topic)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (id, f"{display_name} {address}", primary_type, bank_name, region, full_address, rating, user_rating_count, *review_data, *sentiment_topic_data))
        
        conn.commit()
        print(f"Successfully inserted data for bank ID: {id}")
        
    except Exception as e:
        print(f"Error processing bank with ID {id}: {str(e)}")
        conn.rollback()
        continue

# Close connections at the very end
cursor.close()
conn.close()
print("Data successfully inserted into PostgreSQL database")