"""
Generate a preview image for the avatar interface
"""
import os
from PIL import Image, ImageDraw, ImageFont

def generate_preview(filename, width=800, height=500, bg_color=(245, 245, 245)):
    """
    Generate a preview image for the avatar interface

    Args:
        filename: Output filename
        width: Image width
        height: Image height
        bg_color: Background color (RGB tuple)
    """
    # Create a new image with the given background color
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # Draw a layout mockup
    # Left panel (avatar)
    avatar_panel = (50, 50, 350, 450)
    draw.rectangle(avatar_panel, fill=(255, 255, 255), outline=(200, 164, 21), width=2)

    # Try to load the avatar image
    try:
        avatar_img = Image.open("static/images/avatar.png")
        avatar_size = 250
        avatar_pos = (
            avatar_panel[0] + (avatar_panel[2] - avatar_panel[0] - avatar_size) // 2,
            avatar_panel[1] + 50
        )
        avatar_img = avatar_img.resize((avatar_size, avatar_size))
        image.paste(avatar_img, avatar_pos)
    except Exception as e:
        print(f"Could not load avatar image: {e}")
        # Draw a placeholder circle
        avatar_center = (
            avatar_panel[0] + (avatar_panel[2] - avatar_panel[0]) // 2,
            avatar_panel[1] + 150
        )
        avatar_radius = 100
        draw.ellipse(
            (
                avatar_center[0] - avatar_radius,
                avatar_center[1] - avatar_radius,
                avatar_center[0] + avatar_radius,
                avatar_center[1] + avatar_radius
            ),
            fill=(200, 164, 21)
        )

    # Right panel (chat)
    chat_panel = (400, 50, 750, 450)
    draw.rectangle(chat_panel, fill=(255, 255, 255), outline=(26, 60, 138), width=2)

    # Draw some mock messages
    msg_y = chat_panel[1] + 30

    # User message
    user_msg = (chat_panel[0] + 150, msg_y, chat_panel[2] - 20, msg_y + 40)
    draw.rectangle(user_msg, fill=(240, 216, 122), outline=(200, 164, 21), width=1)

    # Bot message
    bot_msg = (chat_panel[0] + 20, msg_y + 60, chat_panel[0] + 250, msg_y + 100)
    draw.rectangle(bot_msg, fill=(232, 240, 255), outline=(26, 60, 138), width=1)

    # Add title
    try:
        title_font = ImageFont.truetype("arial.ttf", 24)
    except IOError:
        title_font = ImageFont.load_default()

    title = "StarBot with Talking Avatar"

    # In newer PIL versions, textsize is deprecated
    try:
        # For newer PIL versions
        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_width = title_bbox[2] - title_bbox[0]
    except AttributeError:
        # Fallback for older PIL versions
        try:
            title_width, _ = draw.textsize(title, font=title_font)
        except AttributeError:
            # If all else fails, use estimated size
            title_width = len(title) * 12

    title_position = ((width - title_width) // 2, 15)
    draw.text(title_position, title, font=title_font, fill=(26, 60, 138))

    # Save the image
    image.save(filename)
    print(f"Generated preview image: {filename}")

def main():
    """
    Generate the preview image
    """
    # Create the output directory if it doesn't exist
    output_dir = "static/images"
    os.makedirs(output_dir, exist_ok=True)

    # Generate preview image
    output_path = os.path.join(output_dir, "avatar_preview.jpg")
    generate_preview(output_path)

if __name__ == "__main__":
    main()
