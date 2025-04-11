"""
Flask web application for Star College Chatbot
"""
import os
import ssl
import certifi
import httpx
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS

from starbot.data.ingestion import DataIngestion
from starbot.models.config import ModelConfig
from starbot.models.retrieval import RetrievalQA

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

def initialize_starbot():
    """Initialize StarBot components"""
    global data_ingestion, qa_system, initialized
    
    if not initialized:
        # Initialize components
        data_ingestion = DataIngestion()
        model_config = ModelConfig()
        
        # Load data from Star College Durban website
        print("Ingesting data from Star College Durban website...")
        docs = data_ingestion.ingest_website('https://starcollegedurban.co.za/')
        print(f"Ingested {len(docs)} document chunks")
        
        # Create vector store
        vector_store = data_ingestion.create_vector_store(docs, 'star-college')
        print("Vector store created successfully")
        
        # Initialize QA system
        qa_system = RetrievalQA(
            vector_store=vector_store, 
            llm=model_config.get_llm(streaming=False)
        )
        print("QA system initialized")
        
        initialized = True

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
        return jsonify({"message": "StarBot initialized successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        
        # Get answer from StarBot
        answer = qa_system.answer_question(question)
        
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    os.makedirs('static', exist_ok=True)
    app.run(host='0.0.0.0', port=8000, debug=True)
