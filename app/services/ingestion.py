from langchain_text_splitters import RecursiveCharacterTextSplitter
from providers.document_loader import DocumentLoader
from providers.vector_store import VectorStoreProvider
from utils import setup_custom_logger

logger = setup_custom_logger(__name__)


class IngestionService:
    """
    Service responsible for the full ingestion pipeline: Load -> Split -> Embed -> Store.
    """

    def __init__(self, loader: DocumentLoader, vector_store: VectorStoreProvider):
        self.loader = loader
        self.vector_store = vector_store
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )

    async def process_pdf(self, file_path: str) -> int:
        """
        Processes a single PDF file and returns the number of chunks created.

        Args:
            file_path (str): Local path to the uploaded PDF.

        Returns:
            int: Total number of chunks indexed.
        """

        raw_docs = self.loader.load_pdf(file_path)

        chunks = self.splitter.split_documents(raw_docs)
        logger.info(f"Split document into {len(chunks)} chunks.")

        self.vector_store.add_documents(chunks)

        return len(chunks)
