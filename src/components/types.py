from dataclasses import dataclass
from typing import Literal

# Define available options as tuples for consistency
INTERVIEW_TYPES = ("General", "Technical", "Behavioral", "Job Specific")
TECHNICAL_FOCUS_OPTIONS = (
    "Data Science",
    "AI/ML Engineer",
    "Python Developer",
    "TypeScript Developer",
    "Scala Developer",
    "Go Developer",
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
