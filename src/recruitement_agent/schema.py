from typing import Annotated, List, Literal, Dict, Optional
import operator

from pydantic import BaseModel, Field
from typing_extensions import TypedDict

from langchain_core.messages import AnyMessage
from langchain_core.documents import Document


class ExperienceCategoryResponse(BaseModel):
    """Schema for agent response for categorizing profiles based on their experience level."""

    category: Literal[
        "fresher",
        "experienced",
        "senior"
    ] = Field(
        description="Experience category of the candidate."
    )

    confidence_score: int = Field(
        ge=0,
        le=100,
        description="Confidence score for the assigned experience category, from 0 to 100."
    )

    sources: List[str] = Field(
        description="Relevant excerpts from the candidate profile that support the experience categorization."
    )


class SkillMatch(BaseModel):
    matched: List[str] = Field(
        description=(
            "Skills explicitly demonstrated by the candidate through "
            "their skills, projects, work experience, education, "
            "certifications, or other concrete experience."
        )
    )

    partially_matched: List[str] = Field(
        description=(
            "Skills for which the candidate provides explicit but incomplete "
            "evidence. Use this only when the candidate demonstrates a "
            "meaningful part of the same skill, but the evidence is "
            "insufficient for a full match."
        )
    )

    missing: List[str] = Field(
        description=(
            "Skills for which the candidate profile contains no explicit "
            "supporting evidence. Do not infer these skills from related "
            "technologies, projects, or general technical experience."
        )
    )


class SkillAssessmentResponse(BaseModel):
    job_id: str = Field(
        description="ID of the job being assessed."
    )

    required_skills: SkillMatch = Field(
        description="Assessment of required job skills against the candidate profile."
    )

    preferred_skills: SkillMatch = Field(
        description="Assessment of preferred job skills against the candidate profile."
    )

    reasoning: str = Field(
        description=(
            "Concise 1-2 sentence explanation of the most important "
            "matched skills, missing skills, and relevant candidate evidence."
        )
    )

    recommendation: Literal[
        "reject_application",
        "forward_to_recruiter",
        "schedule_assessment",
    ] = Field(
        description=(
            "Recommended next workflow action based on the candidate "
            "profile assessment for the specified job."
        )
    )


class SkillAssessmentList(BaseModel):
    assessments: List[SkillAssessmentResponse] = Field(
        description="Skill assessments for every retrieved job."
    )


class WorkflowResult(BaseModel):
    job_id: str
    match_score: int

    recommendation: Literal[
        "reject_application",
        "forward_to_recruiter",
        "schedule_assessment",
    ]

    status: Literal[
        "rejected",
        "pending_recruiter_review",
        "pending_assessment",
    ]


class RecruitmentState(TypedDict):
    messages: List[AnyMessage]
    experience: Optional[ExperienceCategoryResponse]
    retrieved_jobs: List[Document]
    skill_assessments: List[SkillAssessmentResponse]
    match_scores: Dict[str, int]

    workflow_results: Annotated[
        List[WorkflowResult],
        operator.add
    ]

class JobRoutingState(TypedDict):
    job_id: str
    match_score: int
    assessment: SkillAssessmentResponse
    recommendation: Literal[
        "reject_application",
        "forward_to_recruiter",
        "schedule_assessment",
    ]