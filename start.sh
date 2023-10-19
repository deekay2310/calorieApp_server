#!/bin/bash

# Wait for MongoDB to be available
dockerize -wait tcp://mongo:27017 -timeout 120s

# Insert data
python insert_data.py

# Start Flask application
exec python application.py