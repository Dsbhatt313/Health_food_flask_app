import mysql.connector
from flask_wtf import CSRFProtect
from flask import Flask, render_template, request, url_for, redirect, flash, jsonify
import json
import os
import pandas as pd
import logging

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')  # Use environment variable for the secret key

csrf = CSRFProtect(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Define your paths and other variables
directory_path = "C:/Users/dsbha/OneDrive/Documents/Detailed_ingredients_food"
excel_file_path = "C:/Users/dsbha/OneDrive/Desktop/Nutritional Data.xlsx"

meal_type_calories = {
    "Breakfast": {
        "Male": {
            "Sedentary": 520,
            "Moderately Active": 565,
            "Active": 635
        },
        "Female": {
            "Sedentary": 430,
            "Moderately Active": 475,
            "Active": 520
        }
    },
    "Lunch": {
        "Male": {
            "Sedentary": 750,
            "Moderately Active": 815,
            "Active": 915
        },
        "Female": {
            "Sedentary": 620,
            "Moderately Active": 685,
            "Active": 750
        }
    },
    "Evening Snack": {
        "Male": {
            "Sedentary": 290,
            "Moderately Active": 315,
            "Active": 355
        },
        "Female": {
            "Sedentary": 240,
            "Moderately Active": 265,
            "Active": 290
        }
    },
    "Dinner": {
        "Male": {
            "Sedentary": 635,
            "Moderately Active": 690,
            "Active": 775
        },
        "Female": {
            "Sedentary": 525,
            "Moderately Active": 580,
            "Active": 635
        }
    }
}


# Define activity multipliers globally
activity_multipliers = {
    'sedentary': 1.2,
    'moderately_active': 1.55,
    'active': 1.725,
}

activities = {
    "sedentary": [
        "Desk work", "Watching TV", "Reading", "Sitting", "Cooking", "Household chores", "Driving"
    ],
    "moderately_active": [
        "Jogging", "Relaxed cycling", "Relaxed swimming", "Dancing", "Gardening", "Playing recreational sports",
        "Moderate hiking", "Moderate-intensity workouts"
    ],
    "active": [
        "Running", "High-intensity workouts", "Circuit training", "Playing intense sports", "CrossFit", "Intense swimming",
        "Intense cycling", "Martial arts"
    ]
}

meal_types = ["Breakfast", "Lunch", "Evening Snack", "Dinner"]

age_intervals = ["0-17 years", "18-35 years", "36-55 years", "56-75 years", "76 years and above"]

medical_issues = [
    "None", "Diabetes", "High Blood Pressure", "High Cholesterol", "Heart Disease", "Obesity", "Arthritis", "Asthma",
    "Allergies", "Thyroid Disorders", "Gastrointestinal Disorders", "Mental Health Disorders", "Cancer", "Osteoporosis",
    "Sleep Disorders", "Kidney Disease", "Liver Disease", "Stroke", "Anemia", "HIV/AIDS", "Other"
]

activity_durations = [
    "Less than 15 minutes", "15-30 minutes", "30-45 minutes", "45-60 minutes", "1-2 hours", "2-3 hours", "3-4 hours",
    "More than 4 hours"
]

genders = ["Male", "Female"]

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'healthapp'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'health_data'

# Initialize MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

def read_calorie_data():
    df = pd.read_excel(excel_file_path)
    calorie_dict = {row['Food Name'].strip().lower(): row['Energy(Kcal)'] for _, row in df.iterrows()}
    #logging.info("Calorie data keys: %s", calorie_dict.keys())  # Logging
    return calorie_dict

calorie_data = read_calorie_data()

def find_matching_recipes(input_ingredients, selected_meal_type):
    files_with_ingredients = []
    json_files = [file for file in os.listdir(directory_path) if file.endswith('.json')]
    
    for json_file in json_files:
        json_file_path = os.path.join(directory_path, json_file)
        all_ingredients_found = True
        
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            normalized_data = {k.lower(): v for k, v in data.items()}
            
            for ingredient, quantity, unit in input_ingredients:
                ingredient = ingredient.lower().strip()
                if (ingredient not in normalized_data) or (str(normalized_data[ingredient]['measure']) != quantity) or (normalized_data[ingredient]['unit'] != unit):
                    all_ingredients_found = False
                    break

        if all_ingredients_found:
            files_with_ingredients.append(json_file.replace('.json', '').lower().strip())

    #logging.info("Matching recipes: %s", files_with_ingredients)  # Logging
    return files_with_ingredients


# Example endpoint to get data
@app.route('/api/get_data', methods=['GET'])
def get_data():
    # Example data
    data = {"message": "Hello, World!"}
    return jsonify(data)

# Example endpoint to receive data
@app.route('/api/send_data', methods=['POST'])
def send_data():
    # Get data from request
    received_data = request.json
    # Process the data here
    response = {"status": "success", "data": received_data}
    return jsonify(response)


@app.route('/', methods=['GET', 'POST'])
@csrf.exempt
def index():
    if request.method == 'POST':
        try:
            # Read form inputs
            age = int(request.form['age'])
            height_cm = float(request.form['height_cm'])
            weight_kg = float(request.form['weight_kg'])
            gender = request.form['gender']
            activity_level = request.form['activity_level']
            selected_meal_type = request.form['meal_types']

            if gender not in genders or activity_level not in activity_multipliers.keys():
                raise ValueError("Invalid input")

            # Calculate BMR and calorie needs
            if gender == 'Male':
                bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
            else:
                bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

            calorie_needs = bmr * activity_multipliers[activity_level]

            # Read and process ingredients
            ingredients_input = request.form['ingredients'].lower().strip()
            ingredients_list = [ing.strip() for ing in ingredients_input.split(',')]
            input_ingredients = []
            for ingredient in ingredients_list:
                parts = ingredient.split()
                quantity = parts[0]
                unit = parts[1]
                ing_name = ' '.join(parts[2:])
                input_ingredients.append((ing_name, quantity, unit))

            logging.info("Input ingredients: %s", input_ingredients)

            # Find matching recipes
            matching_recipes = find_matching_recipes(input_ingredients, selected_meal_type)
            recipe_calories = []
            closest_recipe = None
            closest_calories = float('inf')

            meal_calorie_limit = meal_type_calories[selected_meal_type][gender][activity_level.replace('_', ' ').title()]

            for recipe in matching_recipes:
                if recipe in calorie_data:
                    calories_data = calorie_data[recipe]
                    if isinstance(calories_data, str):
                        calories = float(calories_data.split()[0])
                    else:
                        calories = float(calories_data)

                    recipe_calories.append((recipe, calories))

                    if calories <= meal_calorie_limit and (meal_calorie_limit - calories) < closest_calories:
                        closest_calories = meal_calorie_limit - calories
                        closest_recipe = (recipe, calories)

            # Calculate remaining calories after the closest recipe
            remaining_calories = meal_calorie_limit - (closest_recipe[1] if closest_recipe else 0)


            # Save the submission
            selected_activities = request.form.getlist('activities')
            data = (
                ','.join(selected_activities),
                request.form['activity_durations'],
                gender,
                int(height_cm),
                int(weight_kg),
                request.form['meal_types'],
                request.form['age_interval'],
                request.form['medical_issues'],
                ingredients_input
            )
            insert_submission(data)

            return render_template(
                'calorie_needs_result.html',
                gender=gender,
                age=age,
                height_cm=height_cm,
                weight_kg=weight_kg,
                activity_level=activity_level,
                ingredients=ingredients_input,
                matching_recipes=recipe_calories,
                total_calories=sum([calories for _, calories in recipe_calories]),
                calorie_needs=calorie_needs,
                meal_calorie_limit=meal_calorie_limit,
                remaining_calories=remaining_calories,
                closest_recipe=closest_recipe[0] if closest_recipe else None,
                closest_calories=closest_recipe[1] if closest_recipe else None,
                activities=selected_activities,
                meal_type=selected_meal_type
            )
        except ValueError as e:
            logging.error("Error: %s", e)
            flash('Invalid input data, please try again.')
            return redirect(url_for('index'))
    return render_template('index.html', activities=activities, meal_types=meal_types, age_intervals=age_intervals, 
                           medical_issues=medical_issues, activity_durations=activity_durations, genders=genders)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

def insert_submission(data):
    connection = get_db_connection()
    cursor = connection.cursor()
    sql = """
        INSERT INTO submissions (activities, activity_durations, gender, heights_cm, weights_kg, meal_types, age_interval, medical_issues, ingredients)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, data)
    connection.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    app.run(debug=True, port=8000)