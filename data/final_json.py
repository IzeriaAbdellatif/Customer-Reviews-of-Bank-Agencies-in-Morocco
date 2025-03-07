import os
import json

# Define the folder path
folder_path = "raw/"

list_of_data=[]

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):  # Process only JSON files
        file_path = os.path.join(folder_path, filename)

        # Read JSON file
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)  # Load JSON content
                for i in data:
                    list_of_data.append(i)
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")


directory = "processed/"
filename = "data-of-banks.json"

# Create the directory if it doesn't exist
os.makedirs(directory, exist_ok=True)

# Define the full path
file_path = os.path.join(directory, filename)

# Save JSON to file
with open(file_path, "w", encoding="utf-8") as json_file:
    json.dump(list_of_data, json_file, ensure_ascii=False, indent=4)

print("data is saved")

