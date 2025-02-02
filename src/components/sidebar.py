import streamlit as st
from typing import Tuple
from dataclasses import dataclass
from components.types import (
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

        return InterviewSettings(
            interview_type=interview_type,
            job_description=job_description,
            technical_focus=technical_focus,
        )
