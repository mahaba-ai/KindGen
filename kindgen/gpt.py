"""
    GPT Related Functions
"""

from typing import List, Dict, Generator

import cohere
from kindgen import cohere_client


def test_api_key():
    """Function to test Cohere API Key is working"""
    try:
        cohere_client.generate(prompt="sample prompt", max_tokens=3)

        return True
    except:
        return False


def stream(background_info: str, chat_history: List[Dict[str, str]] = []) -> Generator:
    """Get response from Cohere and stream response"""
    cohere_history = format_chat_history_cohere(chat_history, background_info)

    stream = cohere_client.chat_stream(
        chat_history=cohere_history[:-1], message=cohere_history[-1]["message"]
    )

    for event in stream:
        if event.event_type == "text-generation":
            yield event.text


def gpt_response(prompt: str, api_key: str) -> str:
    """Get response from Cohere, with option to get output in json format"""

    co = cohere.Client(
        api_key=api_key,
    )

    response = co.chat(message=prompt)

    return response.text
