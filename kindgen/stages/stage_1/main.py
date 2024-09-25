from kindgen.gpt import stream, fake_stream
from kindgen.stages.stage_1.prompts import substage_1_prompt


def run_substage_1(message, *args):
    prompt = substage_1_prompt.replace("<user-situation>", message)

    yield from stream(prompt)


def run_substage_3(*args):
    yield from fake_stream(
        "Got it! If you want to take a couple of minutes to feel better before we go on, just tap the ‘Calm’ button, and we’ll do a short process together. "
    )


def run_substage_4(*args):
    yield from fake_stream(
        "Alright, let’s dive deeper into your situation. Firstly, who is it affecting? Select as many of the options below that apply."
    )


def run_substage_7(*args):
    yield from fake_stream("Don't worry! We will get on top of this.")


substage_mapping = {
    1: run_substage_1,
    3: run_substage_3,
    4: run_substage_4,
    7: run_substage_7,
}


def main(message, chat_history, substage):
    yield from substage_mapping[substage](message, chat_history)


if __name__ == "__main__":
    main()
