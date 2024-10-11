import time
import string
import streamlit as st

from kindgen.models import ChatHistory, Stage
from kindgen.principles import PRINCIPLES
from kindgen import cohere_client

from typing import Generator
from interface.assets import LOGO_PATH, ASSISTANT_AVATAR_PATH, USER_AVATAR_PATH

# TODO add "if you want to take a couple of minutes to feel better before you go on, just tap the calm button below and we'll do a short process together"


def format_chat_history(chat_history: ChatHistory) -> ChatHistory:
    return [
        {
            "role": "CHATBOT" if entry["role"] == "assistant" else "USER",
            "text": entry["text"],
        }
        for entry in chat_history
        if entry["role"] in ["assistant", "user"]
    ]


st.set_page_config(
    page_title="KindGen Demo",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="collapsed",
)

n_stages = 7

if "state" not in st.session_state:
    st.session_state["state"] = {
        "begin_demo": False,
        "stage": 0,
        "NEED_REBOOT": False,
    }


def stream(message: str, chat_history: ChatHistory | None = None) -> Generator:
    chat_history = format_chat_history(chat_history) if chat_history else []

    stream = cohere_client.chat_stream(message=message, chat_history=chat_history)

    for event in stream:
        if event.event_type == "text-generation":
            yield event.text


def fake_stream(
    message: str, fake_pause: float = 1, fake_word_delay: float = 0.05
) -> Generator[str, None, None]:
    """Yield individual tokens (words) from the message like a chatbot."""
    time.sleep(fake_pause)
    for word in message.split():
        yield f"{word} "
        time.sleep(fake_word_delay)


if "messages" not in st.session_state:
    st.session_state["messages"] = []

if not st.session_state["messages"]:
    initial_assistant_message = "Let me help you. Please tell me about your situation."
    st.session_state["messages"].append(
        {"role": "assistant", "text": initial_assistant_message}
    )

for m in st.session_state["messages"]:
    if m["role"] == "user":
        st.chat_message("user").write(m["text"])
    if m["role"] == "assistant":
        st.chat_message("assistant").write(m["text"])

conversation_stage = st.session_state["state"]["stage"]


def evaluate_response(context, model_question, user_response, stage):
    evaluation_prompt = f"""
    <context> {context} 
    <model output> {model_question} 
    <user response> {user_response} 

    Does this make sense as a response to the model output, and is it relevant for the context? You MUST repond with one word: 'yes' or 'no'.

    Do not be overly strict - only reply 'no' if the response absolutely makes no sense or isn't relevant, otherwise reply 'yes'.
    """
    if stage == 0:
        evaluation_prompt += "This can be any situation related to dealing with children, other teachers, school work, the education system in general. It can be as a simple as 'there is a child behaving badly', or highly specific."
    evaluation_result = stream(evaluation_prompt, chat_history)
    result_string = "".join([chunk for chunk in evaluation_result])
    return result_string.strip()


def respond(message, chat_history):
    yield from stream(message, chat_history)


user_input = st.chat_input("")

