"""
Flask web application for Star College Chatbot
"""
import os
import ssl
import certifi
import httpx
import logging
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set SSL certificate environment variable
os.environ['SSL_CERT_FILE'] = certifi.where()

# Create a custom SSL context
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

# Configure httpx client with SSL context
httpx_client = httpx.Client(verify=certifi.where())

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize components
data_ingestion = None
qa_system = None
initialized = False
use_mock_data = False

# Pre-defined answers for fallback mode
MOCK_ANSWERS = {
    "what is star college durban": "Star College Durban is an Independent, English Medium School established by Horizon Educational Trust. It follows the curriculum from the Department of Education and aims to be academically strong, producing excellent results in the National Matric exams as well as National and International Mathematics, Science and Computer Olympiads.",
    "what is the mission of star college": "The mission of Star College is to enable all students to become the best possible version of themselves. They provide an environment where children develop into empathetic, self-directed, critical thinkers who do not give up when faced with challenges. Additionally, they aim to be academically strong and produce excellent results in various national and international exams and competitions.",
    "where is star college located": "Star College Durban is located at 20 Kinloch Avenue, Westville North 3630, Durban, South Africa.",
    "how can i contact star college": "You can contact Star College Durban via their phone number which is +27 31 262 71 91 or through email at starcollege@starcollege.co.za. They also have a presence on social media platforms such as Facebook, Instagram, Twitter, LinkedIn, and YouTube.",
    "what programs does star college offer": "Based on the available information, Star College offers education for primary school (Little Dolphin Star and Pre-Primary School), as well as separate high schools for boys and girls. They follow the curriculum from the Department of Education in South Africa.",
}

def initialize_starbot():
    """Initialize StarBot components"""
    global data_ingestion, qa_system, initialized, use_mock_data

    if not initialized:
        try:
            # Try to import required modules
            try:
                from starbot.data.ingestion import DataIngestion
                from starbot.models.config import ModelConfig
                from starbot.models.retrieval import RetrievalQA

                # Initialize components
                data_ingestion = DataIngestion()
                model_config = ModelConfig()

                # Load data from Star College Durban website
                logger.info("Ingesting data from Star College Durban website...")
                docs = data_ingestion.ingest_website('https://starcollegedurban.co.za/')
                logger.info(f"Ingested {len(docs)} document chunks")

                # Create vector store
                vector_store = data_ingestion.create_vector_store(docs, 'star-college')
                logger.info("Vector store created successfully")

                # Initialize QA system
                qa_system = RetrievalQA(
                    vector_store=vector_store,
                    llm=model_config.get_llm(streaming=False)
                )
                logger.info("QA system initialized")

                initialized = True
                use_mock_data = False

            except (ImportError, ModuleNotFoundError) as e:
                logger.warning(f"Could not import required modules: {e}")
                logger.warning("Falling back to mock data mode")
                initialized = True
                use_mock_data = True

        except Exception as e:
            logger.error(f"Error initializing StarBot: {e}")
            initialized = True
            use_mock_data = True

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
        mode = "mock data" if use_mock_data else "full QA system"
        logger.info(f"StarBot initialized in {mode} mode")
        return jsonify({
            "message": f"StarBot initialized successfully in {mode} mode",
            "mode": "mock" if use_mock_data else "full"
        })
    except Exception as e:
        logger.error(f"Error during initialization: {e}")
        return jsonify({"error": str(e), "mode": "error"}), 500

@app.route('/ask', methods=['POST'])
def ask():
    """Answer a question"""
    try:
        # Initialize if not already initialized
        initialize_starbot()

        # Get question from request
        data = request.json
        question = data.get('question', '')

        if not question:
            return jsonify({"error": "No question provided"}), 400

        # Check if we're using mock data
        if use_mock_data:
            logger.info(f"Using mock data for question: {question}")
            question_lower = question.lower()
            answer = "I don't have enough information to answer that question."

            # Check for exact matches
            if question_lower in MOCK_ANSWERS:
                answer = MOCK_ANSWERS[question_lower]
            else:
                # Check for partial matches
                for key in MOCK_ANSWERS:
                    if question_lower in key or key in question_lower:
                        answer = MOCK_ANSWERS[key]
                        break
        else:
            # Get answer from StarBot
            logger.info(f"Using QA system for question: {question}")
            answer = qa_system.answer_question(question)

        return jsonify({"answer": answer})
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        return jsonify({"error": str(e), "answer": "Sorry, I encountered an error while processing your question. Please try again."}), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=8000, debug=True)
