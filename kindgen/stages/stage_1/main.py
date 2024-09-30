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
        "Alright, let’s dive deeper into your situation. Firstly, who is it affecting? Select as many of the options below that apply."
    )


def run_stage_1_substage_6(**kwargs) -> Generator[str, None, None]:
    yield from fake_stream("Thanks! Another couple of questions from me:")


def run_stage_1_substage_8(**kwargs) -> Generator[str, None, None]:
    yield from fake_stream("Don't worry! We will get on top of this.")
