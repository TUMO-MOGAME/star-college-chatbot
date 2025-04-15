"""
Script to use a custom image as the StarBot avatar
"""
import os
import sys
import shutil
from PIL import Image

def use_custom_avatar(image_path, output_name="avatar.png", size=(600, 600)):
    """
    Process a custom image and use it as the StarBot avatar
    
    Args:
        image_path: Path to the custom image
        output_name: Name for the output avatar file
        size: Size to resize the avatar to (width, height)
    """
    if not os.path.exists(image_path):
        print(f"Error: Image file not found at {image_path}")
        return False
    
    try:
        # Create the output directory if it doesn't exist
        output_dir = "static/images"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_name)
        
        # Process the image - resize and make circular if needed
        try:
            # Open and resize the image
            img = Image.open(image_path)
            
            # Calculate aspect ratio
            width, height = img.size
            aspect_ratio = width / height
            
            # Determine new dimensions while maintaining aspect ratio
            if aspect_ratio > 1:  # Width > Height
                new_width = size[0]
                new_height = int(new_width / aspect_ratio)
            else:  # Height >= Width
                new_height = size[1]
                new_width = int(new_height * aspect_ratio)
            
            # Resize the image
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Create a new image with the target size and paste the resized image centered
            new_img = Image.new("RGBA", size, (0, 0, 0, 0))
            paste_x = (size[0] - new_width) // 2
            paste_y = (size[1] - new_height) // 2
            new_img.paste(img, (paste_x, paste_y))
            
            # Save the processed image
            new_img.save(output_path)
            print(f"Avatar saved to {output_path}")
            
        except Exception as e:
            print(f"Error processing image: {e}")
            # If image processing fails, just copy the file
            shutil.copy(image_path, output_path)
            print(f"Original image copied to {output_path}")
        
        return True
    
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """
    Main function to process command line arguments
    """
    if len(sys.argv) < 2:
        print("Usage: python use_custom_avatar.py <path_to_image>")
        return
    
    image_path = sys.argv[1]
    use_custom_avatar(image_path)

if __name__ == "__main__":
    main()
