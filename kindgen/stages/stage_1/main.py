from typing import Generator

from kindgen.gpt import stream, fake_stream
from kindgen.stages.stage_1.prompts import substage_1_prompt, substage_1_prompt_eval


def run_stage_1_substage_1(message: str, **kwargs) -> Generator[str, None, None]:
    prompt = substage_1_prompt.replace("<user-situation>", message)
    yield from stream(prompt)


def run_stage_1_substage_1_eval(message: str, **kwargs) -> Generator[str, None, None]:
    prompt = substage_1_prompt_eval.replace("<user-situation>", message)
    yield from stream(prompt)


def run_stage_1_substage_3(**kwargs) -> Generator[str, None, None]:
    yield from fake_stream(
        "Got it! If you want to take a couple of minutes to feel better before we go on, just tap the ‘Calm’ button, and we’ll do a short process together. "
    )


def run_stage_1_substage_4(**kwargs) -> Generator[str, None, None]:
    yield from fake_stream(
        "Alright, let's dive deeper into your situation. Firstly, who is it affecting? Select as many of the options below that apply."
    )


def run_stage_1_substage_7(**kwargs) -> Generator[str, None, None]:
    yield from fake_stream("Thanks! Another couple of questions from me:")


def run_stage_1_substage_10(**kwargs) -> Generator[str, None, None]:
    yield from fake_stream(
        "So that you're aware - your school's standard procedure for such a situation is to notify Pastoral Care and the Head of Department, in addition to exploring a solution to the classroom situation for yourself."
    )
    yield from fake_stream(
        "Kind Gen offers a specialised coaching service to parents via the school for such situations.\n\n"
    )
    yield from fake_stream(
        "At this point the AI would offer some resources to download."
    )
