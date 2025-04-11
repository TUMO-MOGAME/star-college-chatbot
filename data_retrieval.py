"""
Data retrieval system for Star College Chatbot
"""
import os
import logging
import requests
from typing import List, Optional
from bs4 import BeautifulSoup
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebScraper:
    """Web scraper for retrieving data from websites"""
    
    def __init__(self):
        self.visited_urls = set()
    
    def scrape_website(self, base_url: str, max_pages: int = 10) -> List[str]:
        """Scrape a website and return the text content"""
        logger.info(f"Scraping website: {base_url}")
        
        # Normalize base URL
        if not base_url.endswith('/'):
            base_url += '/'
        
        # Start with the base URL
        urls_to_visit = [base_url]
        scraped_texts = []
        
        # Process URLs until we reach the limit or run out of URLs
        while urls_to_visit and len(self.visited_urls) < max_pages:
            # Get the next URL
            url = urls_to_visit.pop(0)
            
            # Skip if already visited
            if url in self.visited_urls:
                continue
            
            # Mark as visited
            self.visited_urls.add(url)
            
            try:
                # Fetch the page
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                # Parse the HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract text content
                text = self._extract_text(soup)
                if text:
                    scraped_texts.append(text)
                
                # Find links to other pages on the same domain
                links = self._extract_links(soup, base_url)
                
                # Add new links to the queue
                for link in links:
                    if link not in self.visited_urls and link not in urls_to_visit:
                        urls_to_visit.append(link)
                
            except Exception as e:
                logger.error(f"Error scraping {url}: {e}")
        
        logger.info(f"Scraped {len(scraped_texts)} pages from {base_url}")
        return scraped_texts
    
    def _extract_text(self, soup: BeautifulSoup) -> str:
        """Extract text content from a BeautifulSoup object"""
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
        
        # Get text
        text = soup.get_text()
        
        # Break into lines and remove leading and trailing space
        lines = (line.strip() for line in text.splitlines())
        
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        
        # Remove blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        
        return text
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract links from a BeautifulSoup object"""
        links = []
        
        # Extract domain from base URL
        domain = base_url.split('//')[-1].split('/')[0]
        
        # Find all links
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            
            # Skip empty links, anchors, and non-HTTP links
            if not href or href.startswith('#') or href.startswith('javascript:'):
                continue
            
            # Convert relative URLs to absolute
            if href.startswith('/'):
                href = base_url + href[1:]
            elif not href.startswith('http'):
                href = base_url + href
            
            # Only include links to the same domain
            if domain in href:
                links.append(href)
        
        return links

class DataRetriever:
    """Data retriever for Star College Chatbot"""
    
    def __init__(self):
        self.scraper = WebScraper()
        self.documents = []
        self.initialized = False
    
    def initialize(self, url: str = "https://starcollegedurban.co.za/") -> bool:
        """Initialize the data retriever"""
        try:
            # Scrape the website
            texts = self.scraper.scrape_website(url)
            
            # Store the documents
            self.documents = texts
            
            # Mark as initialized
            self.initialized = True
            
            logger.info(f"Data retriever initialized with {len(self.documents)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing data retriever: {e}")
            return False
    
    def search(self, query: str, num_results: int = 3) -> List[str]:
        """Search for documents relevant to a query"""
        if not self.initialized:
            success = self.initialize()
            if not success:
                return ["No data available."]
        
        # Simple keyword search for now
        results = []
        query_terms = self._tokenize(query.lower())
        
        # Score each document
        scored_docs = []
        for doc in self.documents:
            score = self._score_document(doc, query_terms)
            if score > 0:
                scored_docs.append((doc, score))
        
        # Sort by score
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        # Return top results
        results = [doc for doc, _ in scored_docs[:num_results]]
        
        # If no results, return a default message
        if not results:
            results = ["No relevant information found."]
        
        return results
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words"""
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', text.lower())
        return words
    
    def _score_document(self, document: str, query_terms: List[str]) -> float:
        """Score a document based on query terms"""
        # Simple TF scoring
        doc_terms = self._tokenize(document.lower())
        
        score = 0
        for term in query_terms:
            score += doc_terms.count(term)
        
        return score
