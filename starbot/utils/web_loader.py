"""
Custom web loader with SSL certificate handling
"""
import os
import ssl
import certifi
import httpx
from typing import List, Optional, Dict, Any
from bs4 import BeautifulSoup
from langchain_community.document_loaders.web_base import WebBaseLoader

# Set SSL certificate environment variable
os.environ['SSL_CERT_FILE'] = certifi.where()

class CustomWebLoader(WebBaseLoader):
    """
    Custom web loader with SSL certificate handling
    """
    def __init__(self, web_path: str):
        """
        Initialize the custom web loader

        Args:
            web_path: URL to load
        """
        # Create a custom SSL context
        ssl_context = ssl.create_default_context()
        ssl_context.load_verify_locations(certifi.where())

        # Configure httpx client with SSL context
        self.client = httpx.Client(verify=certifi.where())

        super().__init__(web_path)

    def _scrape(self, url: str, **kwargs) -> BeautifulSoup:
        """
        Scrape the content from a URL and return a BeautifulSoup object

        Args:
            url: URL to scrape
            **kwargs: Additional keyword arguments

        Returns:
            BeautifulSoup object
        """
        response = self.client.get(url)
        response.raise_for_status()
        html_content = response.text

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        return soup
