import time

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

        # ---------------------------------------
        # Retrieve Chunks
        # ---------------------------------------

        retrieval_start = time.perf_counter()

        chunks = await self.retriever.retrieve_chunks(
            file_id=file_id,
            question=question,
            limit=RAGConfig.TOP_K,
        )

        retrieval_time = (
            time.perf_counter() - retrieval_start
        )

        if not chunks:

            return {
                "answer": "No information found in the uploaded document.",
                "sources": [],
            }

        top_score = chunks[0]["score"]

        if top_score < RAGConfig.MIN_SIMILARITY_SCORE:

            return {
                "answer": "I couldn't find that information in the uploaded document.",
                "sources": [],
            }

        # ---------------------------------------
        # Build Context
        # ---------------------------------------

        context = ContextBuilder.build(chunks)

        prompt = PromptService.build(
            question=question,
            context=context,
        )

        # ---------------------------------------
        # Ask Gemini
        # ---------------------------------------

        llm_start = time.perf_counter()

        response = client.models.generate_content(
            model=GeminiModels.CHAT,
            contents=prompt,
        )

        llm_time = (
            time.perf_counter() - llm_start
        )

        answer = response.text.strip()

        total_time = (
            time.perf_counter() - overall_start
        )

        # ---------------------------------------
        # Logs
        # ---------------------------------------

        print("\n" + "=" * 60)
        print("RAG PIPELINE")
        print("=" * 60)
        print(f"Question           : {question}")
        print(f"Retrieved Chunks   : {len(chunks)}")
        print(f"Top Similarity     : {top_score:.4f}")
        print(f"Retrieval Time     : {retrieval_time:.3f} sec")
        print(f"Gemini Time        : {llm_time:.3f} sec")
        print(f"Total Time         : {total_time:.3f} sec")
        print("=" * 60)

        return {
            "answer": answer,
            "sources": [
                {
                    "chunk_index": chunk["chunk_index"],
                    "score": round(chunk["score"], 4),
                }
                for chunk in chunks
            ],
        }