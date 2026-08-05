from pathlib import Path

from bson import ObjectId

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder

from app.constants.status import FileStatus

from app.schemas.file import FileSchema
from app.schemas.requests import ChatRequest
from app.schemas.responses import ChatResponse

from app.db.collections.files import files_collection

from app.queue.q import q
from app.queue.workers import process_file

from app.services.knowledge_service import KnowledgeService

app = FastAPI(
    title="Enterprise AI Document Intelligence Platform",
    version="1.0.0",
)


# =====================================================
# Health Check
# =====================================================

@app.get("/")
def health():

    return {
        "status": "healthy"
    }


# =====================================================
# Upload Document
# =====================================================

@app.post("/upload")
async def upload(file: UploadFile):

    try:

        document = FileSchema(
            filename=file.filename,
            status=FileStatus.SAVING,
        )

        db_file = await files_collection.insert_one(
            document.model_dump()
        )

        file_id = str(db_file.inserted_id)

        upload_dir = Path("/mnt/uploads") / file_id

        upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = upload_dir / file.filename

        with open(file_path, "wb") as f:
            f.write(await file.read())

        await files_collection.update_one(
            {
                "_id": db_file.inserted_id
            },
            {
                "$set": {
                    "status": FileStatus.QUEUED
                }
            }
        )

        q.enqueue(
            process_file,
            file_id,
            str(file_path),
        )

        return {
            "success": True,
            "file_id": file_id,
            "filename": file.filename,
            "status": FileStatus.QUEUED,
            "message": "Document uploaded successfully and queued for processing."
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# =====================================================
# AI Knowledge Assistant
# =====================================================

@app.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(request: ChatRequest):

    service = KnowledgeService()

    return await service.ask(
        file_id=request.file_id,
        question=request.question,
    )


# =====================================================
# Debug APIs
# =====================================================

@app.get("/files")
async def get_all_files():

    result = []

    async for doc in files_collection.find():

        doc["_id"] = str(doc["_id"])

        if "embedding" in doc:
            doc["embedding_dimension"] = len(doc["embedding"])
            del doc["embedding"]

        result.append(doc)

    return jsonable_encoder(result)


@app.get("/files/{file_id}")
async def get_file(file_id: str):

    doc = await files_collection.find_one(
        {
            "_id": ObjectId(file_id)
        }
    )

    if doc is None:

        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    doc["_id"] = str(doc["_id"])

    if "embedding" in doc:
        doc["embedding_dimension"] = len(doc["embedding"])
        del doc["embedding"]

    return jsonable_encoder(doc)


@app.get("/status/{file_id}")
async def get_status(file_id: str):

    doc = await files_collection.find_one(
        {
            "_id": ObjectId(file_id)
        }
    )

    if doc is None:

        raise HTTPException(
            status_code=404,
            detail="File not found",
        )

    return {
        "file_id": file_id,
        "status": doc["status"],
    }