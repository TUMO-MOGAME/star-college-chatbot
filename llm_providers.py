"""
LLM Provider implementations for Star College Chatbot
"""
import os
import logging
from typing import Optional, Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BaseLLMProvider:
    """Base class for LLM providers"""

    def __init__(self):
        self.initialized = False

    def initialize(self) -> bool:
        """Initialize the LLM provider"""
        raise NotImplementedError

    def get_llm(self) -> Any:
        """Get the LLM instance"""
        raise NotImplementedError

    def answer_question(self, question: str, context: Optional[List[str]] = None) -> str:
        """Answer a question using the LLM"""
        raise NotImplementedError

class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider"""

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        super().__init__()
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
        self.client = None
        self.llm = None

    def initialize(self) -> bool:
        """Initialize the OpenAI provider"""
        try:
            if not self.api_key:
                logger.error("OpenAI API key not provided")
                return False

            # Import required modules
            try:
                from langchain_openai import ChatOpenAI
                from langchain.chains import LLMChain
                from langchain.prompts import PromptTemplate
                import openai

                # Set API key
                os.environ["OPENAI_API_KEY"] = self.api_key
                openai.api_key = self.api_key

                # Initialize client
                self.client = openai.OpenAI(api_key=self.api_key)

                # Initialize LLM
                self.llm = ChatOpenAI(
                    model=self.model,
                    temperature=0,
                    openai_api_key=self.api_key
                )

                self.initialized = True
                logger.info(f"OpenAI provider initialized with model {self.model}")
                return True

            except ImportError as e:
                logger.error(f"Could not import required modules for OpenAI: {e}")
                return False

        except Exception as e:
            logger.error(f"Error initializing OpenAI provider: {e}")
            return False

    def get_llm(self) -> Any:
        """Get the OpenAI LLM instance"""
        if not self.initialized:
            self.initialize()
        return self.llm

    def answer_question(self, question: str, context: Optional[List[str]] = None) -> str:
        """Answer a question using OpenAI"""
        if not self.initialized:
            success = self.initialize()
            if not success:
                return "I'm sorry, I couldn't initialize the language model. Please try again later."

        try:
            # Prepare context
            context_text = "\n".join(context) if context else "No additional context provided."

            # Create prompt
            prompt = f"""
            You are StarBot, a helpful assistant for Star College Durban.

            Use ONLY the following context to answer the question. If the answer is not in the context, say "I don't have enough information to answer that question."

            Context:
            {context_text}

            Question: {question}

            Answer:
            """

            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are StarBot, a helpful assistant for Star College Durban. Only answer based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=500
            )

            # Extract answer
            answer = response.choices[0].message.content.strip()
            return answer

        except Exception as e:
            logger.error(f"Error answering question with OpenAI: {e}")
            return f"I'm sorry, I encountered an error while processing your question: {str(e)}"

class OllamaProvider(BaseLLMProvider):
    """Ollama LLM provider"""

    def __init__(self, model: str = "llama2"):
        super().__init__()
        self.model = model
        self.llm = None

    def initialize(self) -> bool:
        """Initialize the Ollama provider"""
        try:
            # Import required modules
            try:
                from langchain_community.llms import Ollama

                # Initialize LLM
                self.llm = Ollama(model=self.model)

                self.initialized = True
                logger.info(f"Ollama provider initialized with model {self.model}")
                return True

            except ImportError as e:
                logger.error(f"Could not import required modules for Ollama: {e}")
                return False

        except Exception as e:
            logger.error(f"Error initializing Ollama provider: {e}")
            return False

    def get_llm(self) -> Any:
        """Get the Ollama LLM instance"""
        if not self.initialized:
            self.initialize()
        return self.llm

    def answer_question(self, question: str, context: Optional[List[str]] = None) -> str:
        """Answer a question using Ollama"""
        if not self.initialized:
            success = self.initialize()
            if not success:
                return "I'm sorry, I couldn't initialize the language model. Please try again later."

        try:
            # Prepare context
            context_text = "\n".join(context) if context else "No additional context provided."

            # Create prompt
            prompt = f"""
            You are StarBot, a helpful assistant for Star College Durban.

            Use ONLY the following context to answer the question. If the answer is not in the context, say "I don't have enough information to answer that question."

            Context:
            {context_text}

            Question: {question}

            Answer:
            """

            # Get response from Ollama
            answer = self.llm.invoke(prompt).strip()
            return answer

        except Exception as e:
            logger.error(f"Error answering question with Ollama: {e}")
            return f"I'm sorry, I encountered an error while processing your question: {str(e)}"

class MockProvider(BaseLLMProvider):
    """Mock LLM provider using pre-defined answers"""

    def __init__(self):
        super().__init__()
        self.initialized = True
        self.answers = {
            "what is star college durban": "Star College Durban is an Independent, English Medium School established by Horizon Educational Trust. It follows the curriculum from the Department of Education and aims to be academically strong, producing excellent results in the National Matric exams as well as National and International Mathematics, Science and Computer Olympiads.",
            "what is the mission of star college": "The mission of Star College is to enable all students to become the best possible version of themselves. They provide an environment where children develop into empathetic, self-directed, critical thinkers who do not give up when faced with challenges. Additionally, they aim to be academically strong and produce excellent results in various national and international exams and competitions.",
            "where is star college located": "Star College Durban is located at 20 Kinloch Avenue, Westville North 3630, Durban, South Africa.",
            "how can i contact star college": "You can contact Star College Durban via their phone number which is +27 31 262 71 91 or through email at starcollege@starcollege.co.za. They also have a presence on social media platforms such as Facebook, Instagram, Twitter, LinkedIn, and YouTube.",
            "what programs does star college offer": "Based on the available information, Star College offers education for primary school (Little Dolphin Star and Pre-Primary School), as well as separate high schools for boys and girls. They follow the curriculum from the Department of Education in South Africa.",
        }

    def initialize(self) -> bool:
        """Initialize the mock provider"""
        self.initialized = True
        return True

    def get_llm(self) -> Any:
        """Get the mock LLM instance"""
        return None

    def answer_question(self, question: str, context: Optional[List[str]] = None) -> str:
        """Answer a question using pre-defined answers"""
        question_lower = question.lower()

        # Check for exact matches
        if question_lower in self.answers:
            return self.answers[question_lower]

        # Check for partial matches
        for key, value in self.answers.items():
            if question_lower in key or key in question_lower:
                return value

        # Default response
        return "I don't have enough information to answer that question."

class DeepSeekProvider(BaseLLMProvider):
    """DeepSeek LLM provider"""

    def __init__(self, api_key: Optional[str] = None, model: str = "deepseek-chat"):
        super().__init__()
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        self.model = model or os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
        self.client = None

    def initialize(self) -> bool:
        """Initialize the DeepSeek provider"""
        try:
            if not self.api_key:
                logger.error("DeepSeek API key not provided")
                return False

            # Import required modules
            try:
                import requests

                # Test the API key with a simple request
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                # Initialize as successful
                self.initialized = True
                logger.info(f"DeepSeek provider initialized with model {self.model}")
                return True

            except ImportError as e:
                logger.error(f"Could not import required modules for DeepSeek: {e}")
                return False

        except Exception as e:
            logger.error(f"Error initializing DeepSeek provider: {e}")
            return False

    def get_llm(self) -> Any:
        """Get the DeepSeek LLM instance"""
        if not self.initialized:
            self.initialize()
        return None

    def answer_question(self, question: str, context: Optional[List[str]] = None) -> str:
        """Answer a question using DeepSeek"""
        if not self.initialized:
            success = self.initialize()
            if not success:
                return "I'm sorry, I couldn't initialize the language model. Please try again later."

        try:
            import requests
            import json

            # Prepare context
            context_text = "\n".join(context) if context else "No additional context provided."

            # Create prompt
            prompt = f"""
            You are StarBot, a helpful assistant for Star College Durban.

            Use ONLY the following context to answer the question. If the answer is not in the context, say "I don't have enough information to answer that question."

            Context:
            {context_text}

            Question: {question}

            Answer:
            """

            # Prepare the API request
            url = "https://api.deepseek.com/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            data = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are StarBot, a helpful assistant for Star College Durban. Only answer based on the provided context."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0,
                "max_tokens": 500
            }

            # Make the API request
            response = requests.post(url, headers=headers, data=json.dumps(data))
            response.raise_for_status()

            # Parse the response
            result = response.json()
            answer = result.get("choices", [{}])[0].get("message", {}).get("content", "")

            return answer.strip()

        except Exception as e:
            logger.error(f"Error answering question with DeepSeek: {e}")
            return f"I'm sorry, I encountered an error while processing your question: {str(e)}"

def get_llm_provider(provider_type: str = None) -> BaseLLMProvider:
    """Get an LLM provider based on the specified type"""
    provider_type = provider_type or os.environ.get("LLM_PROVIDER", "mock")

    if provider_type.lower() == "openai":
        return OpenAIProvider()
    elif provider_type.lower() == "deepseek":
        return DeepSeekProvider()
    elif provider_type.lower() == "ollama":
        return OllamaProvider()
    else:
        return MockProvider()
