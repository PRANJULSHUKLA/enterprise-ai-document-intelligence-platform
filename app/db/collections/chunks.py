from typing import TypedDict

from pymongo.asynchronous.collection import AsyncCollection

from app.db.db import database


class ChunkSchema(TypedDict):
    file_id: str
    chunk_index: int
    text: str
    embedding: list[float]


COLLECTION_NAME = "chunks"

chunks_collection: AsyncCollection[ChunkSchema] = database[
    COLLECTION_NAME
]