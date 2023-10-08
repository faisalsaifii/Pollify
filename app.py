from flask import request, Flask
from slack_sdk import WebClient
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
import os

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
                    "block_id": "channel-id-input",
                    "element": {
                        "type": "multi_channels_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select channels",
                        },
                        "action_id": "multi_static_select-action",
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
    channel = values[""]
    choices = str(values["choices"]["choices-action"]["value"]).split("\n")
    blocks = [
        {
            "type": "section",
            "block_id": "poll",
            "text": {"type": "mrkdwn", "text": question},
            "accessory": {
                "type": type,
                "options": [],
                "action_id": "choice-action",
            },
        }
    ]
    for i, choice in enumerate(choices):
        blocks[0]["accessory"]["options"].append(
            {
                "text": {
                    "type": "plain_text",
                    "text": choice,
                    "emoji": True,
                },
                "value": f"value-{i}",
            }
        )
    say(
        text="Poll",
        blocks=blocks,
        channel=channel,
    )


@slack_app.action("choice-action")
def choiceHandler(ack, body):
    ack()
    blocks = body["message"]["blocks"]
    action = body["state"]["values"]["poll"]["choice-action"]
    type = action["type"]
    blocks.append(
        {
            "type": "section",
            "block_id": "response",
            "text": {
                "type": "mrkdwn",
                "text": f"<@{body['user']['id']}> chose ",
            },
        }
    )
    if type == "checkboxes":
        selected_options = action["selected_options"]
        for option in selected_options:
            blocks[-1]["text"]["text"] += str(option["text"]["text"])
    elif type == "radio":
        blocks[-1]["text"]["text"] += str(option["text"]["text"])
    slack_web_client.chat_update(
        channel=body["channel"]["id"], ts=body["message"]["ts"], blocks=blocks
    )


@app.route("/", methods=["GET"])
def index():
    return "Poll Star"


@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
