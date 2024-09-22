import json

from kindgen.models import ChatHistory


def extract_json(input_string: str) -> dict:
    """String to Json function"""

    input_string = (
        input_string.replace("```json", "```").replace("```", "").replace("\_", "_")
    )

    input_string_stripped = input_string.lstrip("{").rstrip("}")

    try:
        return json.loads(input_string_stripped)

    except json.JSONDecodeError:
        raise


def format_chat_history(chat_history: ChatHistory) -> ChatHistory:
    return [
        {
            "role": "CHATBOT" if entry["role"] == "assistant" else "USER",
            "text": entry["text"],
        }
        for entry in chat_history
        if entry["role"] in ["assistant", "user"]
    ]
