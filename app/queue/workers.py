import asyncio
import time

from pathlib import Path

from bson import ObjectId
from pdf2image import convert_from_path

from app.constants.status import FileStatus

from app.db.collections.files import files_collection
from app.db.collections.chunks import chunks_collection

from app.llm.vision import image_to_markdown
from app.llm.embeddings import generate_embedding

from app.schemas.chunk import ChunkSchema

from app.utils.chunker import create_chunks


def process_file(file_id: str, file_path: str):

    async def _process():

        start_time = time.perf_counter()
        filename = Path(file_path).name

        print("=" * 60)
        print(f"Started processing file: {file_id}")
        print("=" * 60)

        # ----------------------------------------------------
        # Stage 1 : Processing
        # ----------------------------------------------------

        await files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {
                "$set": {
                    "status": FileStatus.PROCESSING
                }
            }
        )

        print("\nConverting PDF into images...")

        pages = convert_from_path(file_path)

        print(f"Total pages found: {len(pages)}")

        await files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {
                "$set": {
                    "status": FileStatus.EXTRACTING_TEXT
                }
            }
        )

        # Store OCR output page-by-page.
        page_markdowns = []

        # ----------------------------------------------------
        # Stage 2 : OCR using Gemini Vision
        # ----------------------------------------------------

        for index, page in enumerate(pages):

            page_number = index + 1

            image_path = (
                f"{file_path}_page_{index}.jpg"
            )

            print(
                f"\nSaving page {page_number}..."
            )

            page.save(
                image_path,
                "JPEG"
            )

            print(
                f"Sending page {page_number} "
                "to Gemini Vision..."
            )

            try:

                markdown = image_to_markdown(
                    image_path
                )

                print(
                    f"Page {page_number} "
                    "processed successfully."
                )

                page_markdowns.append(
                    {
                        "page_number": page_number,
                        "markdown": markdown,
                    }
                )

            except Exception as e:

                print(
                    f"Failed to process "
                    f"page {page_number}"
                )

                print(e)

                await files_collection.update_one(
                    {"_id": ObjectId(file_id)},
                    {
                        "$set": {
                            "status": FileStatus.FAILED
                        }
                    }
                )

                raise

        # ----------------------------------------------------
        # Stage 3 : Chunking
        # ----------------------------------------------------

        print(
            "\nCreating Knowledge Base "
            "(splitting document into chunks)..."
        )

        await files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {
                "$set": {
                    "status": (
                        FileStatus.CREATING_KNOWLEDGE_BASE
                    )
                }
            }
        )

        # Create page-aware chunks.
        page_chunks = []

        for page_data in page_markdowns:

            page_number = page_data[
                "page_number"
            ]

            markdown = page_data[
                "markdown"
            ]

            chunks = create_chunks(
                markdown
            )

            for chunk in chunks:

                page_chunks.append(
                    {
                        "page_number": page_number,
                        "text": chunk,
                    }
                )

        print(
            f"Total chunks created: "
            f"{len(page_chunks)}"
        )

        # ----------------------------------------------------
        # Stage 4 : Generate Embeddings
        # ----------------------------------------------------

        await files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {
                "$set": {
                    "status": (
                        FileStatus.CREATING_CHUNK_EMBEDDINGS
                    )
                }
            }
        )

        for index, chunk_data in enumerate(
            page_chunks
        ):

            chunk = chunk_data["text"]

            page_number = chunk_data[
                "page_number"
            ]

            print(
                f"Creating embedding for chunk "
                f"{index + 1}/{len(page_chunks)} "
                f"(page {page_number}, "
                f"{len(chunk)} characters)"
            )

            try:

                embedding = generate_embedding(
                    chunk
                )

                chunk_document = ChunkSchema(
                    file_id=file_id,
                    filename=filename,
                    page_number=page_number,
                    chunk_index=index,
                    chunk_length=len(chunk),
                    document_type="general",
                    language="unknown",
                    embedding_model=(
                        "models/gemini-embedding-001"
                    ),
                    embedding_dimension=len(
                        embedding
                    ),
                    text=chunk,
                    embedding=embedding,
                )

                await chunks_collection.insert_one(
                    chunk_document.model_dump()
                )

            except Exception as e:

                print(
                    f"Failed to create embedding "
                    f"for chunk {index + 1}"
                )

                print(e)

                await files_collection.update_one(
                    {"_id": ObjectId(file_id)},
                    {
                        "$set": {
                            "status": (
                                FileStatus.FAILED
                            )
                        }
                    }
                )

                raise

        # ----------------------------------------------------
        # Stage 5 : Completed
        # ----------------------------------------------------

        full_markdown = "\n\n".join(
            page["markdown"]
            for page in page_markdowns
        )

        processing_time = round(
            time.perf_counter()
            - start_time,
            2,
        )

        await files_collection.update_one(
            {"_id": ObjectId(file_id)},
            {
                "$set": {
                    "status": FileStatus.COMPLETED,
                    "markdown": full_markdown,
                    "total_pages": len(pages),
                    "total_chunks": len(page_chunks),
                    "processing_time": processing_time,
                }
            }
        )

        print("\n" + "=" * 60)
        print(
            "Document processing completed "
            "successfully!"
        )
        print(
            f"Filename              : {filename}"
        )
        print(
            f"Total pages processed : {len(pages)}"
        )
        print(
            f"Total chunks created  : "
            f"{len(page_chunks)}"
        )
        print(
            f"Processing time       : "
            f"{processing_time} sec"
        )
        print("=" * 60)

    asyncio.run(_process())