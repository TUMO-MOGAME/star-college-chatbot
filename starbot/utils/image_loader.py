"""
Image loader with OCR capabilities for StarBot
"""
import os
from typing import List, Optional
from PIL import Image
import pytesseract
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader

class ImageLoader(BaseLoader):
    """
    Load images and extract text using OCR
    """
    
    def __init__(self, file_path: str, language: str = "eng"):
        """
        Initialize the image loader
        
        Args:
            file_path: Path to the image file
            language: Language for OCR (default: English)
        """
        self.file_path = file_path
        self.language = language
        
        # Check if file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Image file not found: {file_path}")
        
        # Check if file is an image
        try:
            Image.open(file_path).verify()
        except Exception:
            raise ValueError(f"Not a valid image file: {file_path}")
    
    def load(self) -> List[Document]:
        """
        Load and extract text from the image
        
        Returns:
            List of Document objects containing extracted text
        """
        # Load image using PIL
        image = Image.open(self.file_path)
        
        # Extract text using pytesseract
        try:
            text = pytesseract.image_to_string(image, lang=self.language)
            text = text.strip()
        except Exception as e:
            raise RuntimeError(f"Error extracting text from image: {str(e)}")
        
        # If no text was extracted, return a message
        if not text:
            text = "No text could be extracted from this image."
        
        # Create metadata
        metadata = {
            "source": self.file_path,
            "type": "image",
            "format": image.format,
            "mode": image.mode,
            "width": image.width,
            "height": image.height
        }
        
        # Return document with extracted text
        return [Document(page_content=text, metadata=metadata)]


class DirectoryImageLoader(BaseLoader):
    """
    Load all images from a directory and extract text using OCR
    """
    
    def __init__(self, directory_path: str, glob_pattern: str = "**/*.{jpg,jpeg,png,gif,bmp,tiff}", language: str = "eng", recursive: bool = True):
        """
        Initialize the directory image loader
        
        Args:
            directory_path: Path to the directory
            glob_pattern: Pattern to match image files
            language: Language for OCR (default: English)
            recursive: Whether to search recursively (default: True)
        """
        self.directory_path = directory_path
        self.glob_pattern = glob_pattern
        self.language = language
        self.recursive = recursive
        
        # Check if directory exists
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Directory not found: {directory_path}")
    
    def load(self) -> List[Document]:
        """
        Load and extract text from all images in the directory
        
        Returns:
            List of Document objects containing extracted text
        """
        import glob
        
        # Find all image files in the directory
        if self.recursive:
            image_files = glob.glob(os.path.join(self.directory_path, self.glob_pattern), recursive=True)
        else:
            image_files = glob.glob(os.path.join(self.directory_path, self.glob_pattern), recursive=False)
        
        # Load each image
        documents = []
        for image_file in image_files:
            try:
                loader = ImageLoader(image_file, language=self.language)
                documents.extend(loader.load())
            except Exception as e:
                print(f"Error loading image {image_file}: {str(e)}")
        
        return documents
