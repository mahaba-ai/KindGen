"""
    GPT Related Functions
"""

from typing import Generator

from kindgen import cohere_client


def stream(message: str) -> Generator:
    """Get response from Cohere and stream response"""
    stream = cohere_client.chat_stream(message=message)

    for event in stream:
        if event.event_type == "text-generation":
            yield event.text


def chat(message: str) -> str:
    """Get response from Cohere, with option to get output in json format"""

    response = cohere_client.chat(message=message)

    return response
