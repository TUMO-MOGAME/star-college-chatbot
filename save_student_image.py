"""
Save the student image from the clipboard or a file
"""
import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import subprocess

def save_student_image():
    """
    Save the student image from a file
    """
    root = tk.Tk()
    root.withdraw()
    
    # Ask the user to select an image file
    file_path = filedialog.askopenfilename(
        title="Select Student Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    
    if not file_path:
        print("No file selected. Exiting.")
        return
    
    # Process the image
    output_path = "static/images/student_avatar.jpg"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        # Run the process_student_image.py script
        subprocess.run([sys.executable, "process_student_image.py", file_path, output_path], check=True)
        
        # Run the generate_avatar.py script
        subprocess.run([sys.executable, "generate_avatar.py"], check=True)
        
        # Show a preview of the processed image
        root = tk.Tk()
        root.title("Student Avatar Preview")
        
        # Load and display the processed image
        img = Image.open("static/images/avatar.png")
        img = img.resize((300, 300), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        label = tk.Label(root, image=photo)
        label.pack(padx=10, pady=10)
        
        # Add a label with instructions
        instructions = tk.Label(
            root,
            text="The student image has been processed and saved as the StarBot avatar.\n"
                 "Restart the StarBot server to use the new avatar.",
            wraplength=400,
            justify="center",
            padx=10,
            pady=10
        )
        instructions.pack()
        
        # Add a close button
        close_button = tk.Button(root, text="Close", command=root.destroy)
        close_button.pack(pady=10)
        
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
        print(f"Error: {e}")

if __name__ == "__main__":
    save_student_image()
