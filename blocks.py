poll_input_block = [
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
]