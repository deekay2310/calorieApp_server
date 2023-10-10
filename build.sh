brew install python3
pip3 install -r requirements.txt
brew install docker
docker run -dp 27017:27017 mongo
python3 application.py
