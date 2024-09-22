import streamlit as st

from kindgen.gpt import stream
from interface.assets import LOGO_PATH, ASSISTANT_AVATAR_PATH, USER_AVATAR_PATH

AVATAR_MAPPING = {"assistant": ASSISTANT_AVATAR_PATH, "user": USER_AVATAR_PATH}

st.set_page_config(
    page_title="KindGen Demo",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="expanded",
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
        {"role": "assistant", "text": "Hey!"},
    ]


if "conversation" not in st.session_state:
    reset_conversation()

CONVERSATION = st.session_state.conversation

if clear_conversation:
    reset_conversation()

# Write Conversation History
for conversation_item in CONVERSATION:
    st.chat_message(
        conversation_item["role"], avatar=AVATAR_MAPPING[conversation_item["role"]]
    ).write(conversation_item["text"])

if user_input := st.chat_input():
    st.chat_message("user", avatar=AVATAR_MAPPING["user"]).write(user_input)

    assistant_message = st.chat_message("assistant", avatar=AVATAR_MAPPING["assistant"])

    assistant_response = assistant_message.write_stream(
        stream(message=user_input, chat_history=CONVERSATION)
    )

    CONVERSATION.append({"role": "user", "text": user_input})
    CONVERSATION.append({"role": "assistant", "text": assistant_response})
