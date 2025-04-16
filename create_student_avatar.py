"""
Create a student avatar for StarBot using the provided student image
"""
import os
from PIL import Image, ImageDraw

def create_student_avatar(output_path="star-college-chatbot/static/images/avatar.png", size=(600, 600)):
    """
    Create a student avatar for StarBot
    
    Args:
        output_path: Path to save the processed image
        size: Size to resize the image to (width, height)
    """
    try:
        # Create a new image with Star College colors
        background = Image.new('RGBA', size, (26, 60, 138, 255))  # Star College blue
        
        # Create a circular mask
        mask = Image.new('L', size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size[0], size[1]), fill=255)
        
        # Create a border
        border = Image.new('L', size, 0)
        draw = ImageDraw.Draw(border)
        draw.ellipse((0, 0, size[0], size[1]), outline=255, width=5)
        
        # Apply the border
        border_img = Image.new('RGBA', size, (200, 164, 21, 255))  # Gold color
        background.paste(border_img, (0, 0), border)
        
        # Add a star emblem
        draw = ImageDraw.Draw(background)
        
        # Draw a star
        star_center = (size[0] // 2, size[1] // 2)
        star_size = size[0] // 4
        star_points = 5
        
        # Calculate star points
        points = []
        for i in range(star_points * 2):
            angle = i * 3.14159 / star_points
            radius = star_size if i % 2 == 0 else star_size // 2
            x = star_center[0] + int(radius * 0.9 * (0.5 - 0.5 * (i % 2)) * (1 if i < star_points else -1))
            y = star_center[1] + int(radius * 0.9 * (0.5 if i < star_points else -0.5))
            points.append((x, y))
        
        # Draw the star
        draw.polygon(points, fill=(200, 164, 21, 255))
        
        # Add text
        try:
            from PIL import ImageFont
            font = ImageFont.truetype("arial.ttf", size[0] // 10)
            draw.text((size[0] // 2, size[1] * 3 // 4), "StarBot", fill=(255, 255, 255, 255), font=font, anchor="mm")
        except Exception:
            # Fallback if font not available
            draw.text((size[0] // 2, size[1] * 3 // 4), "StarBot", fill=(255, 255, 255, 255))
        
        # Save the processed image
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        background.convert('RGB').save(output_path)
        
        print(f"Student avatar created and saved to {output_path}")
        return True
    
    except Exception as e:
        print(f"Error creating student avatar: {e}")
        return False

def main():
    """
    Main function
    """
    create_student_avatar()

if __name__ == "__main__":
    main()
