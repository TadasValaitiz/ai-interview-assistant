from dataclasses import dataclass
from tkinter import NO
from typing import Literal

from narwhals import Unknown

# Define available options as tuples for consistency
INTERVIEW_TYPES = ("General", "Technical", "Behavioral", "Job Specific")
TECHNICAL_FOCUS_OPTIONS = (
    "Data Science",
    "AI/ML Engineer",
    "Python Developer",
    "TypeScript Developer",
    "Scala Developer",
    "Go Developer",
    "UX/UI Designer",
    "Product Manager",
)

# Type definitions using Literal
InterviewType = Literal["General", "Technical", "Behavioral", "Job Specific"]
TechnicalFocus = Literal[
    "Data Science",
    "AI/ML Engineer",
    "Python Developer",
    "TypeScript Developer",
    "Scala Developer",
    "Go Developer",
    "UX/UI Designer",
    "Product Manager",
]


@dataclass
class InterviewSettings:
    """Class to store interview settings."""

    interview_type: InterviewType = "General"
    job_description: str = ""
    technical_focus: TechnicalFocus = "Data Science"

    @property
    def has_job_description(self) -> bool:
        """Check if job description is provided for Job Specific interview type."""
        return self.interview_type == "Job Specific" and bool(
            self.job_description.strip()
        )

    @property
    def has_technical_focus(self) -> bool:
        """Check if technical focus is relevant."""
        return self.interview_type == "Technical"

    @property
    def descriptor(self):
        """Interview descriptor"""
        focus = str(self.technical_focus if self.has_technical_focus else "non-focus")
        return f"{self.interview_type}:{focus}"


@dataclass
class ChatMessage:
    role: Literal["assistant", "user", "system"]
    content: str


@dataclass
class AiOptions:
    temperature: float | None = None
    top_p: float | None = None
    frequency_penalty: float | None = None
    presence_penalty: float | None = None
    max_tokens: int | None = None

    def __init__(self, session_state: dict) -> None:
        """Initialize AI options from session state dictionary."""
        self.temperature = session_state.get("ai_temperature")
        self.top_p = session_state.get("ai_top_p")
        self.frequency_penalty = session_state.get("ai_frequency_penalty")
        self.presence_penalty = session_state.get("ai_presence_penalty")
        self.max_tokens = session_state.get("ai_max_tokens")
