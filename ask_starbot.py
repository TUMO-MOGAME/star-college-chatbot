"""
Ask StarBot a question from the command line
"""
import os
import ssl
import certifi
import httpx
import sys
from starbot.data.ingestion import DataIngestion
from starbot.models.config import ModelConfig
from starbot.models.retrieval import RetrievalQA

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python ask_starbot.py \"Your question here\"")
        return

    # Get the question from command-line arguments
    question = " ".join(sys.argv[1:])

    # Set SSL certificate environment variable
    os.environ['SSL_CERT_FILE'] = certifi.where()

    # Create a custom SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.load_verify_locations(certifi.where())

    # Configure httpx client with SSL context
    httpx_client = httpx.Client(verify=certifi.where())

    print("=" * 50)
    print("StarBot - A chatbot that answers questions about Star College Durban")
    print("=" * 50)

    # Initialize components
    print("\nInitializing StarBot...")
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

    # Ask the question
    print(f"\nQuestion: {question}")
    print("\nStarBot: ", end="")
    answer = qa_system.answer_question(question)
    print(answer)

if __name__ == "__main__":
    main()
