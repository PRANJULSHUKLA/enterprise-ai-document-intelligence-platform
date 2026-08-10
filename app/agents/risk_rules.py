from app.constants.agent import AgentConfig


class RiskRules:

    # ==================================================
    # Placeholder Detection
    # ==================================================

    PLACEHOLDER_TERMS = [
        "xxx",
        "______",
        "___",
        "[insert",
        "[insert here",
        "to be confirmed",
        "tbc",
        "to be determined",
        "tbd",
    ]

    # ==================================================
    # Rule Metadata
    # ==================================================

    PLACEHOLDER_CATEGORY = "missing_information"

    PLACEHOLDER_SEVERITY = "medium"

    PLACEHOLDER_CONFIDENCE = (
        AgentConfig.DEFAULT_RULE_CONFIDENCE
    )