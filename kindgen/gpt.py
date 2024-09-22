"""
GPT Related Functions
"""

from typing import Generator

from kindgen import cohere_client
from kindgen.models import ChatHistory
from kindgen.utils.format import format_chat_history


def stream(message: str, chat_history: ChatHistory = None) -> Generator:
    """Get response from Cohere and stream response"""
    if chat_history:
        chat_history = format_chat_history(chat_history)

    stream = cohere_client.chat_stream(message=message, chat_history=chat_history)

    for event in stream:
        if event.event_type == "text-generation":
            yield event.text


def chat(message: str, chat_history: ChatHistory = None) -> str:
    """Get response from Cohere, with option to get output in json format"""
    if chat_history:
        chat_history = format_chat_history(chat_history)

    response = cohere_client.chat(message=message, chat_history=chat_history)

    return response
