import streamlit as st
from openai import OpenAI
from typing import Iterable, Tuple
from components.types import (
    InterviewSettings
)
from openai.types.chat import ChatCompletionMessageParam


def initial_content():
    if not hasattr(st.session_state, "interview_type"):
        st.markdown(
            """
        This app helps you prepare for interviews using AI. You can:
        - Practice answering interview questions
        - Get feedback on your responses
        - Prepare for specific job positions
        """
        )
    else:
        st.markdown("This is message thread")


def main_content(settings: InterviewSettings) -> None:
    initial_content()
    prompt = st.chat_input("Say something")
    fetch_open_AI([{"content": prompt, "role": "user"}])


def system_prompt(settings: InterviewSettings):
    # Create the system prompt based on interview type
    system_prompt = f"You are an experienced interviewer conducting a {settings.interview_type.lower()} interview."

    if settings.has_technical_focus:
        system_prompt += (
            f"\nThis is specifically for a {settings.technical_focus} position."
        )

    if settings.has_job_description:
        system_prompt += f"\nThe candidate is interviewing for a position with this description: {settings.job_description}"


def fetch_open_AI(messages: Iterable[ChatCompletionMessageParam]):
    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating question: {str(e)}")


def chat_messages2(settings: InterviewSettings) -> None:
    """Component for displaying chat messages and generating questions."""
    question_container = st.container()
    with question_container:
        if st.button("Generate Question"):
            if not st.session_state.openai_api_key:
                st.error("Please enter your OpenAI API key at the top of the page!")
            else:
                with st.spinner("Generating question..."):
                    # Create the system prompt based on interview type
                    system_prompt = f"You are an experienced interviewer conducting a {settings.interview_type.lower()} interview."

                    if settings.has_technical_focus:
                        system_prompt += f"\nThis is specifically for a {settings.technical_focus} position."

                    if settings.has_job_description:
                        system_prompt += f"\nThe candidate is interviewing for a position with this description: {settings.job_description}"

                    # Generate question using OpenAI
                    try:
                        client = OpenAI(api_key=st.session_state.openai_api_key)
                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {
                                    "role": "user",
                                    "content": f"Generate a challenging {settings.interview_type.lower()} interview question."
                                    + (
                                        f" for {settings.technical_focus}"
                                        if settings.has_technical_focus
                                        else ""
                                    ),
                                },
                            ],
                            temperature=0.7,
                        )
                        st.session_state.current_question = response.choices[
                            0
                        ].message.content
                        st.write("Question:", st.session_state.current_question)
                    except Exception as e:
                        st.error(f"Error generating question: {str(e)}")


def get_feedback(question: str, answer: str) -> str:
    """Helper function to get feedback on user's answer."""
    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert interviewer providing constructive feedback.",
                },
                {
                    "role": "user",
                    "content": f"Question: {question}\nCandidate's Answer: {answer}\n\nProvide constructive feedback on the answer, including strengths and areas for improvement.",
                },
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating feedback: {str(e)}"
