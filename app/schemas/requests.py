from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    file_id: str = Field(
        ...,
        description="MongoDB File ID of the uploaded document"
    )

    question: str = Field(
        ...,
        description="User question to ask about the uploaded document"
    )
    
class DocumentAnalysisRequest(BaseModel):

    file_id: str = Field(
        ...,
        description="MongoDB File ID of the uploaded document"
    )

    analysis_type: str = Field(
        default="contract",
        description="Type of document analysis to perform"
    )