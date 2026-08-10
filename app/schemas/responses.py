from pydantic import BaseModel, Field


class Source(BaseModel):

    filename: str | None = Field(
        default=None,
        description="Source document filename",
    )

    page_number: int | None = Field(
        default=None,
        description="Page number containing the retrieved content",
    )

    chunk_index: int = Field(
        ...,
        description="Chunk used to generate the answer",
    )

    score: float = Field(
        ...,
        description="Vector similarity score of the retrieved chunk",
    )


class ChatResponse(BaseModel):

    answer: str = Field(
        ...,
        description="Grounded answer generated from the uploaded document",
    )

    sources: list[Source] = Field(
        default_factory=list,
        description="Document pages and chunks used to generate the answer",
    )

    retrieval_time_ms: float = Field(
        ...,
        description="Time spent retrieving relevant document chunks",
    )

    generation_time_ms: float = Field(
        ...,
        description="Time spent generating the answer",
    )

    total_time_ms: float = Field(
        ...,
        description="Total RAG pipeline execution time",
    )