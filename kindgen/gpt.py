"""
GPT Related Functions
"""

import time
from typing import Generator

from kindgen import cohere_client
from kindgen.models import ChatHistory
from kindgen.utils.format import format_chat_history


def stream(message: str, chat_history: ChatHistory | None = None) -> Generator:
    """Get response from Cohere and stream response"""
    chat_history = format_chat_history(chat_history) if chat_history else []

    stream = cohere_client.chat_stream(message=message, chat_history=chat_history)

    for event in stream:
        if event.event_type == "text-generation":
            yield event.text


def fake_stream(
    message: str, fake_pause: float = 1, fake_word_delay: float = 0.05
) -> Generator[str, None, None]:
    """Yield individual tokens (words) from the message like a chatbot."""
    time.sleep(fake_pause)
    for word in message.split():
        yield f"{word} "
        time.sleep(fake_word_delay)


def chat(message: str, chat_history: ChatHistory = None) -> str:
    """Get response from Cohere, with option to get output in json format"""
    chat_history = format_chat_history(chat_history) if chat_history else []

    response = cohere_client.chat(message=message, chat_history=chat_history)

    return response
