import streamlit as st
from typing import Tuple
from dataclasses import dataclass
from components.types import (
    AiOptions,
    InterviewSettings,
    TECHNICAL_FOCUS_OPTIONS,
    INTERVIEW_TYPES,
)


def sidebar() -> InterviewSettings:
    """Sidebar component for interview settings."""
    with st.sidebar:
        st.header("Choose Interview")

        # Initialize session state if not present
        if "interview_type" not in st.session_state:
            st.session_state.interview_type = "General"
        if "job_description" not in st.session_state:
            st.session_state.job_description = ""
        if "technical_focus" not in st.session_state:
            st.session_state.technical_focus = "Data Science"

        if "ai_temperature" not in st.session_state:
            st.session_state.ai_temperature = 0.7
        if "ai_top_p" not in st.session_state:
            st.session_state.ai_top_p = 1.0
        if "ai_max_tokens" not in st.session_state:
            st.session_state.ai_max_tokens = 4096
        if "ai_frequency_penalty" not in st.session_state:
            st.session_state.ai_frequency_penalty = 0.0
        if "ai_presence_penalty" not in st.session_state:
            st.session_state.ai_presence_penalty = 0.0

        # Interview type selection
        interview_type = st.selectbox(
            label="Select Interview Type",
            options=INTERVIEW_TYPES,
            key="interview_type",
        )

        # Technical focus selection
        technical_focus = st.session_state.technical_focus
        if interview_type == "Technical":
            technical_focus = st.radio(
                label="Select Technical Interview Focus",
                options=TECHNICAL_FOCUS_OPTIONS,
                horizontal=False,
                key="technical_focus",
            )

        # Job description input
        job_description = ""
        if interview_type == "Job Specific":
            job_description = st.text_area(
                "Paste Job Description",
                height=200,
                placeholder="Paste the job description here...",
                key="job_description",
            )

        #ai options
        with st.expander("Options"):
            st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                step=0.1,
                key="ai_temperature",
            )
            st.slider("Top P", min_value=0.0, max_value=1.0, step=0.1, key="ai_top_p")
            st.slider(
                label="Max Tokens",
                min_value=1,
                max_value=16383,
                step=1,
                key="ai_max_tokens",
            )
            st.slider(
                "Frequency Penalty",
                min_value=0.0,
                max_value=2.0,
                step=0.1,
                key="ai_frequency_penalty",
            )
            st.slider(
                "Presence Penalty",
                min_value=0.0,
                max_value=2.0,
                step=0.1,
                key="ai_presence_penalty",
            )

        return InterviewSettings(
            interview_type=interview_type,
            job_description=job_description,
            technical_focus=technical_focus,
        )
