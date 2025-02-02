import streamlit as st
from dotenv import load_dotenv
from components.api_key_section import api_key_section
from components.sidebar import sidebar
from components.main_content import main_content
from components.page import page

# Load environment variables
load_dotenv()

def main() -> None:
    """Main application function."""

    page()

    # API Key Section
    api_key_section()

    # Get interview settings from sidebar
    settings = sidebar()

    # Display chat interface
    main_content(settings)


if __name__ == "__main__":
    main()
