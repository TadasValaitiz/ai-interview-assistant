import streamlit as st
import os


def api_key_section():
    """Component for handling OpenAI API key input."""
    
    if "openai_api_key" not in st.session_state:
        st.session_state.openai_api_key = os.getenv("OPENAI_API_KEY", "")
    
    if not st.session_state.openai_api_key:
        st.warning("Please enter your OpenAI API key to use the application.")
        with st.form("api_key_form"):
            api_key_input = st.text_input(
                "OpenAI API Key",
                type="password",
                placeholder="sk-...",
                help="You can get your API key from https://platform.openai.com/api-keys",
            )
            submit_button = st.form_submit_button("Submit API Key")
            if submit_button and api_key_input:
                st.session_state.openai_api_key = api_key_input
                st.success("API key set successfully! You can now use the application.")
                st.rerun()
