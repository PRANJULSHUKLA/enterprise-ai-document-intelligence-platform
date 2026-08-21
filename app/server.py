from pathlib import Path

from bson import ObjectId
from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from app.constants.status import FileStatus

from app.schemas.file import FileSchema
from app.schemas.requests import (
    ChatRequest,
    AnalysisRequest,
    WorkflowRequest,
)

from app.schemas.responses import ChatResponse

from app.services.document_analysis import (
    DocumentAnalysisService,
)

from app.services.workflow_service import (
    WorkflowService,
)

from app.services.knowledge_service import (
    KnowledgeService,
)

from app.db.collections.files import files_collection

from app.queue.q import q
from app.queue.workers import process_file


# =====================================================
# FastAPI Application
# =====================================================

app = FastAPI(
    title="Enterprise AI Document Intelligence Platform",
    version="1.0.0",
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https://.*\.app\.github\.dev",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# =====================================================
# Health Check
# =====================================================

@app.get("/")
async def health():

    return {
        "status": "healthy",
        "service": "DocMind AI",
        "version": "1.0.0",
    }


# =====================================================
# Upload Document
# =====================================================

@app.post("/upload")
async def upload(
    file: UploadFile,
):

    try:

        if not file.filename:

            raise HTTPException(
                status_code=400,
                detail="No filename provided.",
            )

        document = FileSchema(
            filename=file.filename,
            status=FileStatus.SAVING,
        )

        db_file = await files_collection.insert_one(
            document.model_dump()
        )

        file_id = str(
            db_file.inserted_id
        )

        upload_dir = (
            Path("/mnt/uploads")
            / file_id
        )

        upload_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = (
            upload_dir
            / file.filename
        )

        file_bytes = await file.read()

        with open(
            file_path,
            "wb",
        ) as f:

            f.write(file_bytes)

        await files_collection.update_one(
            {
                "_id": db_file.inserted_id
            },
            {
                "$set": {
                    "status": FileStatus.QUEUED
                }
            },
        )

        q.enqueue(
            process_file,
            file_id,
            str(file_path),
            job_timeout=1200,
        )

        return {
            "success": True,
            "file_id": file_id,
            "filename": file.filename,
            "status": FileStatus.QUEUED,
            "message": (
                "Document uploaded successfully "
                "and queued for processing."
            ),
        }

    except HTTPException:

        raise

    except Exception as e:

        print(
            f"Upload failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# =====================================================
# AI Knowledge Assistant — Agent 1
# =====================================================

@app.post(
    "/chat",
    response_model=ChatResponse,
)
async def chat(
    request: ChatRequest,
):

    try:

        service = KnowledgeService()

        return await service.ask(
            file_id=request.file_id,
            question=request.question,
        )

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except RuntimeError as e:

        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    except Exception as e:

        print(
            f"Chat failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Unable to answer the question.",
        )


# =====================================================
# Document Intelligence — Agent 2
# =====================================================

@app.post("/analyze")
async def analyze_document(
    request: AnalysisRequest,
):

    try:

        service = DocumentAnalysisService()

        result = await service.analyze(
            file_id=request.file_id,
            analysis_type=request.analysis_type,
        )

        return {
            "success": True,
            "file_id": request.file_id,
            "analysis": result.model_dump(),
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except RuntimeError as e:

        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    except Exception as e:

        print(
            f"Document analysis failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Document analysis failed.",
        )


# =====================================================
# Workflow / Action Agent — Agent 3
# =====================================================

@app.post("/workflow")
async def create_workflow(
    request: WorkflowRequest,
):

    try:

        service = WorkflowService()

        result = await service.create_plan(
            file_id=request.file_id,
            objective=request.objective,
        )

        return {
            "success": True,
            "file_id": request.file_id,
            "workflow": result.model_dump(),
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e),
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except RuntimeError as e:

        raise HTTPException(
            status_code=409,
            detail=str(e),
        )

    except Exception as e:

        print(
            f"Workflow generation failed: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail="Workflow generation failed.",
        )


# =====================================================
# Get All Documents
# =====================================================

@app.get("/files")
async def get_all_files():

    result = []

    async for doc in files_collection.find():

        doc["_id"] = str(
            doc["_id"]
        )

        if "embedding" in doc:

            doc["embedding_dimension"] = len(
                doc["embedding"]
            )

            del doc["embedding"]

        result.append(doc)

    return jsonable_encoder(
        result
    )


# =====================================================
# Get Single Document
# =====================================================

@app.get("/files/{file_id}")
async def get_file(
    file_id: str,
):

    try:

        object_id = ObjectId(
            file_id
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid file_id.",
        )

    doc = await files_collection.find_one(
        {
            "_id": object_id
        }
    )

    if doc is None:

        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    doc["_id"] = str(
        doc["_id"]
    )

    if "embedding" in doc:

        doc["embedding_dimension"] = len(
            doc["embedding"]
        )

        del doc["embedding"]

    return jsonable_encoder(
        doc
    )


# =====================================================
# Document Processing Status
# =====================================================

@app.get("/status/{file_id}")
async def get_status(
    file_id: str,
):

    try:

        object_id = ObjectId(
            file_id
        )

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Invalid file_id.",
        )

    doc = await files_collection.find_one(
        {
            "_id": object_id
        }
    )

    if doc is None:

        raise HTTPException(
            status_code=404,
            detail="File not found.",
        )

    return {
        "file_id": file_id,
        "status": doc.get(
            "status",
            FileStatus.FAILED,
        ),
        "filename": doc.get(
            "filename"
        ),
        "total_pages": doc.get(
            "total_pages",
            0,
        ),
        "total_chunks": doc.get(
            "total_chunks",
            0,
        ),
        "processing_time": doc.get(
            "processing_time",
            0,
        ),
    }