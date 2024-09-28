"""
Main Application Script to run for a given Workflow
"""

from kindgen.models import ChatHistory, Stage


def respond(
    message: str, chat_history: ChatHistory, conversation_stage: Stage, **kwargs
):
    """
    Process must yield results where required after / in each substage.
    """

    for response in conversation_stage.run(message=message, chat_history=chat_history):
        yield response
