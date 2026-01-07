from abc import ABC, abstractmethod
from langchain_ollama import OllamaLLM
from utils import setup_custom_logger

logger = setup_custom_logger(__name__)


class LLMProvider(ABC):
    """
    Abstract interface for Language Model providers.
    """

    @abstractmethod
    def generate_response(self, prompt: str, context: str) -> str:
        """
        Generates a response based on a prompt and retrieved context.
        """
        pass


class OllamaProvider(LLMProvider):
    """
    Ollama implementation for local LLM execution.
    """

    def __init__(self, model_name: str = "llama3"):
        """
        Initializes de Ollama client.
        """
        self.model = OllamaLLM(model=model_name, base_url="http://localhost:11434")

    def generate_response(self, prompt: str, context: str) -> str:
        """
        Invokes the local model using the provided context.
        """

        full_prompt = f"Context: {context}\n\nQuestion: {prompt}"
        return self.model.invoke(full_prompt)


class LLMManager:
    """
    Manages LLM providers and handles fallback logic.
    """

    def __init__(self, primary: LLMProvider, fallback: LLMProvider | None = None):
        self.primary = primary
        self.fallback = fallback

    def ask(self, prompt: str, context: str) -> str:
        """
        Tries primar provider; falls back to secondary if primary fails.
        """
        try:
            logger.info("Requesting response from primary LLM provider.")
            return self.primary.generate_response(prompt, context)
        except Exception as e:
            logger.warning(f"Primary provider failed: {e}")
            if self.fallback:
                logger.info("Starting fallback to secondary provider.")
                return self.fallback.generate_response(prompt, context)
            raise e
