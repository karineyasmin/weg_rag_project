from abc import ABC, abstractmethod
from langchain_ollama import OllamaLLM
from langchain_google_genai import ChatGoogleGenerativeAI
from utils import setup_custom_logger
from config import Config

logger = setup_custom_logger(__name__)

FULL_PROMPT = """
You are a technical specialist for WEG motor manuals. 
Answer the question strictly using the context provided below.

RULES:
1. Language: Answer in the EXACT SAME language as the question.
2. Source: Use ONLY the provided context. Do not use outside knowledge.
3. Format: Plain text only. No markdown, no bold, no symbols.
4. If the answer is NOT in the context, your response MUST BE EXACTLY: "Information not found."
5. Do not explain the rules. Do not use outside knowledge.
CONTEXT:
{context}

QUESTION:
{prompt}

FINAL ANSWER:
"""


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


class GeminiProvider(LLMProvider):
    """
    Gemini implementation using Google Generative AI Cloud API.
    """

    def __init__(self, model_name: str = Config.PRIMARY_MODEL):
        self.model_name = model_name
        self.api_key = Config.GEMINI_API_KEY
        self.model = None

    def generate_response(self, prompt: str, context: str) -> str:
        if not self.api_key:
            raise ValueError("Gemini API key is missing. Cannot initialize model.")

        if self.model is None:
            self.model = ChatGoogleGenerativeAI(
                model=self.model_name, google_api_key=self.api_key, temperature=0
            )

        formatted_prompt = FULL_PROMPT.format(context=context, prompt=prompt)

        response = self.model.invoke(formatted_prompt)
        return response.content


class OllamaProvider(LLMProvider):
    def __init__(self, model_name: str = Config.FALLBACK_MODEL):
        self.model_name = model_name
        self.model = OllamaLLM(model=model_name, base_url=Config.OLLAMA_URL)

    def generate_response(self, prompt: str, context: str) -> str:
        formatted_prompt = FULL_PROMPT.format(context=context, prompt=prompt)

        try:
            logger.info(f"Sending prompt to Ollama ({self.model_name})...")
            return self.model.invoke(formatted_prompt)
        except Exception as e:
            logger.error(f"Ollama execution error: {str(e)}")
            raise e


class LLMManager:
    """
    Manages LLM providers and handles fallback logic.
    """

    def __init__(self, primary: LLMProvider, fallback: LLMProvider | None = None):
        self.primary = primary
        self.fallback = fallback

    def ask(self, prompt: str, context: str) -> str:
        """
        Attempts to use the primary provider. If the API Key is missing
        or an error occurs, it switches to the fallback provider.
        """
        if isinstance(self.primary, GeminiProvider):
            if not Config.GEMINI_API_KEY or Config.GEMINI_API_KEY.strip() == "":
                logger.warning(
                    "Gemini API Key is missing. Tripping fallback to Ollama immediately."
                )
                return self._handle_fallback(prompt, context)
        try:
            logger.info(f"Attempting request with {type(self.primary).__name__}")
            return self.primary.generate_response(prompt, context)
        except Exception as e:
            logger.error(f"Primary provider encountered an error: {e}")
            return self._handle_fallback(prompt, context)

    def _handle_fallback(self, prompt: str, context: str) -> str:
        """
        Helper method to execute fallback logic.
        """
        if self.fallback:
            logger.info(
                f"Switching to fallback provider: {type(self.fallback).__name__}"
            )
            try:
                return self.fallback.generate_response(prompt, context)
            except Exception as e:
                logger.error(f"Fallback provider also failed: {e}")
                raise e
        raise ValueError("Primary provider failed and no fallback was configured.")
