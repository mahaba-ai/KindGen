from typing import Union
from kindgen.models import ChatHistory


def reset_conversation() -> Union[ChatHistory]:
    conversation = [
        {"role": "assistant", "text": "Let me help you!"},
        {"role": "assistant", "text": "Can you tell me a bit about your situation?"},
    ]

    return conversation
