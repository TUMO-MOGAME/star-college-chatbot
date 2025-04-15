"""
Process the student image for use as the StarBot avatar
"""
import os
import sys
import requests
from PIL import Image
from io import BytesIO

def process_student_image(input_path, output_path="static/images/student_avatar.jpg", size=(600, 600)):
    """
    Process a student image for use as the StarBot avatar
    
    Args:
        input_path: Path to the input image
        output_path: Path to save the processed image
        size: Size to resize the image to (width, height)
    """
    try:
        # Check if the input file exists
        if not os.path.exists(input_path):
            print(f"Error: Input file {input_path} does not exist")
            return False
        
        # Open the image
        img = Image.open(input_path)
        
        # Resize the image while maintaining aspect ratio
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height
        
        if aspect_ratio > 1:  # Width > Height
            new_width = size[0]
            new_height = int(new_width / aspect_ratio)
        else:  # Height >= Width
            new_height = size[1]
            new_width = int(new_height * aspect_ratio)
        
        img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Create a new image with the target size and paste the resized image centered
        new_img = Image.new("RGB", size, (30, 60, 120))
        paste_x = (size[0] - new_width) // 2
        paste_y = (size[1] - new_height) // 2
        new_img.paste(img, (paste_x, paste_y))
        
        # Save the processed image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        new_img.save(output_path)
        print(f"Processed student image saved to {output_path}")
        return True
    
    except Exception as e:
        print(f"Error processing student image: {e}")
        return False

def main():
    """
    Main function to process command line arguments
    """
    if len(sys.argv) < 2:
        print("Usage: python process_student_image.py <input_image_path> [output_image_path]")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "static/images/student_avatar.jpg"
    
    process_student_image(input_path, output_path)

if __name__ == "__main__":
    main()
