import streamlit as st
from openai import OpenAI
from components.types import ChatMessage, InterviewSettings
from openai.types.chat import ChatCompletionMessageParam


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
    system_message = {"role": "system", "content": create_system_prompt(settings)}

    history = st.session_state.messages[settings.descriptor]

    messages = [system_message] + [
        {"role": msg.role, "content": msg.content} for msg in history
    ]

    print("Reply essages:", messages)
    return messages


def prepare_initial_messages(
    settings: InterviewSettings,
) -> list[ChatCompletionMessageParam]:
    """Prepare messages for OpenAI API including system prompt."""
    system_message = {"role": "system", "content": create_system_prompt(settings)}

    content = "Welcome me and give me simple warm-up question. After I answer question, provide constructive feedback on the answer, including strengths and areas for improvement. After feedback ask another question. When I answer 3 questions. Give me a summary of interview and evaluation in table format"
    messages = [system_message, {"role": "user", "content": content}]

    print("Initial_messages:", messages)
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

    system_prompt += "\nAsk candidate questions. Focus only on interview subject. If candidate reply is not related with interview, repeat question. If candidate replies that he don't know, procceed with next question."
    return system_prompt


def fetch_open_AI(messages: list[ChatCompletionMessageParam]) -> str | None:
    """Fetch response from OpenAI API."""
    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def get_feedback(question: str, answer: str) -> str:
    """Helper function to get feedback on user's answer."""
    try:
        client = OpenAI(api_key=st.session_state.openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
        return str(response.choices[0].message.content)
    except Exception as e:
        return f"Error generating feedback: {str(e)}"
