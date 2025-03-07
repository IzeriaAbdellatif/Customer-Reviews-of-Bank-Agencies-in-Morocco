import os
import json

# Define the folder path
folder_path = "raw/"

count = 0

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):  # Process only JSON files
        file_path = os.path.join(folder_path, filename)

        # Read JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)  # Load JSON content
                for i in data:
                    count += 1
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")

print("banks : "+ str(count))

print("reviews : "+str(count * 5))
