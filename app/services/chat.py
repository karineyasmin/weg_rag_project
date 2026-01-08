from providers.vector_store import VectorStoreProvider
from providers.llm import LLMManager
from utils import setup_custom_logger
import os

logger = setup_custom_logger(__name__)


class ChatService:
    """
    Service responsible for retrieving context and generating answers using RAG.
    """

    def __init__(self, vector_store: VectorStoreProvider, llm_manager: LLMManager):
        """
        Initializse the ChatService with required providers.
        """

        self.vector_store = vector_store
        self.llm_manager = llm_manager

    async def answer_question(self, question: str) -> dict:
        """
        Orchestrates the RAG flow: Retrieval -> Argumentation -> Generation.

        Args:
            question (str): The user's question.

        Returns:
            dict: Containing the LLm answer and the source references.
        """
        logger.info(f"Retrieving context for question: {question}")
        relevant_docs = self.vector_store.search(query=question, k=3)

        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])
        references = []
        for doc in relevant_docs:
            full_path = doc.metadata.get("source", "Manual")
            source_name = os.path.basename(full_path)
            page_number = doc.metadata.get("page", "N/A")
            ref_string = f"Source: {source_name} (Page {page_number})"
            references.append(ref_string)

        logger.info("Generating response from LLM.")
        answer = self.llm_manager.ask(prompt=question, context=context_text)

        return {"answer": answer, "references": references}
