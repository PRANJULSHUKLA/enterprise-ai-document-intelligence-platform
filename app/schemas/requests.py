from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    file_id: str = Field(
        ...,
        description="MongoDB File ID of the uploaded document",
    )

    question: str = Field(
        ...,
        min_length=1,
        description="User question to ask about the uploaded document",
    )


class AnalysisRequest(BaseModel):
    file_id: str = Field(
        ...,
        description="MongoDB File ID of the uploaded document",
    )

    analysis_type: str = Field(
        default="contract",
        description="Type of document analysis to perform",
    )


class WorkflowRequest(BaseModel):
    file_id: str = Field(
        ...,
        description="MongoDB File ID of the uploaded document",
    )

    objective: str = Field(
        ...,
        min_length=1,
        description="Business objective for which the workflow should be generated",
    )