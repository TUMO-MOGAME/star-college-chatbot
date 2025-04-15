"""
Generate a placeholder avatar image for StarBot
"""
import os
from PIL import Image, ImageDraw, ImageFont

def generate_avatar(filename, width=600, height=600, bg_color=(30, 60, 120), text_color=(255, 255, 255)):
    """
    Generate a professional avatar image

    Args:
        filename: Output filename
        width: Image width
        height: Image height
        bg_color: Background color (RGB tuple)
        text_color: Text color (RGB tuple)
    """
    # Try to use the student image if available
    student_image_path = "static/images/student_avatar.jpg"

    if os.path.exists(student_image_path):
        try:
            # Open the student image
            img = Image.open(student_image_path)

            # Resize the image while maintaining aspect ratio
            img_width, img_height = img.size
            aspect_ratio = img_width / img_height

            if aspect_ratio > 1:  # Width > Height
                new_width = width
                new_height = int(new_width / aspect_ratio)
            else:  # Height >= Width
                new_height = height
                new_width = int(new_height * aspect_ratio)

            img = img.resize((new_width, new_height), Image.LANCZOS)

            # Create a new image with the target size and paste the resized image centered
            new_img = Image.new("RGB", (width, height), bg_color)
            paste_x = (width - new_width) // 2
            paste_y = (height - new_height) // 2
            new_img.paste(img, (paste_x, paste_y))

            # Save the processed image
            new_img.save(filename)
            print(f"Student avatar saved to {filename}")
            return
        except Exception as e:
            print(f"Error processing student image: {e}")
            print("Falling back to generated avatar...")

    # If student image is not available or processing fails, create a placeholder avatar
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)

    # Draw a circle for the face
    face_radius = width // 3
    face_center = (width // 2, height // 2)
    face_bbox = (
        face_center[0] - face_radius,
        face_center[1] - face_radius,
        face_center[0] + face_radius,
        face_center[1] + face_radius
    )
    draw.ellipse(face_bbox, fill=(240, 220, 180))

    # Draw eyes
    eye_radius = face_radius // 5
    left_eye_center = (face_center[0] - face_radius // 2, face_center[1] - face_radius // 4)
    right_eye_center = (face_center[0] + face_radius // 2, face_center[1] - face_radius // 4)

    # Eye whites
    draw.ellipse((
        left_eye_center[0] - eye_radius,
        left_eye_center[1] - eye_radius,
        left_eye_center[0] + eye_radius,
        left_eye_center[1] + eye_radius
    ), fill=(255, 255, 255))

    draw.ellipse((
        right_eye_center[0] - eye_radius,
        right_eye_center[1] - eye_radius,
        right_eye_center[0] + eye_radius,
        right_eye_center[1] + eye_radius
    ), fill=(255, 255, 255))

    # Pupils
    pupil_radius = eye_radius // 2
    draw.ellipse((
        left_eye_center[0] - pupil_radius,
        left_eye_center[1] - pupil_radius,
        left_eye_center[0] + pupil_radius,
        left_eye_center[1] + pupil_radius
    ), fill=(0, 0, 0))

    draw.ellipse((
        right_eye_center[0] - pupil_radius,
        right_eye_center[1] - pupil_radius,
        right_eye_center[0] + pupil_radius,
        right_eye_center[1] + pupil_radius
    ), fill=(0, 0, 0))

    # Draw a smile
    smile_start = (face_center[0] - face_radius // 2, face_center[1] + face_radius // 4)
    smile_end = (face_center[0] + face_radius // 2, face_center[1] + face_radius // 4)
    smile_control = (face_center[0], face_center[1] + face_radius // 2)

    # Draw a curved smile using a quadratic bezier curve approximation
    points = []
    steps = 20
    for i in range(steps + 1):
        t = i / steps
        # Quadratic bezier formula: B(t) = (1-t)²P₀ + 2(1-t)tP₁ + t²P₂
        x = (1-t)**2 * smile_start[0] + 2*(1-t)*t*smile_control[0] + t**2*smile_end[0]
        y = (1-t)**2 * smile_start[1] + 2*(1-t)*t*smile_control[1] + t**2*smile_end[1]
        points.append((x, y))

    # Draw the smile with a thicker line
    for i in range(len(points) - 1):
        draw.line([points[i], points[i+1]], fill=(0, 0, 0), width=5)

    # Add text "StarBot" at the bottom
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        font = ImageFont.load_default()

    text = "StarBot"
    # In newer PIL versions, textsize is deprecated
    try:
        # For newer PIL versions
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
    except AttributeError:
        # Fallback for older PIL versions
        try:
            text_width, text_height = draw.textsize(text, font=font)
        except AttributeError:
            # If all else fails, use estimated size
            text_width, text_height = len(text) * 20, 40

    text_position = ((width - text_width) // 2, height - text_height - 20)
    draw.text(text_position, text, font=font, fill=text_color)

    # Save the image
    image.save(filename)
    print(f"Generated avatar image: {filename}")

def main():
    """
    Generate the avatar image
    """
    # Create the output directory if it doesn't exist
    output_dir = "static/images"
    os.makedirs(output_dir, exist_ok=True)

    # Generate avatar image
    output_path = os.path.join(output_dir, "avatar.png")
    generate_avatar(output_path)

if __name__ == "__main__":
    main()
