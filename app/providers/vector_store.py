import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from utils import setup_custom_logger


logger = setup_custom_logger(__name__)


class VectorStoreProvider:
    """
    Provider for managing semantic search and document embeddings storage.
    """

    def __init__(self, persist_directory: str):
        """
        Initializes the Vector Store with HuggingFace embeddings.

        Args:
            persist_directory (str): Path where the vector database will be stored.
        """
        self.persist_directory = persist_directory

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.vector_db = None

    def add_documents(self, documents: list[Document]) -> None:
        """
        Generates embeddings and saves documents to the vector store.

        Args:
            documents (list[Document]): List of text chunk to be indexed.
        """
        logger.info(f"Indexing {len(documents)} chunks into ChromaDB")
        self.vector_db = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
        )
        logger.info("Indexing completed successfully.")

    def search(self, query: str, k: int = 3) -> list[Document]:
        """
        Performs a semantic search to find relevant chunks.

        Args:
            query (str): The user's question.
            k (int): Number of relevant chunks to retrieve,

        Returns:
            list[Document]: The most similar document chunks.
        """
        if not self.vector_db:
            self.vector_db = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
            )

        logger.info(f"Searching for: '{query}'")
        return self.vector_db.similarity_search(query, k=k)
