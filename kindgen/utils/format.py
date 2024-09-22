import json


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
