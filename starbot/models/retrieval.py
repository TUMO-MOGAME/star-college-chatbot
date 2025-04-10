"""
Retrieval and response generation for StarBot
"""
import os
import ssl
import certifi
import httpx
from typing import List, Dict, Any, Optional, Union
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import Chroma

# Set SSL certificate environment variable
os.environ['SSL_CERT_FILE'] = certifi.where()

# Create a custom SSL context
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())

# Configure httpx client with SSL context
httpx_client = httpx.Client(verify=certifi.where())

class RetrievalQA:
    """
    Retrieval-based question answering system
    """
    def __init__(self, vector_store: Chroma, llm, k: int = 3):
        """
        Initialize the retrieval QA system

        Args:
            vector_store: Vector store containing document embeddings
            llm: Language model for generating responses
            k: Number of documents to retrieve
        """
        self.vector_store = vector_store
        self.llm = llm
        self.k = k
        self.retriever = vector_store.as_retriever(search_kwargs={"k": k})

        # Create the prompt template
        self.prompt_template = """
        You are StarBot, a helpful assistant that answers questions based ONLY on the provided context.

        Context information is below:
        ---------------------
        {context}
        ---------------------

        Given the context information and not prior knowledge, answer the question: {question}

        If the answer cannot be determined from the context, respond with "I don't have enough information to answer that question."
        """

        self.prompt = ChatPromptTemplate.from_template(self.prompt_template)

        # Create the chain
        self.chain = (
            {"context": self.retriever, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def get_relevant_documents(self, query: str) -> List:
        """
        Get relevant documents for a query

        Args:
            query: User query

        Returns:
            List of relevant documents
        """
        return self.retriever.get_relevant_documents(query)

    def answer_question(self, question: str) -> str:
        """
        Answer a question using the retrieval system

        Args:
            question: User question

        Returns:
            Generated answer
        """
        return self.chain.invoke(question)

    def answer_question_with_sources(self, question: str) -> Dict[str, Any]:
        """
        Answer a question and provide source documents

        Args:
            question: User question

        Returns:
            Dictionary with answer and source documents
        """
        docs = self.get_relevant_documents(question)
        answer = self.answer_question(question)

        return {
            "answer": answer,
            "sources": [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]
        }
