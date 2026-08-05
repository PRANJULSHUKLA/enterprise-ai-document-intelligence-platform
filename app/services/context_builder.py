from app.constants.rag import RAGConfig


class ContextBuilder:

    @staticmethod
    def build(chunks: list[dict]) -> str:
        """
        Combines retrieved chunks into a single context
        for the LLM prompt.
        """

        context = []

        for chunk in chunks[:RAGConfig.MAX_CONTEXT_CHUNKS]:

            context.append(
                f"""
==============================
DOCUMENT CHUNK {chunk["chunk_index"]}
==============================

{chunk["text"]}
"""
            )

        return "\n".join(context).strip()