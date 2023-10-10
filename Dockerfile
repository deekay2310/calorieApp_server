# syntax=docker/dockerfile:1
FROM python:3.7
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["python3", "application.py"]
