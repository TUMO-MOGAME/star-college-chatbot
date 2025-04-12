"""
Example script demonstrating how to extract text from images using StarBot
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
    Main function to demonstrate image text extraction
    """
    parser = argparse.ArgumentParser(description="Extract text from images and answer questions")
    parser.add_argument("--image", type=str, help="Path to an image file")
    parser.add_argument("--image_dir", type=str, help="Path to a directory of images")
    parser.add_argument("--language", type=str, default="eng", help="Language for OCR (default: eng)")
    args = parser.parse_args()
    
    if not args.image and not args.image_dir:
        parser.error("At least one of --image or --image_dir must be provided")
    
    # Initialize components
    print("Initializing StarBot...")
    data_ingestion = DataIngestion()
    model_config = ModelConfig()
    
    # Load data from images
    all_documents = []
    
    if args.image:
        print(f"Extracting text from image: {args.image}")
        try:
            docs = data_ingestion.ingest_image(args.image, language=args.language)
            print(f"Extracted {len(docs)} document chunks")
            all_documents.extend(docs)
        except Exception as e:
            print(f"Error processing image {args.image}: {str(e)}")
    
    if args.image_dir:
        print(f"Extracting text from images in directory: {args.image_dir}")
        try:
            docs = data_ingestion.ingest_image_directory(args.image_dir, language=args.language)
            print(f"Extracted {len(docs)} document chunks from directory")
            all_documents.extend(docs)
        except Exception as e:
            print(f"Error processing image directory {args.image_dir}: {str(e)}")
    
    if not all_documents:
        print("No documents were extracted. Exiting.")
        return
    
    # Display extracted text
    print("\nExtracted Text:")
    print("=" * 50)
    for i, doc in enumerate(all_documents):
        print(f"Document {i+1}:")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Content: {doc.page_content[:200]}...")  # Show first 200 chars
        print("-" * 50)
    
    # Create vector store
    print("\nCreating vector store...")
    vector_store = data_ingestion.create_vector_store(all_documents, 'image-data')
    print("Vector store created successfully")
    
    # Initialize QA system
    qa_system = RetrievalQA(
        vector_store=vector_store, 
        llm=model_config.get_llm(streaming=False)
    )
    print("QA system initialized")
    
    # Interactive Q&A loop
    print("\nYou can now ask questions about the extracted text.")
    print("Type 'exit' to quit.")
    
    while True:
        question = input("\nQuestion: ")
        if question.lower() in ['exit', 'quit', 'q']:
            break
        
        answer = qa_system.ask(question)
        print(f"\nAnswer: {answer}")

if __name__ == "__main__":
    main()
