"""
Choose between different avatar styles
"""
import os
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import shutil

def choose_avatar_style():
    """
    Choose between different avatar styles
    """
    # Check if the avatar images exist
    avatar_paths = {
        "Realistic": "static/images/realistic_avatar.png",
        "Advanced": "static/images/advanced_avatar.png",
        "Photorealistic": "static/images/photorealistic_avatar.png"
    }
    
    # Create the main window
    root = tk.Tk()
    root.title("Choose StarBot Avatar Style")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")
    
    # Create a frame for the title
    title_frame = tk.Frame(root, bg="#1a3c8a", padx=20, pady=10)
    title_frame.pack(fill="x")
    
    # Add a title
    title_label = tk.Label(
        title_frame,
        text="Choose StarBot Avatar Style",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#1a3c8a"
    )
    title_label.pack()
    
    # Create a frame for the avatars
    avatars_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
    avatars_frame.pack(fill="both", expand=True)
    
    # Create a frame for each avatar
    avatar_frames = {}
    avatar_images = {}
    avatar_photos = {}
    selected_style = tk.StringVar(value="Photorealistic")
    
    # Function to select an avatar style
    def select_style(style):
        selected_style.set(style)
        for s in avatar_frames:
            if s == style:
                avatar_frames[s].config(bg="#c8a415")
            else:
                avatar_frames[s].config(bg="#f0f0f0")
    
    # Create a frame for each avatar style
    for i, (style, path) in enumerate(avatar_paths.items()):
        # Check if the avatar image exists
        if not os.path.exists(path):
            continue
        
        # Create a frame for the avatar
        avatar_frames[style] = tk.Frame(
            avatars_frame,
            bg="#f0f0f0",
            padx=10,
            pady=10,
            borderwidth=2,
            relief="ridge"
        )
        avatar_frames[style].grid(row=0, column=i, padx=10, pady=10)
        
        # Load the avatar image
        avatar_images[style] = Image.open(path)
        avatar_images[style] = avatar_images[style].resize((200, 200), Image.LANCZOS)
        avatar_photos[style] = ImageTk.PhotoImage(avatar_images[style])
        
        # Add the avatar image
        avatar_label = tk.Label(
            avatar_frames[style],
            image=avatar_photos[style],
            bg="#f0f0f0"
        )
        avatar_label.pack(padx=10, pady=10)
        
        # Add the avatar style name
        style_label = tk.Label(
            avatar_frames[style],
            text=style,
            font=("Arial", 16, "bold"),
            bg="#f0f0f0"
        )
        style_label.pack(padx=10, pady=5)
        
        # Add a select button
        select_button = tk.Button(
            avatar_frames[style],
            text="Select",
            font=("Arial", 12),
            bg="#1a3c8a",
            fg="white",
            padx=10,
            pady=5,
            command=lambda s=style: select_style(s)
        )
        select_button.pack(padx=10, pady=10)
        
        # Select the default style
        if style == selected_style.get():
            select_style(style)
    
    # Create a frame for the buttons
    buttons_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
    buttons_frame.pack(fill="x")
    
    # Function to apply the selected style
    def apply_style():
        style = selected_style.get()
        if style in avatar_paths and os.path.exists(avatar_paths[style]):
            # Copy the selected avatar to avatar.png
            shutil.copy(avatar_paths[style], "static/images/avatar.png")
            status_label.config(text=f"Applied {style} avatar style!")
    
    # Function to generate all avatars
    def generate_all():
        # Run the avatar generation scripts
        os.system("python generate_realistic_avatar.py")
        os.system("python generate_advanced_avatar.py")
        os.system("python generate_photorealistic_avatar.py")
        
        # Reload the avatar images
        for style, path in avatar_paths.items():
            if os.path.exists(path):
                avatar_images[style] = Image.open(path)
                avatar_images[style] = avatar_images[style].resize((200, 200), Image.LANCZOS)
                avatar_photos[style] = ImageTk.PhotoImage(avatar_images[style])
                avatar_frames[style].children['!label'].config(image=avatar_photos[style])
        
        status_label.config(text="Generated all avatar styles!")
    
    # Add an apply button
    apply_button = tk.Button(
        buttons_frame,
        text="Apply Selected Style",
        font=("Arial", 14, "bold"),
        bg="#1a3c8a",
        fg="white",
        padx=20,
        pady=10,
        command=apply_style
    )
    apply_button.pack(side="left", padx=10)
    
    # Add a generate all button
    generate_button = tk.Button(
        buttons_frame,
        text="Generate All Styles",
        font=("Arial", 14),
        bg="#c8a415",
        fg="white",
        padx=20,
        pady=10,
        command=generate_all
    )
    generate_button.pack(side="right", padx=10)
    
    # Add a status label
    status_label = tk.Label(
        root,
        text="Select an avatar style and click Apply",
        font=("Arial", 12),
        bg="#f0f0f0",
        pady=10
    )
    status_label.pack()
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    choose_avatar_style()
