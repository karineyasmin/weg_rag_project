from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from utils import setup_custom_logger

logger = setup_custom_logger(__name__)


class DocumentLoader:
    """
    Provider responsible for extracting content from PDF files.
    """

    def __init__(self) -> None:
        """
        Initializes the DocumentLoader.
        """
        pass

    def load_pdf(self, file_path: str) -> list[Document]:
        """
        Reads a PDF file and returns a list of Documents with text and metadata.

        Args:
            file_path (str): The local path to the PDF file.

        Returns:
            list[Document]: A list of extracted documents (one per page).
        """

        try:
            logger.info(f"Loading PDF from {file_path}")
            loader = PyPDFLoader(file_path)
            docs = loader.load()
            logger.info(f"Successfully extracted {len(docs)} pages.")
            return docs
        except Exception as e:
            logger.error(f"Failed to load PDF {file_path}: {str(e)}")
            raise e
