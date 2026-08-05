import asyncio

from app.services.retrieval_service import RetrievalService


async def main():

    service = RetrievalService()

    chunks = await service.retrieve_chunks(
        "What is this document about?"
    )

    print("=" * 60)
    print("Chunks Loaded :", len(chunks))
    print("=" * 60)

    if chunks:

        print(chunks[0]["text"][:300])


asyncio.run(main())