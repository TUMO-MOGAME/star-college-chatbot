"""
Image data handler for Star College Chatbot
"""
import os
import logging
from typing import List, Optional
import glob
from starbot.data.ingestion import DataIngestion
from starbot.utils.image_loader import ImageLoader, DirectoryImageLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageDataHandler:
    """Handler for processing image data for the chatbot"""
    
    def __init__(self):
        """Initialize the image data handler"""
        self.data_ingestion = DataIngestion()
        self.processed_images = set()
    
    def process_image(self, image_path: str, language: str = "eng") -> List:
        """
        Process a single image file
        
        Args:
            image_path: Path to the image file
            language: Language for OCR (default: English)
            
        Returns:
            List of document chunks
        """
        logger.info(f"Processing image: {image_path}")
        
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return []
            
            # Process the image
            documents = self.data_ingestion.ingest_image(image_path, language=language)
            
            # Add to processed images
            self.processed_images.add(image_path)
            
            logger.info(f"Processed image {image_path}: {len(documents)} document chunks")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing image {image_path}: {str(e)}")
            return []
    
    def process_image_directory(self, directory_path: str, language: str = "eng") -> List:
        """
        Process all images in a directory
        
        Args:
            directory_path: Path to the directory
            language: Language for OCR (default: English)
            
        Returns:
            List of document chunks
        """
        logger.info(f"Processing images in directory: {directory_path}")
        
        try:
            # Check if directory exists
            if not os.path.isdir(directory_path):
                logger.error(f"Directory not found: {directory_path}")
                return []
            
            # Process the directory
            documents = self.data_ingestion.ingest_image_directory(directory_path, language=language)
            
            # Add all processed images to the set
            image_files = glob.glob(os.path.join(directory_path, "**/*.{jpg,jpeg,png,gif,bmp,tiff}"), recursive=True)
            self.processed_images.update(image_files)
            
            logger.info(f"Processed directory {directory_path}: {len(documents)} document chunks")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing directory {directory_path}: {str(e)}")
            return []
    
    def get_processed_images(self) -> List[str]:
        """
        Get a list of all processed image paths
        
        Returns:
            List of image file paths
        """
        return list(self.processed_images)
