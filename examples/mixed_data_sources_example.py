"""
Example script demonstrating how to use multiple data sources including images with StarBot
"""
import os
import sys
import argparse

# Add the parent directory to the path so we can import the starbot package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from starbot.data.ingestion import DataIngestion
from starbot.models.config import ModelConfig
from starbot.models.retrieval import RetrievalQA

def main():
    """
    Main function to demonstrate using multiple data sources including images
    """
    parser = argparse.ArgumentParser(description="Use multiple data sources including images with StarBot")
    parser.add_argument("--url", type=str, help="URL to scrape")
    parser.add_argument("--text", type=str, help="Path to a text file")
    parser.add_argument("--pdf", type=str, help="Path to a PDF file")
    parser.add_argument("--image", type=str, help="Path to an image file")
    parser.add_argument("--language", type=str, default="eng", help="Language for OCR (default: eng)")
    args = parser.parse_args()
    
    if not any([args.url, args.text, args.pdf, args.image]):
        parser.error("At least one data source must be provided")
    
    # Initialize components
    print("Initializing StarBot...")
    data_ingestion = DataIngestion()
    model_config = ModelConfig()
    
    # Prepare data sources
    urls = [args.url] if args.url else None
    text_files = [args.text] if args.text else None
    pdf_files = [args.pdf] if args.pdf else None
    image_files = [args.image] if args.image else None
    
    # Load data from multiple sources
    print("Ingesting data from multiple sources...")
    all_documents = data_ingestion.ingest_multiple_sources(
        text_files=text_files,
        pdf_files=pdf_files,
        image_files=image_files,
        urls=urls
    )
    
    print(f"Ingested {len(all_documents)} document chunks")
    
    if not all_documents:
        print("No documents were ingested. Exiting.")
        return
    
    # Create vector store
    print("\nCreating vector store...")
    vector_store = data_ingestion.create_vector_store(all_documents, 'mixed-data')
    print("Vector store created successfully")
    
    # Initialize QA system
    qa_system = RetrievalQA(
        vector_store=vector_store, 
        llm=model_config.get_llm(streaming=False)
    )
    print("QA system initialized")
    
    # Interactive Q&A loop
    print("\nYou can now ask questions about the ingested data.")
    print("Type 'exit' to quit.")
    
    while True:
        question = input("\nQuestion: ")
        if question.lower() in ['exit', 'quit', 'q']:
            break
        
        answer = qa_system.ask(question)
        print(f"\nAnswer: {answer}")

if __name__ == "__main__":
    main()
