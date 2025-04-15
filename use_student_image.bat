@echo off
echo StarBot - Use Student Image as Avatar
echo ===================================
echo.
echo This script will help you use a student image as the StarBot avatar.
echo.

set /p image_path=Enter the path to the student image: 

echo.
echo Processing image: %image_path%
echo.

python process_student_image.py "%image_path%"
if %errorlevel% neq 0 (
    echo.
    echo Error processing image. Please check the path and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo Regenerating avatar...
echo.

python generate_avatar.py
if %errorlevel% neq 0 (
    echo.
    echo Error generating avatar.
    echo.
    pause
    exit /b 1
)

echo.
echo Success! The student image has been processed and saved as the StarBot avatar.
echo.
echo Please restart the StarBot server to use the new avatar.
echo.

pause
