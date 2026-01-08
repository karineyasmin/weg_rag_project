import os
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.logger import setup_custom_logger
from models.schemas import DocumentResponse, QuestionResponse, QuestionRequest
from providers.document_loader import DocumentLoader
from providers.vector_store import VectorStoreProvider
from providers.llm import OllamaProvider, LLMManager, GeminiProvider
from services.ingestion import IngestionService
from services.chat import ChatService
from config import Config

logger = setup_custom_logger(__name__)
router = APIRouter()

VECTOR_STORE_PATH = Path(Config.VECTOR_STORE_PATH)
TEMP_UPLOAD_PATH = Path(Config.TEMP_UPLOAD_PATH)

VECTOR_STORE_PATH.mkdir(parents=True, exist_ok=True)
TEMP_UPLOAD_PATH.mkdir(parents=True, exist_ok=True)

loader = DocumentLoader()
vector_store = VectorStoreProvider(persist_directory=str(VECTOR_STORE_PATH))

ollama_fallback = OllamaProvider()
gemini_primary = GeminiProvider()

llm_manager = LLMManager(primary=gemini_primary, fallback=ollama_fallback)

ingestion_service = IngestionService(loader=loader, vector_store=vector_store)
chat_service = ChatService(vector_store=vector_store, llm_manager=llm_manager)


@router.post("/documents", response_model=DocumentResponse)
async def upload_documents(files: list[UploadFile] = File(...)):
    """
    Endpoint to upload and index PDF documents.

    Extracts text, creates chunk, and stores embeddings.

    Uses pathlib for cross-platform compatibility.
    """
    logger.info(f"POST /documents called with {len(files)} files")

    total_chunks = 0

    try:
        for file in files:
            file_path = TEMP_UPLOAD_PATH / file.filename

            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            chunks_count = await ingestion_service.process_pdf(str(file_path))
            total_chunks += chunks_count

            file_path.unlink(missing_ok=True)

        return DocumentResponse(
            message="Documents processed successfully",
            documents_indexed=len(files),
            total_chunks=total_chunks,
        )
    except Exception as e:
        logger.error(f"Error during document ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process documents.")


@router.post("/question", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Endpoint to retrieve context and answer questions using an LLM.
    """
    try:
        logger.info(f"POST /question called with: {request.question}")

        result = await chat_service.answer_question(request.question)

        return QuestionResponse(
            answer=result["answer"], references=result["references"]
        )
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        raise HTTPException(status_code=500, detail="Error generating answer.")
