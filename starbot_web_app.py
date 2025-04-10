"""
Flask web application for StarBot
"""
import os
import ssl
import certifi
import httpx
from flask import Flask, render_template, request, jsonify
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

@app.route('/')
def home():
    """Render home page"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>StarBot - Star College Durban Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1 {
                color: #1E88E5;
                text-align: center;
                margin-bottom: 10px;
            }
            .subtitle {
                color: #424242;
                text-align: center;
                margin-bottom: 30px;
            }
            .chat-container {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 20px;
                height: 400px;
                overflow-y: auto;
                margin-bottom: 20px;
                background-color: white;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .user-message {
                background-color: #E3F2FD;
                padding: 10px 15px;
                border-radius: 18px;
                margin-bottom: 15px;
                max-width: 80%;
                margin-left: auto;
                margin-right: 10px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            .bot-message {
                background-color: #F5F5F5;
                padding: 10px 15px;
                border-radius: 18px;
                margin-bottom: 15px;
                max-width: 80%;
                margin-right: auto;
                margin-left: 10px;
                box-shadow: 0 1px 2px rgba(0,0,0,0.1);
            }
            .input-container {
                display: flex;
                margin-bottom: 20px;
            }
            #user-input {
                flex-grow: 1;
                padding: 12px 15px;
                border: 1px solid #ddd;
                border-radius: 25px;
                font-size: 16px;
                outline: none;
                transition: border-color 0.3s;
            }
            #user-input:focus {
                border-color: #1E88E5;
            }
            #send-button {
                padding: 12px 20px;
                background-color: #1E88E5;
                color: white;
                border: none;
                border-radius: 25px;
                margin-left: 10px;
                cursor: pointer;
                font-weight: bold;
                transition: background-color 0.3s;
            }
            #send-button:hover {
                background-color: #1976D2;
            }
            .loading {
                text-align: center;
                margin: 20px 0;
                color: #666;
            }
            .loading-dots {
                display: inline-block;
            }
            .loading-dots:after {
                content: '.';
                animation: dots 1.5s steps(5, end) infinite;
            }
            @keyframes dots {
                0%, 20% { content: '.'; }
                40% { content: '..'; }
                60% { content: '...'; }
                80%, 100% { content: ''; }
            }
            .about {
                margin-top: 30px;
                padding: 20px;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            .about h3 {
                color: #1E88E5;
                margin-top: 0;
            }
            .footer {
                text-align: center;
                margin-top: 30px;
                color: #666;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <h1>🤖 StarBot</h1>
        <p class="subtitle">A chatbot that answers questions about Star College Durban</p>
        
        <div class="chat-container" id="chat-container">
            <div class="bot-message">
                <strong>StarBot:</strong> Hello! I'm StarBot. I can answer questions about Star College Durban. What would you like to know?
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="user-input" placeholder="Ask a question about Star College Durban...">
            <button id="send-button">Send</button>
        </div>
        
        <div id="loading" class="loading" style="display: none;">
            <p>StarBot is thinking<span class="loading-dots"></span></p>
        </div>
        
        <div class="about">
            <h3>About StarBot</h3>
            <p><strong>StarBot</strong> is a chatbot that answers questions about Star College Durban using information from their website.</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Uses free LLM models via Ollama</li>
                <li>Answers questions based only on provided data</li>
                <li>Responds with "I don't have enough information" when the answer isn't in the data</li>
            </ul>
            <p><strong>Sample questions you can ask:</strong></p>
            <ul>
                <li>What is Star College Durban?</li>
                <li>What is the mission of Star College?</li>
                <li>Where is Star College located?</li>
                <li>How can I contact Star College?</li>
            </ul>
        </div>
        
        <div class="footer">
            Powered by Ollama, LangChain, and Flask
        </div>
        
        <script>
            // Function to add a message to the chat
            function addMessage(message, isUser) {
                const chatContainer = document.getElementById('chat-container');
                const messageDiv = document.createElement('div');
                messageDiv.className = isUser ? 'user-message' : 'bot-message';
                messageDiv.innerHTML = `<strong>${isUser ? 'You' : 'StarBot'}:</strong> ${message}`;
                chatContainer.appendChild(messageDiv);
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            
            // Function to send a message
            function sendMessage() {
                const userInput = document.getElementById('user-input');
                const message = userInput.value.trim();
                
                if (message) {
                    // Add user message to chat
                    addMessage(message, true);
                    
                    // Clear input
                    userInput.value = '';
                    
                    // Show loading indicator
                    document.getElementById('loading').style.display = 'block';
                    
                    // Send message to server
                    fetch('/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ question: message }),
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Hide loading indicator
                        document.getElementById('loading').style.display = 'none';
                        
                        // Add bot response to chat
                        addMessage(data.answer, false);
                    })
                    .catch(error => {
                        // Hide loading indicator
                        document.getElementById('loading').style.display = 'none';
                        
                        // Add error message to chat
                        addMessage('Sorry, there was an error processing your request.', false);
                        console.error('Error:', error);
                    });
                }
            }
            
            // Event listeners
            document.getElementById('send-button').addEventListener('click', sendMessage);
            document.getElementById('user-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    '''

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
    # Run the Flask app
    print("Starting web server at http://127.0.0.1:5000")
    app.run(debug=True)
