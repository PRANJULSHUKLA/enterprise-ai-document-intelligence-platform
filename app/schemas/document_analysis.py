from pydantic import BaseModel, Field


class Party(BaseModel):
    name: str = Field(
        description="Name of the party or organization."
    )

    role: str = Field(
        description="Role of the party in the document."
    )


class Obligation(BaseModel):
    party: str = Field(
        description="Party responsible for the obligation."
    )

    obligation: str = Field(
        description="Description of the obligation."
    )

    deadline: str | None = Field(
        default=None,
        description="Deadline or time period if explicitly stated."
    )

    evidence: str = Field(
        description="Exact or near-exact supporting text from the document."
    )


class FinancialTerm(BaseModel):
    description: str = Field(
        description="Description of the financial term."
    )

    amount: str | None = Field(
        default=None,
        description="Explicit monetary amount if present."
    )

    frequency: str | None = Field(
        default=None,
        description="Payment frequency if explicitly stated."
    )

    evidence: str = Field(
        description="Supporting evidence from the document."
    )


class RiskFlag(BaseModel):

    title: str = Field(
        description="Short title describing the risk."
    )

    category: str = Field(
        default="general",
        description=(
            "Risk category such as financial, contractual, "
            "compliance, operational, privacy, ambiguity, "
            "deadline, or missing_information."
        )
    )

    severity: str = Field(
        default="medium",
        description=(
            "Risk severity: low, medium, or high."
        )
    )

    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description=(
            "Confidence that the identified issue is a "
            "genuine risk based on the document."
        )
    )

    explanation: str = Field(
        description=(
            "Why this represents a potential issue "
            "based only on the document."
        )
    )

    evidence: str = Field(
        description=(
            "Short supporting passage from the document."
        )
    )

    source: str = Field(
        default="ai",
        description=(
            "Origin of the risk: ai or rule."
        )
    )


class MissingInformation(BaseModel):
    item: str = Field(
        description="Information that appears to be missing or unclear."
    )

    reason: str = Field(
        description="Why the information appears incomplete or unclear."
    )


class DocumentAnalysis(BaseModel):

    document_type: str = Field(
        description="Identified document type."
    )

    executive_summary: str = Field(
        description="Concise summary of the document."
    )

    parties: list[Party] = Field(
        default_factory=list
    )

    key_terms: list[str] = Field(
        default_factory=list,
        description="Important terms explicitly found in the document."
    )

    obligations: list[Obligation] = Field(
        default_factory=list
    )

    deadlines: list[str] = Field(
        default_factory=list,
        description="Important dates or deadlines explicitly stated."
    )

    financial_terms: list[FinancialTerm] = Field(
        default_factory=list
    )

    risks: list[RiskFlag] = Field(
        default_factory=list
    )

    missing_information: list[MissingInformation] = Field(
        default_factory=list
    )