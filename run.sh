pip3 install -r requirements.txt
export SLACK_SIGNING_SECRET=a03a70d6a199de0eacba673064fe2947
export SLACK_BOT_TOKEN=xoxb-5649828779333-5718433923317-LYzQxfLcqAER14yqDwUwzaWE
FLASK_APP=app.py
python3 -m flask --debug run -p 5000