"""
Simple API backend for StarBot
"""
import os
import ssl
import certifi
import httpx
from flask import Flask, request, jsonify
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
print("Initializing StarBot...")
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
print("StarBot is ready!")

@app.route('/ask', methods=['POST'])
def ask():
    """Answer a question"""
    try:
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
    # Install flask-cors if not already installed
    try:
        import flask_cors
    except ImportError:
        print("Installing flask-cors...")
        os.system("pip install flask-cors")
        print("flask-cors installed successfully")
    
    print("Starting StarBot API server...")
    app.run(debug=True)
