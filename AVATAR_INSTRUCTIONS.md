# StarBot Avatar Instructions

This document explains how to use a custom image as the avatar for StarBot.

## Using the Student Image as the Avatar

To use the student image as the avatar for StarBot, follow these steps:

1. Save the student image to a file on your computer (e.g., `student.jpg`)
2. Process the image using the provided script:

```bash
python process_student_image.py student.jpg
```

3. Regenerate the avatar:

```bash
python generate_avatar.py
```

4. Restart the StarBot server to use the new avatar

## Alternative Method

If you have the student image in a different location or want to use a different image, you can use the `use_custom_avatar.py` script:

```bash
python use_custom_avatar.py path/to/your/image.jpg
```

This script will process the image and save it as the StarBot avatar.

## Troubleshooting

If you encounter any issues:

1. Make sure the image file exists and is a valid image format (JPG, PNG, etc.)
2. Check that the `static/images` directory exists
3. Try running the scripts with administrator privileges if you encounter permission issues
4. If all else fails, the system will fall back to using the generated cartoon avatar

## Customizing the Avatar

You can customize the avatar by editing the `generate_avatar.py` script. Some options include:

- Changing the background color
- Adjusting the size of the avatar
- Adding text or other elements to the avatar

## Using the Avatar in StarBot

The avatar is used in the StarBot interface when you access the avatar version:

- Default URL: `http://your-domain.com/` (avatar version is now the default)
- Explicit avatar URL: `http://your-domain.com/avatar`
- Standard version (no avatar): `http://your-domain.com/standard`
