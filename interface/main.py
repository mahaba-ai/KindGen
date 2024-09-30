import time
import streamlit as st

from kindgen import logger
from kindgen.models import ChatHistory, Stage
from kindgen.gpt import fake_stream
from kindgen.main import respond
from interface.assets import LOGO_PATH, ASSISTANT_AVATAR_PATH, USER_AVATAR_PATH
from interface.methods import reset_conversation

st.set_page_config(
    page_title="KindGen Demo",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "state" not in st.session_state:
    st.session_state["state"] = {
        "begin_demo": False,
        "stage": Stage(stage=1, substage=1, val=0),
        "NEED_REBOOT": False,
    }

STATE: dict = st.session_state.state

if "PLACEHOLDER_STATE" not in st.session_state:
    st.session_state["PLACEHOLDER_STATE"] = {"show": False, "emotions": False}

PLACEHOLDER_STATE = st.session_state.PLACEHOLDER_STATE

if "conversation" not in st.session_state:
    st.session_state.conversation, STATE["stage"] = reset_conversation()

CONVERSATION: ChatHistory = st.session_state.conversation


def TEXT_RESPONSE(user_input: str, CURRENT_STAGE: Stage, **kwargs):
    if user_input:
        st.chat_message("user", avatar=AVATAR["user"]).write(user_input)

    print("assistant message = ")
    assistant_message = st.chat_message("assistant", avatar=AVATAR["assistant"])

    if CURRENT_STAGE.stage == 1 and CURRENT_STAGE.substage == 1:
        STATE["stage"].update_val(True)
        state_passed = False

        while not state_passed:
            response_gen = respond(
                message=user_input,
                chat_history=CONVERSATION,
                conversation_stage=CURRENT_STAGE,
            )
            response = "".join(response_gen)
            print(f"assistant response = {response}")

            if "yes" in response.lower():
                state_passed = True
            else:
                assistant_response = assistant_message.write_stream(
                    fake_stream("I'm not sure I understand. Could you try again?")
                )
                CONVERSATION.append({"role": "assistant", "text": assistant_response})
                STATE["stage"].update_val(False)
                user_input = None
                while not user_input:
                    user_input = st.session_state.get("user_input", None)

    STATE["stage"].update_val(False)
    assistant_response = assistant_message.write_stream(
        respond(
            message=user_input,
            chat_history=CONVERSATION,
            conversation_stage=CURRENT_STAGE,
        )
    )

    time.sleep(2)
    if user_input:
        CONVERSATION.append({"role": "user", "text": user_input})

    print(CONVERSATION)
    CONVERSATION.append({"role": "assistant", "text": assistant_response})
    STATE["stage"].next_substage()
    response_handler()


def END(**kwargs):
    logger.info("No Action Taken.")

    st.balloons()


def pick_emotions(*args, **kwargs):
    PLACEHOLDER_STATE["show"] = True
    PLACEHOLDER_STATE["stage"] = "emotions"
    st.rerun()


def get_affected_people(*args, **kwargs):
    PLACEHOLDER_STATE["show"] = True
    PLACEHOLDER_STATE["stage"] = "affected_people"
    st.rerun()


def get_what_have_you_tried(*args, **kwargs):
    PLACEHOLDER_STATE["show"] = True
    PLACEHOLDER_STATE["stage"] = "tried"
    st.rerun()


RESPONSE_TYPES = {
    (1, 1): TEXT_RESPONSE,
    (1, 2): pick_emotions,
    (1, 3): TEXT_RESPONSE,
    (1, 4): TEXT_RESPONSE,
    (1, 5): get_affected_people,
    (1, 6): TEXT_RESPONSE,
    (1, 7): get_what_have_you_tried,
    (1, 8): TEXT_RESPONSE,
    (1, 9): END,
}

AVATAR = {"assistant": ASSISTANT_AVATAR_PATH, "user": USER_AVATAR_PATH}


with st.sidebar:
    st.image(LOGO_PATH)
    lcol, rcol = st.columns((0.5, 0.5))
    with lcol:
        about_button = st.button("About", type="primary", use_container_width=True)
    with rcol:
        clear_conversation = st.button("Restart", use_container_width=True)

        if clear_conversation:
            reset_conversation()


def response_handler(user_input: str | None = None):
    CURRENT_STAGE = STATE["stage"]
    response_method = RESPONSE_TYPES[CURRENT_STAGE.to_tuple()]
    logger.info(f"Working on stage {CURRENT_STAGE}")

    response_method(user_input=user_input, CURRENT_STAGE=CURRENT_STAGE, STATE=STATE)


for message in CONVERSATION:
    st.chat_message(message["role"], avatar=AVATAR[message["role"]]).write(
        message["text"]
    )


if STATE["NEED_REBOOT"]:
    STATE["NEED_REBOOT"] = False
    time.sleep(0.5)

    response_handler()

if PLACEHOLDER_STATE["show"]:
    SELECTIONS = "No selection made."
    placeholder_stage = PLACEHOLDER_STATE["stage"]
    with st.chat_message("assistant", avatar=AVATAR["assistant"]):
        if placeholder_stage == "emotions":
            STATE["emotions"] = st.multiselect(
                "Please tell me the emotions you are feeling",
                ["Calm", "Ok", " Anxious", "Sad", "Annoyed", "Angry", "Furious"],
            )
            SELECTIONS = (
                f"[*selection input*] Emotions: {', '.join(STATE['emotions'])}."
            )

        elif placeholder_stage == "tried":
            STATE["solutions_tried"] = st.multiselect(
                "What have you tried?",
                [
                    "Telling them off in class",
                    "Talking to them privately",
                    "I've threatened them with detention",
                    "I wrote to their parents",
                    "Other (please write)",  # NOTE: How will we implement 'other' ?
                ],
            )

            STATE["still_exists_flag"] = st.multiselect(
                "Does the problem still exist?",
                ["Yes", "No"],
            )
            SELECTIONS = f"[*selection input*] Still a current problem? {STATE['still_exists_flag']}. Solutions tried: {', '.join(STATE['solutions_tried'])}."

        elif placeholder_stage == "affected_people":
            STATE["affected_people"] = st.multiselect(
                "Please can you pick the people affected?",
                [
                    "The child himself/herself",
                    "Myself as a teacher",
                    "Other children in class",
                    "The whole class",
                    "The child’s parents",
                ],
            )

            SELECTIONS = f"[*selection input*] People Affected: {', '.join(STATE['affected_people'])}."

        submit = st.button("Finalize input")
        if submit:
            PLACEHOLDER_STATE["show"] = False
            STATE["stage"].next_substage()
            STATE["NEED_REBOOT"] = True
            CONVERSATION.append({"role": "user", "text": SELECTIONS})
            st.rerun()


def main():
    if user_input := st.chat_input():
        response_handler(user_input)


if __name__ == "__main__":
    main()
