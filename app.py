import json
from flask import request, Flask
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import os
import uuid
import re

app = Flask(__name__)
bot_token = os.environ.get("SLACK_BOT_TOKEN")
slack_app = App(token=bot_token, signing_secret=os.environ.get("SLACK_SIGNING_SECRET"))
slack_web_client = WebClient(token=bot_token)
handler = SlackRequestHandler(slack_app)


@slack_app.command("/poll")
def repeat_text(ack, body):
    ack()
    slack_web_client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "callback_id": "poll",
            "title": {"type": "plain_text", "text": "Create a Poll"},
            "submit": {"type": "plain_text", "text": "Submit"},
            "close": {"type": "plain_text", "text": "Cancel"},
            "blocks": [
                {
                    "type": "input",
                    "block_id": "type",
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a type of poll",
                        },
                        "options": [
                            {
                                "text": {"type": "plain_text", "text": "Single Choice"},
                                "value": "radio_buttons",
                            },
                            {
                                "text": {"type": "plain_text", "text": "Multi Choice"},
                                "value": "checkboxes",
                            },
                        ],
                        "action_id": "multi_static_select-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Type of Poll",
                    },
                },
                {
                    "type": "input",
                    "block_id": "question",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "question-action",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Enter the question",
                        },
                    },
                    "label": {"type": "plain_text", "text": "Question"},
                },
                {
                    "type": "input",
                    "block_id": "choices",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "choices-action",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Enter the choices (Each on new line)",
                        },
                    },
                    "label": {"type": "plain_text", "text": "Choices"},
                },
                {
                    "type": "input",
                    "block_id": "channels",
                    "element": {
                        "type": "multi_channels_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select channels",
                        },
                        "action_id": "channels-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Channels for the Poll",
                    },
                },
            ],
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
def choiceHandler(ack, body, action):
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
            slack_web_client.chat_update(
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
        slack_web_client.chat_update(
            channel=body["channel"]["id"],
            ts=body["message"]["ts"],
            blocks=blocks,
            text=body["message"]["text"],
        )


@app.route("/", methods=["GET"])
def index():
    return "Poll Star"


@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