if user_input:
    conversation_stage = st.session_state["state"]["stage"]
    chat_history = st.session_state["messages"]

    st.session_state["messages"].append({"role": "user", "text": user_input})
    st.chat_message("user").write(user_input)

    def build_stage_prompt(stage):
        if stage == 0:
            print("running stage 0")
            return """
            You are an expert in empathy and communication, acting as a coach for teachers navigating challenging situations.
            When you respond, do so promptly and clearly. 

            Respond with this, or similar:

            "Let me help you. Please tell me about your situation."
            """
        elif stage == 1:
            print("running stage 1")
            return """
            You are an expert in empathy and communication, acting as a coach for teachers navigating challenging situations.
            When you respond, do so promptly and clearly. 

            Now that the user has described their situation, ask about the emotions they're feeling about it.

            For example:

            "Could you tell me how you feel about this? Which emotion(s) resonate the most: Relatively calm, okay, anxious, sad, annoyed, frustrated, angry, furious?"
            
            However, do not simply just list options. This is a conversation.
            """
        elif stage == 2:
            print("running stage 2")
            return """
            You are an expert in empathy and communication, acting as a coach for teachers navigating challenging situations.
            When you respond, do so promptly and clearly. 

            Now ask the user who this situation is affecting - tailor your question to the specific situation following your chat history.

            For example:

            "All right, let's dive deeper into this situation. Firstly, who is it affecting - is it just the child themself and yourself as a teacher? Or is it also affecting other children in the class, maybe even the whole class? Does it affect the children's parents?"
            
            However, do not simply just list options. This is a conversation.
            """
        elif stage == 3:
            print("running stage 3")
            return """
            You are an expert in empathy and communication, acting as a coach for teachers navigating challenging situations.
            When you respond, do so promptly and clearly. 

            Now ask the user how this situation is affecting them - tailor your question to the specific situation following your chat history e.g. if the user previously said it is affecting them and the whole class, ask how it affects them and how it affects the class.

            For example:

            "Alright, how is it affecting them?"
            """
        elif stage == 4:
            print("running stage 4")
            return """
            You are an expert in empathy and communication, acting as a coach for teachers navigating challenging situations.
            When you respond, do so promptly and clearly. 

            Now ask the user what this solutions they're tried so far - tailor your question to the specific situation following your chat history.

            For example:

            "Thank you. I'm getting the picture. What, if any, solutions to this have you tried so far? "
            """
        elif stage == 5:
            print("running stage 5")
            return """
            You are an expert in empathy and communication, acting as a coach for teachers navigating challenging situations.
            When you respond, do so promptly and clearly. 

            Now ask the user how long this has been going on for - tailor your question to the specific situation following your chat history e.g. if the user is mentioning a specific event, rather than a behaviour, instead ask if this event has occurred before.

            For example:

            "Alright, how long has this been going on?"
            """
        elif stage == 6:
            print("running stage 6")
            return """
            You are an expert in empathy and communication, acting as a coach for teachers navigating challenging situations.
            When you respond, do so promptly and clearly. 

            Now ask the user how about more specific needs the child/children/subject might have - again, tailor your question to the specific situation following your chat history and remember what the user has said so far, e.g. if the child is lashing out in class, perhaps ask if the user is aware of issues at home, if it's a group of children, ask about the group dynamic and perhaps specific issues of the different children in the group.

            Ask a number of specific questions.

            For example:

            "To your knowledge, does the child have any special educational needs or disabilities, such as ADHD, dyslexia, OCD, or maybe on the autistic spectrum? Are there any problems at home that you're aware of between the parents? Are there any language difficulties, such as the mother tongue being different to that spoken at school? And also, do you happen to know if this child reacts similarly in other classes, in other subjects with other teachers?"
            """
        elif stage == 7:
            print("running stage 7")
            return """
            You are an expert in empathy and communication, acting as a coach for teachers navigating challenging situations.
            When you respond, do so promptly and clearly. 

            When you respond, do so promptly and clearly. Your goal is to guide the user through their challenging situation using one or more of the 9 KindGen principles that are applicable to the situation. 
            
            The 9 KindGen principles are as follows:

            - {PRINCIPLES['PRINCIPLE_1']}
            - {PRINCIPLES['PRINCIPLE_2']}
            - {PRINCIPLES['PRINCIPLE_3']}
            - {PRINCIPLES['PRINCIPLE_4']}
            - {PRINCIPLES['PRINCIPLE_5']}
            - {PRINCIPLES['PRINCIPLE_6']}
            - {PRINCIPLES['PRINCIPLE_7']}
            - {PRINCIPLES['PRINCIPLE_8']}
            - {PRINCIPLES['PRINCIPLE_9']}

            You MUST not, under any circumstances, make up principles. Cite the name of the principle as given e.g. "Blank Sheet Attitude", "One for All, All for One" - do not alter these. 
        

            If a number of principles are applicable, choose max 3. 

            Base your response, including the principles chosen, on the user input thus far from your chat history, where the user explains the situation, who its affected, how its affecting them, etc.
            
            Make sure the principles you choose are relevant for the user's situation, and briefly explain how they are relevant.

            Finally, suggest a number of potential actions for the user based on each suggested principle. Once again you must make these specific and relevant to both the principle(s) suggested and the user's situation and input thus far.

            A great example response for the situation "A child gets very stressed out when their test score is less than fantastic" could look like:

            "Let's explore the 9 Kind Gen Principles and look at which ones may help here. 

            So firstly, we have One for All and All for One. And it seems that this principle actually would help in this situation, because it could well be that this child feels alone with their problem. And so creating a class environment where all of the pupils, all of the children feel a common goal that they're all supporting each other towards, so that everybody's on his side in this situation, so he doesn't feel alone.

            The principle of Empathetic Listening is likely also to be important here, because when we feel deeply heard and understood, we tend to calm down. So that principle probably applies here.

            The principle of Safe to Fall, is having a safe space where the child understands that it's all right, it's okay if they don't get great grades, so they feel safe. That feels applicable here. 

            And the principle of Finding the Child's Best Way. It could be that the child has other learning methods that would be better for them and support them better when taking tests. 

            Firstly, if you would like to understand more about any of those four principles, you can listen to those below before we go on. 

            Let's go through them one by one and look at what potential actions you could do for each of those principles. 

            So with One for All and All for One, the key here is that the class feels aligned around a particular goal and are supporting, rooting for each other. So one action here could be to align the entire class around an 'opponent' which is outside of the test, at least on an individual basis. For example, the class average being a goal that the whole class aligns around, and all of the children supporting each other in the test, and celebrating each other's successes and supporting each other, commiserating when they as individuals don't do so well, but all of them having an eye on that larger goal of the class performance as a whole. It may be that this child would benefit a lot - since it sounds like they are generally a high performer - from mentoring and supporting a low-performing child. And that would give this child who gets upset with test scores, even slightly subpar test scores, it would give them a lot of confidence feeling that they are supporting and mentoring another child in the class. 

            With the Empathetic Listening Principle, it sounds like it would be a good idea to sit down with the child and to ask them what their expectations are every time they sit a test and also to explore what kind of preparation they're doing and also what happens. when they don't perform so well, at home. So in other words, how their parents react ie try to understand whether there's a lot of parental pressure here.

            The Safe to Fall Principle applies here by really helping the children understand that these tests are not be and end all tests. The journey of life is much, much, much bigger than these tests, so that they feel they have a larger and wiser perspective on these tests. And they understand particularly that you as the teacher are not going to criticize or punish them if they underperform. 

            With the Find the child's Best learning way principle, you may find when you speak with the child that the method being used in the class to discuss the topic and learn the topic is not optimal for the child. You may gain some insight or intuition into an alternative way to really help the child's learning. 

            Alright, so of those four principles and the ideas from each of those four, which resonate most with you now? Which feels most doable? 
            "
            """
        else:
            return "I'm not sure I understand!"

    if conversation_stage > n_stages:
        st.balloons()
        user_input = None
    else:
        dynamic_prompt = build_stage_prompt(conversation_stage)
        assistant_message = st.chat_message("assistant")
        evaluation_result = evaluate_response(
            dynamic_prompt,
            st.session_state["messages"][-2]["text"],
            user_input,
            conversation_stage,
        )
        print(evaluation_result)
        if (
            evaluation_result.translate(
                str.maketrans("", "", string.punctuation)
            ).lower()
            == "yes"
        ):
            st.session_state["state"]["stage"] = conversation_stage + 1
            dynamic_prompt = build_stage_prompt(st.session_state["state"]["stage"])
            assistant_response = assistant_message.write_stream(
                respond(dynamic_prompt, chat_history)
            )
            st.session_state["messages"].append(
                {"role": "assistant", "text": assistant_response}
            )
        else:
            chat_history.pop()
            chat_history.pop()
            assistant_message.write_stream(fake_stream("I'm not sure I understand."))
            assistant_response = assistant_message.write_stream(
                respond(dynamic_prompt, chat_history)
            )
            st.session_state["messages"].append(
                {"role": "assistant", "text": assistant_response}
            )
