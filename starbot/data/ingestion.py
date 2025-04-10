"""
Data ingestion module for StarBot
"""
import os
import ssl
import certifi
import httpx
from typing import List, Union, Optional
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import (
    TextLoader,
    DirectoryLoader,
    PyPDFLoader
)
from starbot.utils.web_loader import CustomWebLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings

# Set SSL certificate environment variable
os.environ['SSL_CERT_FILE'] = certifi.where()

# Create a custom SSL context
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

# Configure httpx client with SSL context
httpx_client = httpx.Client(verify=certifi.where())

class DataIngestion:
    """
    Handles ingestion of various data sources into the vector database
    """
    def __init__(self, embedding_model: str = "nomic-embed-text", chunk_size: int = 750, chunk_overlap: int = 100):
        """
        Initialize the data ingestion module

        Args:
            embedding_model: Name of the Ollama embedding model to use
            chunk_size: Size of text chunks for splitting documents
            chunk_overlap: Overlap between chunks
        """
        self.embedding_model = embedding_model
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
        self.embeddings = OllamaEmbeddings(model=self.embedding_model)

    def ingest_text_file(self, file_path: str) -> List:
        """
        Ingest a single text file

        Args:
            file_path: Path to the text file

        Returns:
            List of document chunks
        """
        loader = TextLoader(file_path)
        documents = loader.load()
        return self.text_splitter.split_documents(documents)

    def ingest_pdf_file(self, file_path: str) -> List:
        """
        Ingest a single PDF file

        Args:
            file_path: Path to the PDF file

        Returns:
            List of document chunks
        """
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        return self.text_splitter.split_documents(documents)

    def ingest_website(self, url: str) -> List:
        """
        Ingest content from a website

        Args:
            url: URL of the website

        Returns:
            List of document chunks
        """
        loader = CustomWebLoader(url)
        documents = loader.load()
        return self.text_splitter.split_documents(documents)

    def ingest_directory(self, directory_path: str, glob_pattern: str = "**/*.txt") -> List:
        """
        Ingest all text files in a directory

        Args:
            directory_path: Path to the directory
            glob_pattern: Pattern to match files

        Returns:
            List of document chunks
        """
        loader = DirectoryLoader(directory_path, glob=glob_pattern)
        documents = loader.load()
        return self.text_splitter.split_documents(documents)

    def ingest_multiple_sources(self,
                               text_files: Optional[List[str]] = None,
                               pdf_files: Optional[List[str]] = None,
                               urls: Optional[List[str]] = None,
                               directories: Optional[List[str]] = None) -> List:
        """
        Ingest multiple data sources

        Args:
            text_files: List of text file paths
            pdf_files: List of PDF file paths
            urls: List of website URLs
            directories: List of directory paths

        Returns:
            List of document chunks
        """
        all_documents = []

        if text_files:
            for file_path in text_files:
                all_documents.extend(self.ingest_text_file(file_path))

        if pdf_files:
            for file_path in pdf_files:
                all_documents.extend(self.ingest_pdf_file(file_path))

        if urls:
            for url in urls:
                all_documents.extend(self.ingest_website(url))

        if directories:
            for directory in directories:
                all_documents.extend(self.ingest_directory(directory))

        return all_documents

    def create_vector_store(self, documents: List, collection_name: str = "starbot-data") -> Chroma:
        """
        Create a vector store from documents

        Args:
            documents: List of document chunks
            collection_name: Name of the collection in the vector store

        Returns:
            Chroma vector store
        """
        return Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            collection_name=collection_name
        )
