import json
import bcrypt
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from pymongo import MongoClient
import mongomock
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager
from datetime import datetime, timedelta
from functools import reduce
from bson import json_util 
from pymongo import MongoClient


api = Flask(__name__)
api.secret_key = 'secret'
api.config["JWT_SECRET_KEY"] = "softwareEngineering"
api.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(api)
mongo = None

def setup_mongo_client(app):
    global mongo
    if app.config['TESTING']:
        # Use mongomock for testing
        app.mongo_client = mongomock.MongoClient()
        mongo = app.mongo_client["test"]
    else:
        # Use a real MongoDB connection for production
        app.mongo_client = MongoClient('localhost', 27017)
        mongo = app.mongo_client["test"]

# Call setup_mongo_client during normal (non-test) app initialization
setup_mongo_client(api)

@api.route('/token', methods=["POST"])
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = mongo.user.find_one({"email": email})
    if (user is not None and (user["password"] == password)):
        access_token = create_access_token(identity=email)
        return jsonify({"message": "Login successful", "access_token":access_token})
    else:
        print("Invalid email or password")
        return jsonify({"message": "Invalid email or password"}),401

@api.route("/register", methods=['POST'])
def register():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    first_name = request.json.get('firstName', None)
    last_name = request.json.get('lastName', None)
    new_document = {
    "email": email,
    "password": password,
    "first_name": first_name,
    "last_name": last_name,
    }
    query = {
        "email": email,
    }
    try:
        inserted = mongo.user.update_one(query, {"$set": new_document}, upsert=True)
        if (inserted.upserted_id):
            response = jsonify({"msg": "register successful"})
        else:   
            print("User already exists")
            response = jsonify({"msg": "User already exists"})
    except Exception as e:
        response = jsonify({"msg": "register failed"})

    return response

@api.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response

@api.route('/events', methods=['GET'])
def get_events():
    events_collection = mongo.events
    events = list(events_collection.find({}))
    print(events)
    for event in events:
        event["_id"] = str(event["_id"]) # Convert ObjectId to string
    return jsonify(events)

@api.route('/is-enrolled', methods=['POST'])
@jwt_required()
def is_enrolled():
    data = request.json
    eventTitle = data['eventTitle']
    current_user = get_jwt_identity()
    enrollment = mongo.db.user.find_one({"email": current_user, "eventTitle": eventTitle})

    if enrollment:
        return jsonify({"isEnrolled": True})
    else:
        return jsonify({"isEnrolled": False})


@api.route('/enroll', methods=['POST'])
@jwt_required()
def enroll_event():
    data = request.get_json()  # get data from POST request
    current_user = get_jwt_identity()
    try:
        # Insert data into MongoDB
        mongo.db.user.insert_one({
            "email": current_user,
            "eventTitle": data['eventTitle']
        })
        response = {"status": "Data saved successfully"}
    except Exception as e:
        response = {"status": "Error", "message": str(e)}
    
    return jsonify(response)

@api.route('/profile')
@jwt_required()
def my_profile():
    current_user = get_jwt_identity()
    profile = mongo.db.user.find_one({"email": current_user})
    return jsonify(json_util.dumps(profile))

@api.route('/caloriesConsumed',methods=["POST"])
@jwt_required()
def addUserConsumedCalories():
    data = request.get_json()  # get data from POST request
    current_user = get_jwt_identity()
    try:
        # Insert data into MongoDB
        mongo.db.user.update_one({'email': current_user, "consumedDate": data['intakeDate']}, {"$push": {"foodConsumed": {"item":data["intakeFoodItem"],"calories":data["intakeCalories"]}}}, upsert=True)
        response = {"status": "Data saved successfully"}
        statusCode = 200
    except Exception as e:
        response = {"status": "Error", "message": str(e)}
        statusCode = 500
    return jsonify(response),statusCode

@api.route('/profileUpdate',methods=["POST"])
@jwt_required()
def profileUpdate():
    current_user = get_jwt_identity()
    first_name = request.json.get('firstName', None)
    last_name = request.json.get('lastName', None)
    age = request.json.get('age', None)
    weight = request.json.get('weight', None)
    height = request.json.get('height', None)
    new_document = {
    "first_name": first_name,
    "last_name": last_name,
    "age": age,
    "weight": weight,
    "height": height,
    }
    query = {
        "email": current_user,
    }
    try:
        mongo.db.user.update_one(query, {"$set": new_document}, upsert=True)
        response = jsonify({"msg": "update successful"})
    except Exception as e:
        response = jsonify({"msg": "update failed"})

    return response

