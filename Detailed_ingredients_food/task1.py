import json
import os

input_ingredients = input("Enter ingredients: ").split(',')

files_with_ingredients = []

directory_path = "C:/Users/dsbha/OneDrive/Documents/Detailed_ingredients_food"

try:
    directory_contents = os.listdir(directory_path)
    json_files = [file for file in directory_contents if file.endswith('.json')]
except PermissionError:
    print("Permission denied when accessing the directory.")
    json_files = []

if not json_files:
    print(f"No JSON files found in directory: {directory_path}")
else:
    for json_file in json_files:
        json_file_path = os.path.join(directory_path, json_file)
        
        both_ingredients_found = False
        
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                
                normalized_data = {k.lower(): v for k, v in data.items()}
                
                for input_ingredient in input_ingredients:
                    normalized_ingredient = input_ingredient.strip().lower()
                    if normalized_ingredient not in normalized_data:
                        break
                else:
                    both_ingredients_found = True
        except FileNotFoundError:
            print(f"File not found: {json_file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON file: {json_file_path}")
        except PermissionError:
            print(f"Permission denied when accessing the file: {json_file_path}")
        except Exception as e:
            print(f"An error occurred with file {json_file_path}: {e}")

        if both_ingredients_found:
            files_with_ingredients.append(json_file)

print(files_with_ingredients)
