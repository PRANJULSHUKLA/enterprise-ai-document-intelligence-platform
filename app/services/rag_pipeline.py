import time

from google.genai import types

from app.constants.models import GeminiModels
from app.constants.rag import RAGConfig

from app.llm.gemini import client

from app.services.context_builder import ContextBuilder
from app.services.prompt_service import PromptService
from app.services.retrieval_service import RetrievalService


class RAGPipeline:

    def __init__(self):

        self.retriever = RetrievalService()

    async def run(
        self,
        file_id: str,
        question: str,
    ):

        overall_start = time.perf_counter()

        # ==================================================
        # 1. Retrieval
        # ==================================================

        retrieval_start = time.perf_counter()

        chunks = await self.retriever.retrieve_chunks(
            file_id=file_id,
            question=question,
            limit=RAGConfig.TOP_K,
        )

        retrieval_time = (
            time.perf_counter() - retrieval_start
        )

        # ==================================================
        # 2. No Results
        # ==================================================

        if not chunks:

            total_time = (
                time.perf_counter() - overall_start
            )

            return {
                "answer": (
                    "I couldn't find relevant information "
                    "in the uploaded document."
                ),
                "sources": [],
                "retrieval_time_ms": round(
                    retrieval_time * 1000,
                    2,
                ),
                "generation_time_ms": 0.0,
                "total_time_ms": round(
                    total_time * 1000,
                    2,
                ),
            }

        # ==================================================
        # 3. Relevance Check
        # ==================================================

        top_score = chunks[0].get(
            "score",
            0.0,
        )

        if top_score < RAGConfig.MIN_SIMILARITY_SCORE:

            total_time = (
                time.perf_counter() - overall_start
            )

            return {
                "answer": (
                    "I couldn't find enough relevant information "
                    "in the uploaded document to answer that question."
                ),
                "sources": [],
                "retrieval_time_ms": round(
                    retrieval_time * 1000,
                    2,
                ),
                "generation_time_ms": 0.0,
                "total_time_ms": round(
                    total_time * 1000,
                    2,
                ),
            }

        # ==================================================
        # 4. Context Construction
        # ==================================================

        context_chunks = chunks[
            :RAGConfig.MAX_CONTEXT_CHUNKS
        ]

        context = ContextBuilder.build(
            context_chunks
        )

        # Prevent excessively large prompts
        if len(context) > RAGConfig.MAX_CONTEXT_LENGTH:

            context = context[
                :RAGConfig.MAX_CONTEXT_LENGTH
            ]

        # ==================================================
        # 5. Prompt Construction
        # ==================================================

        prompt = PromptService.build(
            question=question,
            context=context,
        )

        # ==================================================
        # 6. Gemini Generation
        # ==================================================

        llm_start = time.perf_counter()

        response = client.models.generate_content(
            model=GeminiModels.CHAT,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=RAGConfig.TEMPERATURE,
                max_output_tokens=RAGConfig.MAX_OUTPUT_TOKENS,
            ),
        )

        generation_time = (
            time.perf_counter() - llm_start
        )

        # ==================================================
        # 7. Extract Answer
        # ==================================================

        answer = (
            response.text.strip()
            if response.text
            else "I couldn't generate an answer."
        )

        # ==================================================
        # 8. Total Time
        # ==================================================

        total_time = (
            time.perf_counter() - overall_start
        )

        # ==================================================
        # 9. Sources
        # ==================================================

        sources = [
            {
                "filename": chunk.get(
                    "filename"
                ),
                "page_number": chunk.get(
                    "page_number"
                ),
                "chunk_index": chunk.get(
                    "chunk_index"
                ),
                "score": round(
                    chunk.get(
                        "score",
                        0.0,
                    ),
                    4,
                ),
            }
            for chunk in context_chunks
        ]

        # ==================================================
        # 10. Logs
        # ==================================================

        print("\n" + "=" * 70)
        print("RAG PIPELINE")
        print("=" * 70)

        print(
            f"Question            : {question}"
        )

        print(
            f"Retrieved Chunks    : {len(chunks)}"
        )

        print(
            f"Context Chunks      : {len(context_chunks)}"
        )

        print(
            f"Context Length      : {len(context)} chars"
        )

        print(
            f"Top Similarity      : {top_score:.4f}"
        )

        print(
            f"Retrieval Time      : {retrieval_time:.3f} sec"
        )

        print(
            f"Generation Time     : {generation_time:.3f} sec"
        )

        print(
            f"Total Time          : {total_time:.3f} sec"
        )

        print("=" * 70)

        # ==================================================
        # 11. Response
        # ==================================================

        return {
            "answer": answer,
            "sources": sources,
            "retrieval_time_ms": round(
                retrieval_time * 1000,
                2,
            ),
            "generation_time_ms": round(
                generation_time * 1000,
                2,
            ),
            "total_time_ms": round(
                total_time * 1000,
                2,
            ),
        }