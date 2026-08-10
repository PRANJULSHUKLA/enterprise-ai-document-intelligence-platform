from app.constants.rag import RAGConfig


class ContextBuilder:

    @staticmethod
    def build(chunks: list[dict]) -> str:
        """
        Builds a structured, source-aware context for the LLM.
        """

        context = []

        for chunk in chunks[:RAGConfig.MAX_CONTEXT_CHUNKS]:

            filename = chunk.get(
                "filename",
                "Unknown document",
            )

            page_number = chunk.get(
                "page_number",
                "Unknown",
            )

            chunk_index = chunk.get(
                "chunk_index",
                "Unknown",
            )

            score = chunk.get(
                "score",
                0.0,
            )

            text = chunk.get(
                "text",
                "",
            )

            context.append(
                f"""
[SOURCE]
Document: {filename}
Page: {page_number}
Chunk: {chunk_index}
Relevance Score: {score}

[CONTENT]
{text}

[END SOURCE]
"""
            )

        return "\n".join(context).strip()