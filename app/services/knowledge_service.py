from app.services.rag_pipeline import RAGPipeline


class KnowledgeService:

    def __init__(self):

        self.pipeline = RAGPipeline()

    async def ask(
        self,
        file_id: str,
        question: str,
    ):

        return await self.pipeline.run(
            file_id=file_id,
            question=question,
        )