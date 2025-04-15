# Using the Student Image as the StarBot Avatar

To use the student image as the avatar for StarBot, follow these steps:

## Step 1: Save the Student Image

1. Right-click on the student image in your web browser
2. Select "Save Image As..." or "Download Image"
3. Save the image to your computer (e.g., as `student.jpg`)

## Step 2: Process the Image

Run the following command to process the image:

```bash
python process_student_image.py path/to/student.jpg
```

Replace `path/to/student.jpg` with the actual path to the saved image.

## Step 3: Regenerate the Avatar

Run the following command to regenerate the avatar:

```bash
python generate_avatar.py
```

## Step 4: Restart the StarBot Server

Restart the StarBot server to use the new avatar:

```bash
python star_college_server.py
```

## Verifying the Avatar

1. Open your web browser and navigate to the StarBot URL
2. The student image should now be used as the avatar
3. The avatar will animate when the chatbot responds to questions

## Troubleshooting

If you encounter any issues:

1. Make sure the image file exists and is a valid image format (JPG, PNG, etc.)
2. Check that the `static/images` directory exists
3. Try running the scripts with administrator privileges if you encounter permission issues
4. If all else fails, the system will fall back to using the generated cartoon avatar
