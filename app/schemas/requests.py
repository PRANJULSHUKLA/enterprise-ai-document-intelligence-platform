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