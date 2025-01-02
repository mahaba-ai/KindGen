import streamlit as st
import cohere

from typing import Generator
from assets import LOGO_PATH, ASSISTANT_AVATAR_PATH, USER_AVATAR_PATH
from pydantic import BaseModel
from typing import List
from prompts import MAIN_PROMPT, COMM_STYLE_PROMPT, EXPORT_PROMPT


class ChatEntry(BaseModel):
    role: str
    text: str


class ChatHistory(BaseModel):
    entries: List[ChatEntry]


AVATAR = {"assistant": ASSISTANT_AVATAR_PATH, "user": USER_AVATAR_PATH}

st.set_page_config(
    page_title="KindGen Demo",
    page_icon=LOGO_PATH,
    layout="wide",
)

with st.sidebar:
    API_KEY = st.text_input("Enter API Key")

    verbosity = st.slider(
        "Response Detail Level",
        1,
        10,
        5,
        help="Set how detailed your communication should be. Low for concise, high for detailed.",
    )

    mode = st.selectbox(
        "Communication Mode",
        ["Professional", "Assertive", "Casual", "Empathetic"],
        help="Choose the tone and approach for your communication.",
    )

    sentence_structure = st.radio(
        "Preferred Response Structure",
        ["Direct and Clear", "Open-Ended and Reflective", "Step-by-Step Instructions"],
        help="Choose the structure for sentences in your communication.",
    )

    session_summary_button = st.button(
        "Export Printable Summary", use_container_width=True
    )


if not API_KEY:
    st.warning("Enter API Key.")
else:
    cohere_client = cohere.Client(api_key=API_KEY)

    if "conversation" not in st.session_state:
        st.session_state.conversation = [
            {
                "role": "assistant",
                "text": "What is the challenging situation you are facing in class?",
                "avatar": ASSISTANT_AVATAR_PATH,
            }
        ]

    CONVERSATION: ChatHistory = st.session_state.conversation

    def format_chat_history(chat_history: ChatHistory) -> ChatHistory:
        sys_prompt = [
            {"role": "SYSTEM", "text": MAIN_PROMPT},
            {
                "role": "SYSTEM",
                "text": COMM_STYLE_PROMPT.replace(
                    "<verbosity>",
                    str(verbosity)
                    .replace("comm_mode", mode)
                    .replace("<resonse_struct>", sentence_structure),
                ),
            },
        ]

        return sys_prompt + [
            {
                "role": "CHATBOT" if entry["role"] == "assistant" else "USER",
                "text": entry["text"],
            }
            for entry in chat_history
            if entry["role"] in ["assistant", "user"]
        ]

    def stream(message: str, chat_history: ChatHistory | None = None) -> Generator:
        chat_history = format_chat_history(chat_history) if chat_history else []

        stream = cohere_client.chat_stream(message=message, chat_history=chat_history)

        for event in stream:
            if event.event_type == "text-generation":
                yield event.text

    for message in CONVERSATION:
        st.chat_message(message["role"], avatar=AVATAR[message["role"]]).write(
            message["text"]
        )

    if user_input := st.chat_input():
        st.chat_message("user", avatar=AVATAR["user"]).write(user_input)
        assistant_message = st.chat_message("assistant", avatar=AVATAR["assistant"])
        assistant_response = assistant_message.write_stream(
            stream(user_input, chat_history=CONVERSATION)
        )

        CONVERSATION.append(
            {
                "role": "user",
                "text": user_input,
            }
        )

        CONVERSATION.append(
            {
                "role": "assistant",
                "text": assistant_response,
            }
        )


if session_summary_button:
    generated_text = ""
    for text in stream(message=EXPORT_PROMPT, chat_history=CONVERSATION):
        generated_text += text

    st.download_button(
        label="Click here to download your report",
        data=generated_text,
        file_name="kindgen_report.txt",
    )
