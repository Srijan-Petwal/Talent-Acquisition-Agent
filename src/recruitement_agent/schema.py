from typing import List,Literal,Dict,Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langchain_core.documents import Document



class ExperienceCategoryResponse(BaseModel):
    """Schema for agent response for categorizing profiles based on their experience level"""
    category: Literal["fresher","experienced","senior"]= Field(description="Experience category of the candidate.")
    confidence_score:int=Field(
        ge=0,
        le=100,
        description="Confidenc score for the assigned experience category, from 0 to 100."
    )
    sources:List[str]=Field(
        description="Relevant excerpts from candidate profile that support the experience categorization."
    )

class RecruitmentState(TypedDict):
    messages:List[AnyMessage]
    experience:Optional[ExperienceCategoryResponse]
    retrieved_jobs:List[Document]