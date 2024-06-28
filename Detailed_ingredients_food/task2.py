import json
import os

files_with_ingredients = []

directory_path = "C:/Users/dsbha/OneDrive/Documents/Detailed_ingredients_food"

ingredient_units = {}

input_ingredients = []

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
        
        try:
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                
                normalized_data = {k.lower(): v for k, v in data.items()}
                
                for ingredient, details in normalized_data.items():
                    if ingredient not in ingredient_units:
                        ingredient_units[ingredient] = set()
                    ingredient_units[ingredient].add(details['unit'])
        except FileNotFoundError:
            print(f"File not found: {json_file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON file: {json_file_path}")
        except PermissionError:
            print(f"Permission denied when accessing the file: {json_file_path}")
        except Exception as e:
            print(f"An error occurred with file {json_file_path}: {e}")

while True:
    ingredient = input("Enter ingredient (or type 'stop' to finish): ").strip().lower()
    if ingredient == 'stop':
        break
    if ingredient not in ingredient_units:
        print(f"No data found for ingredient: {ingredient}. Please enter a valid ingredient.")
        continue
    quantity = input(f"Enter quantity for {ingredient} (measure): ").strip()
    unit_options = ingredient_units[ingredient]
    unit = input(f"Enter unit for {ingredient} (choose from {', '.join(unit_options)}): ").strip()
    if unit not in unit_options:
        print(f"Invalid unit for {ingredient}. Please choose from the available units.")
        continue
    input_ingredients.append((ingredient, quantity, unit))

for json_file in json_files:
    json_file_path = os.path.join(directory_path, json_file)
    
    all_ingredients_found = True
    
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            
            normalized_data = {k.lower(): v for k, v in data.items()}
            
            for ingredient, quantity, unit in input_ingredients:
                if (ingredient not in normalized_data) or (str(normalized_data[ingredient]['measure']) != quantity) or (normalized_data[ingredient]['unit'] != unit):
                    all_ingredients_found = False
                    break
    except FileNotFoundError:
        print(f"File not found: {json_file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON file: {json_file_path}")
    except PermissionError:
        print(f"Permission denied when accessing the file: {json_file_path}")
    except Exception as e:
        print(f"An error occurred with file {json_file_path}: {e}")

    if all_ingredients_found:
        files_with_ingredients.append(json_file)

print(files_with_ingredients)
