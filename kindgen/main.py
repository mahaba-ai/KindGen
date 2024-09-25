"""
Main Application Script to run for a given Workflow
"""

from kindgen.stages import (
    run_stage_1,
    run_stage_2,
    run_stage_3,
    run_stage_4,
    run_stage_5,
    run_stage_6,
)

stage_function_map = {
    1: run_stage_1,
    2: run_stage_2,
    3: run_stage_3,
    4: run_stage_4,
    5: run_stage_5,
    6: run_stage_6,
}


def respond(message, chat_history, conversation_stage: tuple[int, int]):
    """
    Process must yield results where required after / in each substage.
    """
    stage, substage = conversation_stage

    for response in stage_function_map[stage](message, chat_history, substage):
        yield response


if __name__ == "__main__":
    for item in respond("a child is beign a pain", None, (1, 1)):
        print(item)
