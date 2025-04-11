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
            "what is star college durban": "**About Star College Durban**\n\nStar College Durban is an Independent, English Medium School established by Horizon Educational Trust.\n\nThe school follows the curriculum from the Department of Education and focuses on academic excellence, particularly in:\n\n• Mathematics\n• Science\n• Computer Technology\n\nStar College aims to be academically strong, producing excellent results in the National Matric exams as well as National and International Mathematics, Science and Computer Olympiads.",

            "what is the mission of star college": "**Mission of Star College**\n\nThe mission of Star College is to enable all students to become the best possible version of themselves.\n\nThe school strives to create an environment where children develop into:\n\n• Empathetic individuals\n• Self-directed learners\n• Critical thinkers who persevere when faced with challenges\n\nAdditionally, they aim to be academically strong and produce excellent results in various national and international exams and competitions.",

            "where is star college located": "**Location**\n\nStar College Durban is located at:\n\n20 Kinloch Avenue\nWestville North 3630\nDurban, South Africa",

            "how can i contact star college": "**Contact Information**\n\nYou can reach Star College Durban through the following channels:\n\n**Phone Number:**\n+27 31 262 71 91\n\n**Email:**\nstarcollege@starcollege.co.za\n\n**Social Media:**\nThe school also maintains a presence on various platforms including Facebook, Instagram, Twitter, LinkedIn, and YouTube.",

            "what programs does star college offer": "**Educational Programs**\n\nStar College offers a comprehensive education system that includes:\n\n• **Primary Education:** Little Dolphin Star and Pre-Primary School\n• **Secondary Education:** Separate high schools for boys and girls\n\nAll programs follow the curriculum from the Department of Education in South Africa, providing students with a strong academic foundation.",
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
        return "**I don't have enough information**\n\nI'm sorry, but I don't have enough information in my database to answer that question about Star College Durban.\n\nFor more specific information, you might want to:\n\n• Visit the official Star College Durban website\n• Contact the school directly at +27 31 262 71 91\n• Email them at starcollege@starcollege.co.za"

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
            # Log the API key (first 5 chars only for security)
            api_key_preview = self.api_key[:5] + '...' if self.api_key else None
            logger.info(f"Attempting to initialize DeepSeek provider with API key starting with: {api_key_preview}")
            logger.info(f"Using model: {self.model}")

            if not self.api_key:
                logger.error("DeepSeek API key not provided")
                return False

            # Import required modules
            try:
                import requests
                logger.info("Successfully imported requests module")

                # Test the API key with a simple request
                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                # Make a simple test request to verify the API key
                try:
                    logger.info("Testing DeepSeek API connection...")
                    test_url = "https://api.deepseek.com/v1/models"
                    test_response = requests.get(test_url, headers=headers)

                    if test_response.status_code == 200:
                        logger.info("DeepSeek API connection successful!")
                    else:
                        logger.error(f"DeepSeek API test failed with status code: {test_response.status_code}")
                        logger.error(f"Response: {test_response.text}")
                        return False
                except Exception as e:
                    logger.error(f"Error testing DeepSeek API: {e}")
                    return False

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

            Format your answer in a readable, user-friendly style following these guidelines:
            1. Use proper paragraphs with line breaks between them
            2. Use bullet points for lists
            3. Use headers (with bold formatting) for different sections when appropriate
            4. Keep paragraphs short and focused on one idea
            5. Use a conversational, helpful tone
            6. Organize information logically
            7. Highlight important information

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

    # Log all environment variables for debugging (excluding sensitive values)
    logger.info("Environment variables:")
    for key, value in os.environ.items():
        if key in ["OPENAI_API_KEY", "DEEPSEEK_API_KEY"]:
            value_preview = value[:5] + "..." if value else "None"
            logger.info(f"  {key}: {value_preview}")
        elif key.lower() in ["llm_provider", "deepseek_model", "openai_model"]:
            logger.info(f"  {key}: {value}")

    logger.info(f"Selected provider type: {provider_type}")

    if provider_type.lower() == "openai":
        logger.info("Creating OpenAI provider")
        return OpenAIProvider()
    elif provider_type.lower() == "deepseek":
        logger.info("Creating DeepSeek provider")
        return DeepSeekProvider()
    elif provider_type.lower() == "ollama":
        logger.info("Creating Ollama provider")
        return OllamaProvider()
    else:
        logger.info(f"Creating Mock provider (unknown type: {provider_type})")
        return MockProvider()
