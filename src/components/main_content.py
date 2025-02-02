import streamlit as st
from openai import OpenAI
from typing import Iterable
from components.api import (
    add_message,
    fetch_open_AI,
    init_chat_state,
    prepare_initial_messages,
    prepare_reply_messages,
)
from components.types import ChatMessage, InterviewSettings
from openai.types.chat import ChatCompletionMessageParam


def is_beginning(settings: InterviewSettings):
    current_messages = st.session_state.messages[settings.descriptor]
    return not current_messages


def messages_content(settings: InterviewSettings):
    """Display chat messages and welcome message."""
    init_chat_state(settings)

    if is_beginning(settings):
        st.markdown(
            """
        This app helps you prepare for interviews using AI. You can:
        - Practice answering interview questions
        - Get feedback on your responses
        - Prepare for specific job positions
        """
        )

    # Display all messages for current interview type
    current_messages = st.session_state.messages[settings.descriptor]
    for message in current_messages:
        with st.chat_message(message.role):
            st.write(message.content)


def main_content(settings: InterviewSettings) -> None:
    """Main chat interface."""
    messages_content(settings)

    if is_beginning(settings):
        role = f" {settings.technical_focus}" if settings.has_technical_focus else ""
        if st.button(f"Start {settings.interview_type}{role} interview"):
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    messages = prepare_initial_messages(settings)
                    handle_messages(settings=settings, messages=messages)
            st.rerun()

    else:
        chat_input(settings)


def chat_input(settings: InterviewSettings):
    if prompt := st.chat_input("Type your message here..."):
        user_message = ChatMessage(role="user", content=prompt)
        add_message(settings, user_message)

        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                messages = prepare_reply_messages(settings)
                handle_messages(settings=settings, messages=messages)
        st.rerun()


def handle_messages(
    settings: InterviewSettings, messages: list[ChatCompletionMessageParam]
):
    response = fetch_open_AI(messages)
    if response:
        st.write(response)
        assistant_message = ChatMessage(role="assistant", content=response)
        add_message(settings, assistant_message)
