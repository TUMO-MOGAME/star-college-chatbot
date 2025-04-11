"""
Flask web application for Star College Chatbot
"""
import os
import ssl
import certifi
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set SSL certificate environment variable
os.environ['SSL_CERT_FILE'] = certifi.where()

# Create a custom SSL context
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
llm_provider = None
data_retriever = None
initialized = False
provider_type = None

def initialize_starbot():
    """Initialize StarBot components"""
    global llm_provider, data_retriever, initialized, provider_type

    if not initialized:
        try:
            # Log all environment variables for debugging (excluding sensitive values)
            logger.info("Server environment variables:")
            for key, value in os.environ.items():
                if key in ["OPENAI_API_KEY", "DEEPSEEK_API_KEY"]:
                    value_preview = value[:5] + "..." if value else "None"
                    logger.info(f"  {key}: {value_preview}")
                elif key.lower() in ["llm_provider", "deepseek_model", "openai_model", "port"]:
                    logger.info(f"  {key}: {value}")

            # Import the LLM provider and data retriever
            logger.info("Importing modules...")
            from llm_providers import get_llm_provider
            from data_retrieval import DataRetriever
            logger.info("Modules imported successfully")

            # Get the LLM provider type from environment variable or default to "mock"
            provider_type = os.environ.get("LLM_PROVIDER", "mock")
            logger.info(f"Selected provider type from environment: {provider_type}")

            # Initialize the LLM provider
            logger.info(f"Getting LLM provider for type: {provider_type}")
            llm_provider = get_llm_provider(provider_type)
            logger.info("Initializing LLM provider...")
            provider_initialized = llm_provider.initialize()

            if not provider_initialized:
                logger.warning("Could not initialize LLM provider, falling back to mock provider")
                llm_provider = get_llm_provider("mock")
                llm_provider.initialize()
                provider_type = "mock"

            # Initialize the data retriever
            logger.info("Initializing data retriever...")
            data_retriever = DataRetriever()
            data_retriever.initialize()

            logger.info(f"StarBot initialized with {provider_type} provider")
            initialized = True

        except Exception as e:
            logger.error(f"Error initializing StarBot: {e}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Import the mock provider as fallback
            from llm_providers import MockProvider
            llm_provider = MockProvider()
            initialized = True
            provider_type = "mock"

# Serve the static HTML file
@app.route('/')
def home():
    """Serve the HTML file"""
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)

@app.route('/initialize')
def initialize():
    """Initialize StarBot"""
    try:
        initialize_starbot()
        logger.info(f"StarBot initialized with {provider_type} provider")
        return jsonify({
            "message": f"StarBot initialized successfully with {provider_type} provider",
            "mode": provider_type
        })
    except Exception as e:
        logger.error(f"Error during initialization: {e}")
        return jsonify({"error": str(e), "mode": "error"}), 500

@app.route('/ask', methods=['POST'])
def ask():
    """Answer a question"""
    try:
        # Initialize if not already initialized
        if not initialized:
            initialize_starbot()

        # Get question from request
        data = request.json
        question = data.get('question', '')

        if not question:
            return jsonify({"error": "No question provided"}), 400

        # Get relevant context from data retriever
        context = data_retriever.search(question) if data_retriever else []

        # Get answer from LLM provider
        logger.info(f"Using {provider_type} provider for question: {question}")
        answer = llm_provider.answer_question(question, context)

        return jsonify({
            "answer": answer,
            "mode": provider_type
        })
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        return jsonify({
            "error": str(e),
            "answer": "Sorry, I encountered an error while processing your question. Please try again.",
            "mode": "error"
        }), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=8000, debug=True)
