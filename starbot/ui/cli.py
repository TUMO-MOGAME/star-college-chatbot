"""
Command-line interface for StarBot
"""
import os
import argparse
from typing import List, Optional

from starbot.data.ingestion import DataIngestion
from starbot.models.config import ModelConfig
from starbot.models.retrieval import RetrievalQA

class StarBotCLI:
    """
    Command-line interface for StarBot
    """
    def __init__(self):
        """
        Initialize the CLI
        """
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        self.model_config = ModelConfig()
        self.data_ingestion = DataIngestion()
        self.vector_store = None
        self.qa_system = None
        
    def ingest_data(self, 
                   text_files: Optional[List[str]] = None,
                   pdf_files: Optional[List[str]] = None,
                   urls: Optional[List[str]] = None,
                   directories: Optional[List[str]] = None,
                   collection_name: str = "starbot-data"):
        """
        Ingest data from various sources
        
        Args:
            text_files: List of text file paths
            pdf_files: List of PDF file paths
            urls: List of website URLs
            directories: List of directory paths
            collection_name: Name of the collection in the vector store
        """
        print("Ingesting data...")
        documents = self.data_ingestion.ingest_multiple_sources(
            text_files=text_files,
            pdf_files=pdf_files,
            urls=urls,
            directories=directories
        )
        
        print(f"Ingested {len(documents)} document chunks")
        
        print("Creating vector store...")
        self.vector_store = self.data_ingestion.create_vector_store(
            documents=documents,
            collection_name=collection_name
        )
        
        print("Vector store created successfully")
        
        # Initialize the QA system
        self.qa_system = RetrievalQA(
            vector_store=self.vector_store,
            llm=self.model_config.get_llm()
        )
        
    def chat_loop(self):
        """
        Start an interactive chat loop
        """
        if not self.qa_system:
            print("Error: No data has been ingested. Please ingest data first.")
            return
        
        print("\nStarBot is ready! Type 'exit' to quit.")
        
        while True:
            user_input = input("\nYou: ")
            
            if user_input.lower() in ["exit", "quit", "q"]:
                break
                
            print("\nStarBot: ", end="")
            answer = self.qa_system.answer_question(user_input)
            print()  # Add a newline after the streaming response
            
    def run(self):
        """
        Run the CLI application
        """
        parser = argparse.ArgumentParser(description="StarBot - A chatbot that answers questions based on custom data")
        
        subparsers = parser.add_subparsers(dest="command", help="Command to run")
        
        # Ingest command
        ingest_parser = subparsers.add_parser("ingest", help="Ingest data")
        ingest_parser.add_argument("--text", nargs="+", help="Text files to ingest")
        ingest_parser.add_argument("--pdf", nargs="+", help="PDF files to ingest")
        ingest_parser.add_argument("--url", nargs="+", help="URLs to ingest")
        ingest_parser.add_argument("--dir", nargs="+", help="Directories to ingest")
        ingest_parser.add_argument("--collection", default="starbot-data", help="Collection name for the vector store")
        
        # Chat command
        chat_parser = subparsers.add_parser("chat", help="Start chat session")
        
        args = parser.parse_args()
        
        if args.command == "ingest":
            self.ingest_data(
                text_files=args.text,
                pdf_files=args.pdf,
                urls=args.url,
                directories=args.dir,
                collection_name=args.collection
            )
            
            # Start chat after ingestion
            self.chat_loop()
            
        elif args.command == "chat":
            # Try to load existing vector store
            try:
                from langchain_community.vectorstores import Chroma
                
                self.vector_store = Chroma(
                    collection_name="starbot-data",
                    embedding_function=self.model_config.get_embeddings()
                )
                
                self.qa_system = RetrievalQA(
                    vector_store=self.vector_store,
                    llm=self.model_config.get_llm()
                )
                
                self.chat_loop()
                
            except Exception as e:
                print(f"Error loading vector store: {e}")
                print("Please ingest data first using the 'ingest' command")
                
        else:
            parser.print_help()
