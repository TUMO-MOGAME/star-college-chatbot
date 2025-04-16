"""
Process the student portrait image for use as the StarBot avatar
"""
import os
import sys
from PIL import Image, ImageDraw, ImageOps, ImageFilter, ImageEnhance

def process_student_portrait(input_path="star-college-chatbot/static/images/student_avatar_original.jpg",
                           output_path="star-college-chatbot/static/images/avatar.png",
                           size=(600, 600)):
    """
    Process the student portrait image for use as the StarBot avatar

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

        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')

        # Crop to square focusing on the face
        width, height = img.size

        # For portrait images, we want to focus on the face
        # Assuming the face is in the upper portion of the image
        if width > height:
            # Landscape image - crop to square from center
            left = (width - height) // 2
            top = 0
            right = left + height
            bottom = height
        else:
            # Portrait image - crop to square focusing on the face (upper portion)
            top = height // 8  # Start from 1/8 down to focus on face
            left = 0
            bottom = top + width
            right = width

            # If the crop would go beyond the image, adjust
            if bottom > height:
                diff = bottom - height
                top = max(0, top - diff)
                bottom = height

        # Crop the image
        img = img.crop((left, top, right, bottom))

        # Resize to the target size
        img = img.resize(size, Image.LANCZOS)

        # Enhance the image slightly
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)

        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)

        # Create a circular mask
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)

        # Apply the mask
        img_masked = Image.new('RGBA', size, (0, 0, 0, 0))
        img_masked.paste(img, (0, 0), mask)

        # Create a background with Star College colors
        background = Image.new('RGBA', size, (26, 60, 138, 255))  # Star College blue

        # Create a border
        border = Image.new('L', size, 0)
        draw = ImageDraw.Draw(border)
        draw.ellipse((0, 0, size[0], size[1]), outline=255, width=5)

        # Apply the border
        border_img = Image.new('RGBA', size, (200, 164, 21, 255))  # Gold color
        background.paste(border_img, (0, 0), border)

        # Paste the masked image onto the background
        result = Image.alpha_composite(background, img_masked)

        # Convert back to RGB for saving as PNG
        result = result.convert('RGB')

        # Save the processed image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        result.save(output_path)

        print(f"Processed student portrait saved to {output_path}")
        return True

    except Exception as e:
        print(f"Error processing student portrait: {e}")
        return False

def main():
    """
    Main function to process command line arguments
    """
    input_path = sys.argv[1] if len(sys.argv) > 1 else "star-college-chatbot/static/images/student_avatar_original.jpg"
    output_path = sys.argv[2] if len(sys.argv) > 2 else "star-college-chatbot/static/images/avatar.png"

    process_student_portrait(input_path, output_path)

if __name__ == "__main__":
    main()
