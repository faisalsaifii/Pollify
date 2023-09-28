from flask import request
from flask import Flask
from flask_cors import CORS
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import json
import os

app = Flask(__name__)
bot_token = os.environ.get("SLACK_BOT_TOKEN")
user_token = os.environ.get("SLACK_USER_TOKEN")
slack_app = App(token=bot_token, signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))
slack_web_client = WebClient(token=bot_token)
slack_user_client = WebClient(token=user_token)
handler = SlackRequestHandler(slack_app)


@app.route("/", methods=["GET"])
def index():
    return "Poll Star"


@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
