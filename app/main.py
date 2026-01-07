from fastapi import FastAPI
from api import router as api_router
from utils import setup_custom_logger

logger = setup_custom_logger("main")

app = FastAPI(
    title="RAG Challenge - WEG Manuals",
    description="API for indexing technical documents and answering questions using RAG.",
    version="1.0.0",
)


app.include_router(api_router)


@app.get("/")
async def root():
    """
    Root endpoint to verify if the API is running.
    """

    return {"status": "online", "message": "RAG API is up and running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
