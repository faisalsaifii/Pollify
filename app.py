from flask import render_template, request, Flask
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from slack_bolt.oauth.oauth_settings import OAuthSettings
from slack_bolt.oauth.oauth_flow import OAuthFlow
from mongodb_installation_store import MongoDBInstallationStore
from pymongo import MongoClient
import os
import uuid
import re
from dotenv import load_dotenv
from blocks import poll_input_block

load_dotenv()
app = Flask(__name__)
mongo_uri = os.environ.get("MONGO_URI")
mongo_client = MongoClient(mongo_uri)
db = mongo_client["slack"]
collection = db["installations"]
client_id = os.environ["SLACK_CLIENT_ID"]
client_secret = os.environ["SLACK_CLIENT_SECRET"]

oauth_settings = OAuthSettings(
    client_id=client_id,
    client_secret=client_secret,
    scopes=["commands", "chat:write"],
    user_scopes=[],
    installation_store=MongoDBInstallationStore(
        client=mongo_client, database="slack", client_id=client_id
    ),
)

oauth_flow = OAuthFlow(settings=oauth_settings)

slack_app = App(
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"), oauth_flow=oauth_flow
)
handler = SlackRequestHandler(slack_app)


@slack_app.command("/poll")
def repeat_text(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "poll",
            "title": {"type": "plain_text", "text": "Create a Poll"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": poll_input_block,
        },
    )


@slack_app.view("poll")
def handle_submission(ack, body, say):
    ack()
    values = body["view"]["state"]["values"]
    type = values["type"]["multi_static_select-action"]["selected_option"]["value"]
    question = values["question"]["question-action"]["value"]
    channels = values["channels"]["channels-action"]["selected_channels"]
    choices = str(values["choices"]["choices-action"]["value"]).strip().split("\n")
    id = uuid.uuid4()
    blocks = [
        {
            "type": "section",
            "block_id": f"poll-{id}",
            "text": {"type": "mrkdwn", "text": f"*{question}*"},
            "accessory": {
                "type": type,
                "options": [],
                "action_id": f"choice-action-{id}",
            },
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "*Votes*"},
        },
    ]
    for i, choice in enumerate(choices):
        blocks[0]["accessory"]["options"].append(
            {
                "text": {
                    "type": "plain_text",
                    "text": choice,
                    "emoji": True,
                },
                "value": str(i + 1),
            }
        )
        blocks.append(
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*{i+1}. {choice}*: "},
            }
        )
    for channel in channels:
        say(
            text="Poll",
            blocks=blocks,
            channel=channel,
        )


@slack_app.action(re.compile("(.*?)"))
def choiceHandler(ack, body, action, client):
    ack()
    id = ("").join(action["block_id"].split("-")[1:])
    block_id = action["block_id"]
    blocks = body["message"]["blocks"]
    type = action["type"]
    if type == "checkboxes":
        selected_options = action["selected_options"]
        for block in blocks:
            if f"{body['user']['id']}" in block["text"]["text"]:
                block["text"]["text"] = block["text"]["text"].replace(
                    f"<@{body['user']['id']}> ", ""
                )
        for option in selected_options:
            selected_value = option["value"]
            for block in blocks:
                value = block["text"]["text"][1]
                if value == selected_value:
                    block["text"]["text"] += f"<@{body['user']['id']}> "
            client.chat_update(
                channel=body["channel"]["id"],
                ts=body["message"]["ts"],
                blocks=blocks,
                text=body["message"]["text"],
            )
    if type == "radio_buttons":
        selected_value = action["selected_option"]["value"]
        for block in blocks:
            if f"{body['user']['id']}" in block["text"]["text"]:
                block["text"]["text"] = block["text"]["text"].replace(
                    f"<@{body['user']['id']}> ", ""
                )
        for block in blocks:
            value = block["text"]["text"][1]
            if value == selected_value:
                block["text"]["text"] += f"<@{body['user']['id']}> "
        client.chat_update(
            channel=body["channel"]["id"],
            ts=body["message"]["ts"],
            blocks=blocks,
            text=body["message"]["text"],
        )


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/tos", methods=["GET"])
def tos():
    return render_template("tos.html")


@app.route("/privacy", methods=["GET"])
def privacy():
    return render_template("privacy.html")


@app.route("/support", methods=["GET"])
def support():
    return render_template("support.html")


@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)


@app.route("/slack/install", methods=["GET"])
def install():
    return handler.handle(request)


@app.route("/slack/oauth_redirect", methods=["GET"])
def oauth_redirect():
    return handler.handle(request)
