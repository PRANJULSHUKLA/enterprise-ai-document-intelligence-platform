class AgentConfig:

    # ==================================================
    # Document Analysis
    # ==================================================

    CONTRACT_ANALYSIS = "contract"

    MAX_DOCUMENT_LENGTH = 30000

    # ==================================================
    # Generation
    # ==================================================

    TEMPERATURE = 0.1

    MAX_OUTPUT_TOKENS = 8192

    # ==================================================
    # Risk Analysis
    # ==================================================

    RISK_CATEGORIES = [
        "financial",
        "contractual",
        "compliance",
        "operational",
        "privacy",
        "ambiguity",
        "deadline",
        "missing_information",
        "general",
    ]

    RISK_SEVERITIES = [
        "low",
        "medium",
        "high",
    ]

    DEFAULT_RULE_CONFIDENCE = 0.95