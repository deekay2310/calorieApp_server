# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app

# Install dependencies
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose the port app will run on
EXPOSE 8080

# Copy needed contents to run the Flask app
COPY application.py apps.py forms.py templates static /app

# Set environment variables for MongoDB

# Populate database with food data
COPY food_data/calories.csv /app/food_data/
COPY insert_food_data.py /app
RUN python insert_food_data.py

# Run your Flask application
CMD ["python", "application.py"]










