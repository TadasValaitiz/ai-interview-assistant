from dataclasses import dataclass
from tkinter import NO
import streamlit as st
from openai import OpenAI
from components.types import AiOptions, ChatMessage, InterviewSettings
from openai.types.chat import ChatCompletionMessageParam
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],  # Output to console
)


def init_chat_state(settings: InterviewSettings) -> None:
    """Initialize chat state for the current interview type."""
    if "messages" not in st.session_state:
        st.session_state.messages = {}
    if settings.descriptor not in st.session_state.messages:
        st.session_state.messages[settings.descriptor] = []


def add_message(settings: InterviewSettings, message: ChatMessage) -> None:
    """Add a message to the session state for the current interview type."""
    init_chat_state(settings)
    st.session_state.messages[settings.descriptor].append(message)


def prepare_reply_messages(
    settings: InterviewSettings,
) -> list[ChatCompletionMessageParam]:
    """Prepare reply messages for OpenAI API"""
    system_message: ChatCompletionMessageParam = {
        "role": "system",
        "content": create_system_prompt(settings),
    }

    history = st.session_state.messages[settings.descriptor]
    messages: list[ChatCompletionMessageParam] = [system_message] + [
        {"role": msg.role, "content": msg.content} for msg in history
    ]

    return messages


def prepare_initial_messages(
    settings: InterviewSettings,
) -> list[ChatCompletionMessageParam]:
    """Prepare messages for OpenAI API including system prompt."""
    system_message: ChatCompletionMessageParam = {
        "role": "system",
        "content": create_system_prompt(settings),
    }

    user_message: ChatCompletionMessageParam = {
        "role": "user",
        "content": "Welcome me and give first question.",
    }

    messages: list[ChatCompletionMessageParam] = [system_message, user_message]

    return messages


def create_system_prompt(settings: InterviewSettings) -> str:
    """Create system prompt based on interview settings."""
    system_prompt = f"You are an expert interviewer conducting a {settings.interview_type.lower()} interview."

    if settings.has_technical_focus:
        system_prompt += (
            f"\nThis is specifically for a {settings.technical_focus} position."
        )

    if settings.has_job_description:
        system_prompt += f"\nThe candidate is interviewing for a position with this description: {settings.job_description}"

    system_prompt += """\nAsk candidate questions. 
    Focus only on interview subject. If candidate reply is not related with interview, repeat question. If candidate replies that he don't know, procceed with next question.
    \nYou can start with simple questions, then proceed with more dificult. For developer roles, you can give some code snippets.
    \nKeep track of how many interview questions candidate answered.
    \nWhen Evaluating interview provide evaluation for each question. If you can add something to answer, please add, so candidate can learn later.
    \nnExample 1 for typescript developer interview:
    Question 1. What is the difference between `const` and `let` in typescript?
    \nnExample 1 for typescript developer interview:
    Question 2. What is the difference between interface and class and type in typescript?
    """
    return system_prompt


def fetch_open_AI(messages: list[ChatCompletionMessageParam]) -> str | None:
    """Fetch response from OpenAI API."""
    options: AiOptions = AiOptions(dict(st.session_state))

    logging.warning("Options: %s", options)

    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            top_p=options.top_p,
            frequency_penalty=options.frequency_penalty,
            presence_penalty=options.presence_penalty,
            max_tokens=options.max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None
