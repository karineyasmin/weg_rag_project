from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.logger import setup_custom_logger
from models.schemas import DocumentResponse, QuestionResponse, QuestionRequest

logger = setup_custom_logger(__name__)
router = APIRouter()


@router.post("/documents", response_model=DocumentResponse)
async def upload_documents(files: list[UploadFile] = File(...)):
    """
    Endpoint to upload and index PDF documents.
    """
    logger.info(f"POST /documents called with {len(files)} files")

    # service logic

    return DocumentResponse(
        message="Documents processed successfully",
        documents_indexed=len(files),
        total_chunks=0,
    )


@router.post("/question", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Endpoint to retrieve context and answer questions using an LLM.
    """

    logger.info(f"POST /question called with: {request.question}")

    # service logic

    return QuestionResponse(answer="Implementation pending RAG logic.", references=[])
