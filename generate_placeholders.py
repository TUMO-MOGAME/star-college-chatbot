"""
Generate placeholder images for StarBot
"""
import os
from PIL import Image, ImageDraw, ImageFont

def generate_placeholder_image(filename, text, width=800, height=600, bg_color=(230, 230, 230), text_color=(100, 100, 100)):
    """
    Generate a placeholder image with text
    
    Args:
        filename: Output filename
        text: Text to display on the image
        width: Image width
        height: Image height
        bg_color: Background color (RGB tuple)
        text_color: Text color (RGB tuple)
    """
    # Create a new image with the given background color
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    # Try to use a system font, fall back to default if not available
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    text_width, text_height = draw.textsize(text, font=font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    
    # Draw the text
    draw.text(position, text, font=font, fill=text_color)
    
    # Save the image
    image.save(filename)
    print(f"Generated placeholder image: {filename}")

def main():
    """
    Generate all placeholder images
    """
    # Create the output directory if it doesn't exist
    output_dir = "static/images"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate placeholder images
    placeholders = [
        ("campus_main.jpg", "Main Campus"),
        ("science.jpg", "Science Laboratory"),
        ("computer_lab.jpg", "Computer Lab"),
        ("library.jpg", "Library"),
        ("sports_field.jpg", "Sports Field"),
        ("students.jpg", "Students"),
        ("chess.jpg", "Chess Champion")
    ]
    
    for filename, text in placeholders:
        output_path = os.path.join(output_dir, filename)
        generate_placeholder_image(output_path, text)

if __name__ == "__main__":
    main()
