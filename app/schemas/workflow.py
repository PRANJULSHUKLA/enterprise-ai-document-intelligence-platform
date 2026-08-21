from typing import Literal

from pydantic import BaseModel, Field


class ActionItem(BaseModel):

    priority: Literal[
        "critical",
        "high",
        "medium",
        "low",
    ]

    title: str

    action: str

    reason: str

    source: Literal[
        "analysis",
        "risk",
        "missing_information",
        "deadline",
        "ai",
    ] = "ai"

    evidence: str | None = None

    requires_human_approval: bool = False


class WorkflowPlan(BaseModel):

    readiness_status: Literal[
        "ready",
        "conditionally_ready",
        "not_ready",
        "insufficient_information",
    ]

    overall_assessment: str

    immediate_actions: list[ActionItem] = Field(
        default_factory=list
    )

    upcoming_actions: list[ActionItem] = Field(
        default_factory=list
    )

    monitoring_items: list[ActionItem] = Field(
        default_factory=list
    )

    human_approval_required: bool = False

    approval_reason: str | None = None