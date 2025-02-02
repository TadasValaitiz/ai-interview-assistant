import streamlit as st
import os
from dotenv import load_dotenv
from components.api_key_section import api_key_section
from components.sidebar import sidebar
from components.main_content import main_content
from components.page import page

# Load environment variables
load_dotenv()


def init_session_state() -> None:
    """Initialize session state variables."""
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
    if "interview_type" not in st.session_state:
        st.session_state.interview_type = "General"
    if "job_description" not in st.session_state:
        st.session_state.job_description = ""


def main() -> None:
    """Main application function."""
    init_session_state()

    page()

    # API Key Section
    api_key_section()

    # Get interview settings from sidebar
    settings = sidebar()

    # Display chat interface
    main_content(settings)


if __name__ == "__main__":
    main()
