from typing import Union
from kindgen.models import ChatHistory, Stage


def reset_conversation() -> Union[ChatHistory, Stage]:
    conversation = [
        {"role": "assistant", "text": "Let me help you!"},
        {"role": "assistant", "text": "Can you tell me a bit about your situation?"},
    ]

    stage = Stage(stage=1, substage=1)

    return conversation, stage