@api.route('/goalsUpdate',methods=["POST"])
@jwt_required()
def goalsUpdate():
    current_user = get_jwt_identity()
    current_user = get_jwt_identity()
    targetWeight = request.json.get('targetWeight', None)
    targetCalories = request.json.get('targetCalories', None)
    targetGoal = request.json.get('targetGoal', None)

    new_document = {
        "target_weight": targetWeight,
        "target_calories": targetCalories,
        "target_goal": targetGoal
    }
    query = {
        "email": current_user,
    }
    try:
        mongo.db.user.update_one(query, {"$set": new_document}, upsert=True)
        response = jsonify({"msg": "update successful"})
    except Exception as e:
        response = jsonify({"msg": "update failed"})

    return response


@api.route('/caloriesBurned',methods=["POST"])
@jwt_required()
def addUserBurnedCalories():
    data = request.get_json()  # get data from POST request
    current_user = get_jwt_identity()
    try:
        # Insert data into MongoDB
        mongo.db.user.update_one({'email': current_user, "consumedDate": data['burnoutDate']}, {"$inc": {"burntCalories": int(data["burntoutCalories"])}}, upsert=True)
        response = {"status": "Data saved successfully"}
        statusCode = 200
    except Exception as e:
        response = {"status": "Error", "message": str(e)}
        statusCode = 500
    return jsonify(response),statusCode

@api.route('/weekHistory',methods=["POST"])
@jwt_required()
def getWeekHistory():
    data = request.get_json()  # get data from POST request
    current_user = get_jwt_identity()
    todayDate = datetime.strptime(data["todayDate"],"%m/%d/%Y")
    dates = [(todayDate-timedelta(days=x)).strftime("%m/%d/%Y") for x in range(7)]
    calorieLimit = 1000
    result = []
    try:
        for index,dateToFind in enumerate(dates):
            # Every day's res item should like this
            # {
            #   dayIndex: 0,               #Interger from 0-6
            #   date: "10/13/2023",        #Date 0=today, 6=7th day ago from today
            #   foodConsumed: [            # A list of dicts, each dict contains a food item and its calories
            #     {
            #       item: "Chicken Salad",
            #       calories: 500,
            #     },
            #     {
            #       item: "Onion Soup",
            #       calories: 300,
            #     },
            #     {
            #       item: "Potato Salad",
            #       calories: 500,
            #     },
            #     {
            #       item: "Cheese Burger",
            #       calories: 500,
            #     },
            #   ],
            #   caloriesConsumed: 1800,    # the sum of all calories consumed from above list
            #   exceededDailyLimit: false, # true or false based on whether caloriesConsumed is > limit user set
            #   burntCalories: 1200,       # calories burnt out on that day
            # }
            res = {}
            data = mongo.db.user.find_one({'email': current_user, "consumedDate": dateToFind})
            res["dayIndex"] = index
            res["date"] = dateToFind
            if data:
                if "foodConsumed" in data:
                    res["foodConsumed"] = data["foodConsumed"]
                    res["caloriesConsumed"] = reduce(lambda a,b: a+b, [int(item["calories"]) for item in data["foodConsumed"]])
                    res["exceededDailyLimit"] = res["caloriesConsumed"]>calorieLimit
                if "burntCalories" in data:
                    res["burntCalories"] = data["burntCalories"]
            if "foodConsumed" not in res:
                res["foodConsumed"] = []
            if "caloriesConsumed" not in res:
                res["caloriesConsumed"] = 0
            if "burntCalories" not in res:
                res["burntCalories"] = 0
            if "exceededDailyLimit" not in res:
                res["exceededDailyLimit"] = False
            result.append(res)
        response = result
        statusCode = 200
    except Exception as e:
        response = {"status": "Error", "message": str(e)}
        statusCode = 500
    return jsonify(response),statusCode

@api.route('/foodCalorieMapping',methods=["GET"])
@jwt_required()
def getFoodCalorieMapping():
    try:
        data = mongo.db.food.find()
        # Response should be in this format {foodItem: calories, foodItem: calories....} 
        # For Example { Potato: 50, Acai: 20, Cheeseburger: 80 }
        response = {item["food"]:item["calories"] for item in data}
        statusCode = 200
    except Exception as e:
        response = {"status": "Error", "message": str(e)}
        statusCode = 500
    return jsonify(response),statusCode

@api.route('/usersEvents',methods=["GET"])
@jwt_required()
def getUserRegisteredEvents():
    try:
        # current_user = get_jwt_identity()
        current_user = get_jwt_identity()
        data = mongo.db.user.find({"email": current_user, "eventTitle":{"$exists": True}})
        response = []
        date="10/23/2023"
        for item in data:
            res = {"eventName": item["eventTitle"], "date": date}
            response.append(res)
        # Response should be in this format [{eventName: Yoga, date: "12/11/2023"},{eventName: Swimming, date: "11/10/2023"}]
        # For Example { Potato: 50, Acai: 20, Cheeseburger: 80 }
        statusCode = 200
    except Exception as e:
        response = {"status": "Error", "message": str(e)}
        statusCode = 500
    return jsonify(response),statusCode
