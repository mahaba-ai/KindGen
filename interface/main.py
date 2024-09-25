import time
import streamlit as st

from kindgen import logger
from kindgen.main import respond
from interface.assets import LOGO_PATH, ASSISTANT_AVATAR_PATH, USER_AVATAR_PATH

AVATAR_MAPPING = {"assistant": ASSISTANT_AVATAR_PATH, "user": USER_AVATAR_PATH}

st.set_page_config(
    page_title="KindGen Demo",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="collapsed",
)

with st.sidebar:
    st.image(LOGO_PATH)
    lcol, rcol = st.columns((0.5, 0.5))
    with lcol:
        about_button = st.button("About", type="primary", use_container_width=True)
    with rcol:
        clear_conversation = st.button("Restart", use_container_width=True)


def reset_conversation():
    st.session_state["conversation"] = [
        {"role": "assistant", "text": "Let me help you!"},
        {"role": "assistant", "text": "Can you tell me a bit about your situation?"},
    ]

    st.session_state["stage"] = [1, 1]


if "conversation" not in st.session_state:
    reset_conversation()


if "state" not in st.session_state:
    st.session_state["state"] = {
        "begin_demo": False,
        "stage": [1, 1],
        "NEED_REBOOT": False,
    }

CONVERSATION = st.session_state.conversation
STATE = st.session_state.state

RESPONSE_TYPES = {
    (1, 1): "STREAM",
    (1, 2): "emotions",
    (1, 3): "FR",
    (1, 4): "FR",
    (1, 5): "people_affected",
    (1, 6): "what_have_you_tried",
    (1, 7): "FR",
    (1, 8): None,
}

if clear_conversation:
    reset_conversation()

for conversation_item in CONVERSATION:
    st.chat_message(
        conversation_item["role"], avatar=AVATAR_MAPPING[conversation_item["role"]]
    ).write(conversation_item["text"])


@st.dialog("How do you Feel?")
def pick_emotions():
    STATE["user_feelings"] = st.multiselect(
        "Pick Emotions",
        ["Calm", "Ok", " Anxious", "Sad", "Annoyed", "Angry", "Furious"],
    )

    submit = st.button("Finalize")
    if submit:
        st.info(
            "At this point, the user would be guided to deal with their emotions on screen."
        )
        time.sleep(1)
        STATE["stage"][1] += 1
        STATE["NEED_REBOOT"] = True
        st.rerun()


@st.dialog("Who is affected?")
def get_affected_people():
    STATE["affected_people"] = st.multiselect(
        "Pick Affected People",
        [
            "The child himself/herself",
            "Myself as a teacher",
            "Other children in class",
            "The whole class",
            "The child’s parents",
        ],
    )

    submit = st.button("Finalize")
    if submit:
        STATE["stage"][1] += 1
        STATE["NEED_REBOOT"] = True

        st.rerun()


@st.dialog("What have you tried?")
def get_what_have_you_tried():
    STATE["solutions_tried"] = st.multiselect(
        "Pick Affected People",
        [
            "I've tried telling them off in class and taking the paper airplanes away",
            "I’ve tried talking to them privately, telling them to behave",
            "I’ve threatened them with detention",
            "I wrote to their parents",
            "Other (please write)",
        ],
    )

    STATE["still_exists_flag"] = st.multiselect(
        "Does the problem still exist?",
        ["Yes", "No"],
    )

    submit = st.button("Finalize")
    if submit:
        STATE["stage"][1] += 1
        STATE["NEED_REBOOT"] = True
        st.rerun()


def response_handler(user_input=None):
    CURRENT_STAGE = STATE["stage"]
    response_type = RESPONSE_TYPES[tuple(CURRENT_STAGE)]
    logger.info(f"Working on stage {CURRENT_STAGE}, which has type {response_type}")

    if response_type == "STREAM":
        st.chat_message("user", avatar=AVATAR_MAPPING["user"]).write(user_input)

        assistant_message = st.chat_message(
            "assistant", avatar=AVATAR_MAPPING["assistant"]
        )

        assistant_response = assistant_message.write_stream(
            respond(
                message=user_input,
                chat_history=CONVERSATION,
                conversation_stage=CURRENT_STAGE,
            )
        )
        time.sleep(2)

        CONVERSATION.append({"role": "user", "text": user_input})
        CONVERSATION.append({"role": "assistant", "text": assistant_response})
        STATE["stage"][1] += 1
        response_handler()
    elif response_type == "emotions":
        pick_emotions()
    elif response_type == "people_affected":
        get_affected_people()
    elif response_type == "what_have_you_tried":
        get_what_have_you_tried()

    elif response_type == "FR":
        assistant_message = st.chat_message(
            "assistant", avatar=AVATAR_MAPPING["assistant"]
        )

        assistant_response = assistant_message.write_stream(
            respond(None, None, CURRENT_STAGE)
        )
        time.sleep(2)

        CONVERSATION.append({"role": "assistant", "text": assistant_response})
        STATE["stage"][1] += 1
        response_handler()
    else:
        logger.info("No Action")

        STATE["stage"][1] += 1
        st.balloons()
        return


if STATE["NEED_REBOOT"]:
    STATE["NEED_REBOOT"] = False
    time.sleep(0.5)

    response_handler()

if user_input := st.chat_input():
    response_handler(user_input)
