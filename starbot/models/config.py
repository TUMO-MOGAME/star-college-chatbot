"""
Model configuration for StarBot
"""
import os
import ssl
import certifi
import httpx
from typing import List, Dict, Any, Optional
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Set SSL certificate environment variable
os.environ['SSL_CERT_FILE'] = certifi.where()

# Create a custom SSL context
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

# Configure httpx client with SSL context
httpx_client = httpx.Client(verify=certifi.where())

class ModelConfig:
    """
    Configuration for LLM models used in StarBot
    """
    def __init__(self,
                llm_model: str = "mistral",
                embedding_model: str = "nomic-embed-text",
                streaming: bool = True):
        """
        Initialize model configuration

        Args:
            llm_model: Name of the Ollama LLM model to use
            embedding_model: Name of the Ollama embedding model to use
            streaming: Whether to enable streaming responses
        """
        self.llm_model = llm_model
        self.embedding_model = embedding_model
        self.streaming = streaming

    def get_llm(self, streaming: Optional[bool] = None) -> ChatOllama:
        """
        Get the configured LLM

        Args:
            streaming: Override the default streaming setting

        Returns:
            Configured ChatOllama model
        """
        use_streaming = self.streaming if streaming is None else streaming

        if use_streaming:
            return ChatOllama(
                model=self.llm_model,
                streaming=True,
                callbacks=[StreamingStdOutCallbackHandler()]
            )
        else:
            return ChatOllama(
                model=self.llm_model,
                streaming=False
            )

    def get_embeddings(self) -> OllamaEmbeddings:
        """
        Get the configured embeddings model

        Returns:
            Configured OllamaEmbeddings model
        """
        return OllamaEmbeddings(model=self.embedding_model)

    @staticmethod
    def list_available_models() -> List[str]:
        """
        List available Ollama models

        Returns:
            List of available model names
        """
        try:
            import ollama
            models = ollama.list()
            return [model['name'] for model in models['models']]
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
