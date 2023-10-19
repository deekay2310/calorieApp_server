import csv
from apps import App

# Initialize app and mongo client
app = App().app
mongo = App().mongo

# Process and insert food data
with open("food_data/calories.csv", "r", encoding="ISO-8859-1") as f:
    lines = f.readlines()
    
    for line in lines[1:]:
        cleaned_line = line[1:-2]
        food, calories = cleaned_line.split(",")
        mongo.db.food.insert_one({"food": food, "calories": calories})

# Process and insert exercise data
with open("food_data/exercise_dataset.csv", "r", encoding="utf-8") as exercise_data:
    reader = csv.reader(exercise_data, delimiter=",", quotechar='"')
    next(reader, None)  # Skip the header
    
    for row in reader:
        activity = row[0].strip('"')
        calories_per_kg_per_hour = float(row[1])
        mongo.db.activities.insert_one(
            {"activity": activity, "burn_rate": calories_per_kg_per_hour}
        )