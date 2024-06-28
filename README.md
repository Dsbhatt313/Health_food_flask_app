Flask Health & Nutrition App Documentation:

Overview

This Flask application assists users in calculating their daily calorie needs and finding recipes based on input ingredients and selected meal types. It considers factors like age, height, weight, gender, activity level, and any medical issues. The application uses a dataset called `Nutritional Data.xlsx` to extract food names and their energy values (in Kcal), and JSON files to manage ingredients with their respective measures and units.

Setup Instructions

Prerequisites

Before you begin, ensure you have the following software installed on your system:

- Python 3.x
- Flask
- MySQL
- Pandas
- Operating System (Windows, macOS, or Linux)

Installation

1. Clone the Repository

   First, download the application's source code from the repository:

   ```bash
   git clone https://github.com/your-repository/Health_food_flask_app.git
   cd Health_food_flask_app
   ```

2. Create a Virtual Environment and Activate It

   This helps to manage dependencies and keep them separate from other projects:

   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows use `venv\Scripts\activate`
   ```

3. Install Required Packages

   Install all necessary packages listed in the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

4. Set Up the MySQL Database

   Create and configure the database to store user inputs:

   - Create a MySQL database named `health_data`.
   - Use the following SQL command to create the `submissions` table:

     ```sql
     CREATE TABLE submissions (
       id INT AUTO_INCREMENT PRIMARY KEY,
       selected_activities TEXT,
       activity_durations VARCHAR(255),
       gender VARCHAR(10),
       height_cm INT,
       weight_kg INT,
       meal_type VARCHAR(255),
       age_interval VARCHAR(255),
       medical_issues VARCHAR(255),
       ingredients TEXT
     );
     ```

5. Configure Environment Variables

   Create a file named `.env` in the root directory and add the following variables to secure sensitive information:

   ```bash
   SECRET_KEY=your_secret_key
   MYSQL_USER=your_mysql_user
   MYSQL_PASSWORD=your_mysql_password
   ```

6. Run the Flask Application

   Start the application using the following command:

   ```bash
   flask run
   ```

   The application should now be running on `http://127.0.0.1:8000`.

File Structure

Below is an overview of the project's file structure:

```plaintext
Health_food_flask_app/
│
├── static/
│   ├── style.css             # CSS for the application's styling
│   └── script.js             # JavaScript for added functionality
│
├── templates/
│   ├── index.html            # Main form for user input
│   ├── calorie_needs_result.html # Displays results
│   ├── error.html            # Error page
│   └── about.html            # About page
│
├── Detailed_ingredients_food/
│   ├── All in one.json       # JSON files with detailed ingredients
│   └── ...                   # Additional JSON files
│
├── app.py                    # Main application file
├── requirements.txt          # List of required packages
└── README.md                 # Project overview
```

Detailed Description

 `app.py`

This is the main file of the application. It includes:

- Flask Setup: Initializes and configures the Flask application.
- Routes:
  - `/`: Handles both GET and POST requests for the main form. On submission, it processes data, calculates calorie needs, finds recipes, and shows results.
  - `/error`: Renders the error page for any issues.
  - `/about`: Displays information about the application.
- Helper Functions:
  - `get_db_connection()`: Connects to the MySQL database.
  - `read_calorie_data()`: Reads calorie data from the `Nutritional Data.xlsx` file.
  - `find_matching_recipes(input_ingredients, selected_meal_type)`: Finds recipes based on ingredients and meal type.
  - `insert_submission(data)`: Inserts user data into the database.

`static/style.css`

This file contains CSS code that defines the look and feel of the application. It styles the forms and result pages to ensure a visually appealing layout.

`static/script.js`

Contains JavaScript code to enhance user interaction and the overall functionality of the application.

`templates/index.html`

This is the main form where users enter their details:

- Age
- Height (in cm)
- Weight (in kg)
- Gender
- Activity Level
- Activities and durations
- Meal type, age interval, medical issues
- Ingredients with quantity and unit

`templates/calorie_needs_result.html`

Displays the calculated daily calorie needs, matching recipes, the closest recipe within the calorie limit, and the remaining calories for the selected meal type.

`templates/error.html`

Shows an error message if something goes wrong during form submission or data processing.

`templates/about.html`

Provides information about the application, its purpose, and usage instructions.




Data Management

`Nutritional Data.xlsx`

The main dataset provided by the company. It is used to create the JSON files, ensuring consistency and easy reference. It contains food names and their corresponding energy values (in Kcal).

`Detailed_ingredients_food`

