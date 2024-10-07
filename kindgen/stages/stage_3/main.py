from typing import Generator

from kindgen.gpt import stream
from kindgen.stages.stage_3.prompts import substage_1, substage_2


def run_stage_3_substage_1(message: str, **kwargs) -> Generator[str, None, None]:
    prompt = substage_1.prompt.replace("<conversation>", message)
    yield from stream(prompt)


def run_stage_3_substage_2(message: str, **kwargs) -> Generator[str, None, None]:
    prompt = substage_2.prompt.replace("<user_response>", message)
    yield from stream(prompt)
