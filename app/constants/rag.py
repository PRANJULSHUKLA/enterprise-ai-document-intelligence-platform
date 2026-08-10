class RAGConfig:

    # ==================================================
    # Retrieval
    # ==================================================

    TOP_K = 4

    MAX_CONTEXT_CHUNKS = 4

    MIN_SIMILARITY_SCORE = 0.65

    VECTOR_INDEX_NAME = "vector_index"

    VECTOR_SEARCH_CANDIDATES = 50

    # ==================================================
    # Generation
    # ==================================================

    MAX_OUTPUT_TOKENS = 2048

    TEMPERATURE = 0.2

    # ==================================================
    # Context
    # ==================================================

    MAX_CONTEXT_LENGTH = 8000