Contains JSON files for each food item, named to match the food names in the Excel dataset. Each JSON file lists ingredients with their measures and units, ensuring easy data reference and retrieval.

Configuration

Environment Variables

- SECRET_KEY: A key used by Flask to secure the session.
- MYSQL_USER: Your MySQL username.
- MYSQL_PASSWORD: Your MySQL password.

Usage Instructions

1. Access the Form

   Open your web browser and go to `http://127.0.0.1:8000` to access the application.

2. Fill Out the Form

   - Enter your age, height (in cm), and weight (in kg).
   - Select your gender and activity level.
   - Choose your activities and durations.
   - Select your meal type, age interval, and any medical issues.
   - Input the ingredients you have, specifying the quantity and unit for each.

3. Submit the Form

   Click the "Submit" button to process your input.

4. View Results

   The results page will show your estimated daily calorie needs, matching recipes, the closest recipe within the calorie limit, and remaining calories for your selected meal type.

Error Handling

The application includes mechanisms for handling errors related to database connections, form submissions, and data processing. If an error occurs, it will be logged, and you will be redirected to the form with an error message.

Security Considerations

- Secret Key Management: Store the secret key in an environment variable to prevent exposure in the source code.
- Database Credentials: Keep database credentials in environment variables for security.

Logging

The application uses the `logging` module to log information and errors, which aids in debugging and monitoring the application.

Contributions

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

Contact

For questions or support, open an issue in the repository or contact the maintainer at dsbhatt1234@gmail.com.











BMR and Calorie Needs Calculation Documentation:

Overview
The Basal Metabolic Rate (BMR) calculation estimates the number of calories required to keep the body functioning at rest. This value can be adjusted to account for different activity levels to determine total daily calorie needs.

Equations Used

1. Mifflin-St Jeor Equation for BMR:
    - For men:
    \[ BMR = 10 \times \text{weight in kg} + 6.25 \times \text{height in cm} - 5 \times \text{age} + 5 \]
    - For women:
    \[ BMR = 10 \times \text{weight in kg} + 6.25 \times \text{height in cm} - 5 \times \text{age} - 161 \]

2. Total Daily Calorie Needs:
    - The BMR is multiplied by an activity multiplier that reflects the user's activity level to estimate total daily calorie needs.

Implementation in `app.py`

Below is the specific code snippet from `app.py` that performs the BMR and calorie needs calculation:

```python
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
```

Explanation of the BMR and Calorie Needs Calculation Steps

1. Extract User Input:
    - `data = request.json` extracts the user input from the JSON body of the request.
    - `gender`, `age`, `height_cm`, `weight_kg`, and `activity_level` are extracted from the input data.

2. Define Activity Multipliers:
    - `activity_multipliers` is a dictionary that maps activity levels to corresponding multipliers.
        - Sedentary (little or no exercise): `1.2`
        - Moderately active (moderate exercise/sports 3-5 days/week): `1.55`
        - Active (hard exercise/sports 6-7 days a week): `1.725`

3. Calculate BMR:
    - This checks the gender and uses the corresponding Mifflin-St Jeor equation to calculate the BMR.
        - For men: 
        \[ BMR = 10 \times \text{weight in kg} + 6.25 \times \text{height in cm} - 5 \times \text{age} + 5 \]
        - For women: 
        \[ BMR = 10 \times \text{weight in kg} + 6.25 \times \text{height in cm} - 5 \times \text{age} - 161 \]

4. Calculate Total Daily Calorie Needs:
    - The BMR is multiplied by the appropriate activity multiplier to estimate the total daily calorie needs:
        - `calorie_needs = bmr * activity_multipliers[activity_level]`

5. Return Results:
    - The calculated BMR and total daily calorie needs are returned as a JSON response.


Example Usage

When a user submits the form with their details, the front-end JavaScript sends a POST request to the `/` endpoint with the user’s age, gender, height, weight, and activity level.

Example request payload:
```json
{
    "gender": "Male",
    "age": 30,
    "height_cm": 175,
    "weight_kg": 70,
    "activity_level": "moderately_active"
}
```

Example response:
```json
{
    "bmr": 1665.0,
    "calorie_needs": 2580.75
}
```

Summary

The BMR and total daily calorie needs calculation in the `index` function of `app.py` uses the Mifflin-St Jeor equation, adjusted for gender, to estimate BMR. This BMR is then multiplied by an activity multiplier based on the user’s activity level to determine the total daily calorie needs. The function extracts user inputs, performs the calculations, and returns the results as a JSON response. This documentation explains the purpose and process of each step to help developers understand and maintain the code.
