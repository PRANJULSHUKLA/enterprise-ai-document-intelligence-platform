from app.constants.rag import RAGConfig

from app.db.collections.chunks import chunks_collection

from app.llm.embeddings import generate_embedding


class RetrievalService:

    async def retrieve_chunks(
        self,
        file_id: str,
        question: str,
        limit: int = RAGConfig.TOP_K,
    ):

        # ----------------------------------------
        # Generate Question Embedding
        # ----------------------------------------

        query_embedding = generate_embedding(question)

        # ----------------------------------------
        # MongoDB Atlas Vector Search
        # ----------------------------------------

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 100,
                    "limit": limit,
                    "filter": {
                        "file_id": file_id
                    }
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "chunk_index": 1,
                    "text": 1,
                    "score": {
                        "$meta": "vectorSearchScore"
                    }
                }
            }
        ]

        cursor = chunks_collection.aggregate(pipeline)

        chunks = []

        async for doc in cursor:

            chunks.append(
                {
                    "chunk_index": doc["chunk_index"],
                    "text": doc["text"],
                    "score": doc["score"],
                }
            )

        return chunks