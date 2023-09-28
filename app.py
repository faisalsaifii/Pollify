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
                                "value": "single_choice",
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Multi Choice",
                                    "emoji": True,
                                },
                                "value": "multichoice",
                            },
                        ],
                        "action_id": "multi_static_select-action",
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Type of Poll",
                        "emoji": True,
                    },
                },
                {
                    "type": "input",
                    "block_id": "question",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Enter the question",
                            "emoji": True,
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
                        "action_id": "plain_text_input-action",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Enter the choices (Each on new line)",
                            "emoji": True,
                        },
                    },
                    "label": {"type": "plain_text", "text": "Choices"},
                },
            ],
        },
    )


@slack_app.view("poll")
def handle_submission(ack, body):
    ack()
    values = body["view"]["state"]["values"]
    type = values["type"]["multi_static_select-action"]["selected_option"]["value"]
    question = values["question"]["plain_text_input-action"]["value"]
    options = str(values["answer"]["plain_text_input-action"]["value"]).split("\n")
    slack_web_client.chat_postMessage(
        text=f"Question: {question}\nAnswer: {options}\nProduct: {type}",
    )


@app.route("/", methods=["GET"])
def index():
    return "Poll Star"


@app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
