"""
Download an image from a URL and save it to a file
"""
import os
import sys
import requests
from PIL import Image
from io import BytesIO

def download_image(url, output_path):
    """
    Download an image from a URL and save it to a file
    
    Args:
        url: URL of the image
        output_path: Path to save the image to
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Save the image
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Image downloaded and saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False

def main():
    """
    Main function to process command line arguments
    """
    if len(sys.argv) < 3:
        print("Usage: python download_image.py <image_url> <output_path>")
        return
    
    url = sys.argv[1]
    output_path = sys.argv[2]
    download_image(url, output_path)

if __name__ == "__main__":
    main()
