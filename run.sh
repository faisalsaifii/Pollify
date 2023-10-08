pip3 install -r requirements.txt
export SLACK_SIGNING_SECRET="357b9d3cc30f15a2639afa7416cbbec6"
export SLACK_BOT_TOKEN="xoxb-5846374025732-5984562103538-YGvgQP3wYUxY0LejFJMeozVO"
FLASK_APP=app.py
python3 -m flask --debug run -p 5000