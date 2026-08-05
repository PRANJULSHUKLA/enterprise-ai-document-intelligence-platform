from app.db.collections.chunks import chunks_collection
from app.utils.chunker import create_chunks

import asyncio

from bson import ObjectId
from pdf2image import convert_from_path

from app.db.collections.files import files_collection
from app.llm.embeddings import generate_embedding
from app.llm.vision import image_to_markdown


def process_file(file_id: str, file_path: str):

    async def _process():

        print("=" * 60)
        print(f"Started processing: {file_id}")
        print("=" * 60)

        await files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {"$set": {"status": "processing"}}
        )

        print("Converting PDF to images...")
        pages = convert_from_path(file_path)

        await files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {"$set": {"status": "extracting text"}}
        )

        full_markdown = ""

        for index, page in enumerate(pages):

            image_path = f"{file_path}_page_{index}.jpg"

            print(f"Saving page {index + 1}...")

            page.save(image_path, "JPEG")

            print(f"Sending page {index + 1} to Gemini...")

            markdown = image_to_markdown(image_path)

            print(f"Page {index + 1} processed.")

            full_markdown += markdown + "\n\n"

        
        

        print("Chunking Documents...")

        await files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {
                "$set": {
                    "status": "chunking, creating knowledge base"
                    
                }
            }
        )
        
        chunks = create_chunks(full_markdown)
        print(f"Total chunks created: {len(chunks)}")
        
        await files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {
                "$set": {
                    "status": "creating chunk embeddings"
                }
            }
        )
        
        for index, chunk in enumerate(chunks):
            print(f"Creating embedding for chunk {index + 1}/{len(chunks)}...")
            embedding = generate_embedding(chunk)
            await chunks_collection.insert_one(
                {"file_id": file_id,
                 "chunk_index": index,
                 "text": chunk,
                 "embedding": embedding}
            )
            
        await files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {
                "$set": {
                    "status": "completed",
                    "markdown": full_markdown,
                    "chunks": len(chunks)
                }
            }
        )

        print("=" * 60)
        print("Processing completed successfully!")
        print(f"total chunks created: {len(chunks)}")
        print("=" * 60)

    asyncio.run(_process())