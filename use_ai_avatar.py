"""
Download and use an AI-generated avatar for StarBot
"""
import os
import sys
import requests
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import webbrowser
import shutil

def download_thispersondoesnotexist():
    """
    Download a random AI-generated face from thispersondoesnotexist.com
    """
    url = "https://thispersondoesnotexist.com/"
    output_path = "static/images/ai_avatar_raw.jpg"
    
    try:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Download the image
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        
        # Save the image
        with open(output_path, 'wb') as f:
            f.write(response.content)
        
        # Process the image
        process_avatar(output_path)
        
        return True
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False

def process_avatar(input_path, output_path="static/images/ai_avatar.png"):
    """
    Process an avatar image to make it suitable for StarBot
    """
    try:
        # Open the image
        img = Image.open(input_path)
        
        # Crop to square focusing on the face (center crop)
        width, height = img.size
        size = min(width, height)
        left = (width - size) // 2
        top = (height - size) // 2
        right = left + size
        bottom = top + size
        img = img.crop((left, top, right, bottom))
        
        # Resize to 600x600
        img = img.resize((600, 600), Image.LANCZOS)
        
        # Create a circular mask
        mask = Image.new('L', (600, 600), 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse((0, 0, 600, 600), fill=255)
        
        # Create a new image with a blue background
        background = Image.new('RGB', (600, 600), '#1a3c8a')
        
        # Paste the face onto the background using the mask
        background.paste(img, (0, 0), mask)
        
        # Save the processed image
        background.save(output_path)
        
        # Also save as avatar.png for the chatbot to use
        background.save("static/images/avatar.png")
        
        print(f"Processed avatar saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error processing avatar: {e}")
        return False

def open_ai_avatar_sites():
    """
    Open a GUI with links to AI avatar generation sites
    """
    root = tk.Tk()
    root.title("AI Avatar Generator for StarBot")
    root.geometry("800x600")
    root.configure(bg="#f0f0f0")
    
    # Create a frame for the title
    title_frame = tk.Frame(root, bg="#1a3c8a", padx=20, pady=10)
    title_frame.pack(fill="x")
    
    # Add a title
    title_label = tk.Label(
        title_frame,
        text="Generate a Realistic Avatar for StarBot",
        font=("Arial", 24, "bold"),
        fg="white",
        bg="#1a3c8a"
    )
    title_label.pack()
    
    # Create a frame for the content
    content_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
    content_frame.pack(fill="both", expand=True)
    
    # Add instructions
    instructions = tk.Label(
        content_frame,
        text="Choose one of the following methods to create a realistic avatar for StarBot:",
        font=("Arial", 14),
        bg="#f0f0f0",
        wraplength=700,
        justify="left"
    )
    instructions.pack(anchor="w", pady=(0, 20))
    
    # Create a frame for the options
    options_frame = tk.Frame(content_frame, bg="#f0f0f0")
    options_frame.pack(fill="both", expand=True)
    
    # Option 1: This Person Does Not Exist
    option1_frame = tk.Frame(options_frame, bg="#f0f0f0", padx=10, pady=10, borderwidth=2, relief="ridge")
    option1_frame.pack(fill="x", pady=10)
    
    option1_title = tk.Label(
        option1_frame,
        text="Option 1: This Person Does Not Exist",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    )
    option1_title.pack(anchor="w")
    
    option1_desc = tk.Label(
        option1_frame,
        text="Generate a random realistic face using AI. This will download a face from thispersondoesnotexist.com and process it for use as the StarBot avatar.",
        font=("Arial", 12),
        bg="#f0f0f0",
        wraplength=700,
        justify="left"
    )
    option1_desc.pack(anchor="w", pady=(5, 10))
    
    option1_button = tk.Button(
        option1_frame,
        text="Generate Random Face",
        font=("Arial", 12, "bold"),
        bg="#1a3c8a",
        fg="white",
        padx=10,
        pady=5,
        command=download_thispersondoesnotexist
    )
    option1_button.pack(anchor="w")
    
    # Option 2: Visit AI Avatar Sites
    option2_frame = tk.Frame(options_frame, bg="#f0f0f0", padx=10, pady=10, borderwidth=2, relief="ridge")
    option2_frame.pack(fill="x", pady=10)
    
    option2_title = tk.Label(
        option2_frame,
        text="Option 2: Visit AI Avatar Generation Sites",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    )
    option2_title.pack(anchor="w")
    
    option2_desc = tk.Label(
        option2_frame,
        text="Visit one of these websites to create or download a realistic avatar, then save it and use it as the StarBot avatar.",
        font=("Arial", 12),
        bg="#f0f0f0",
        wraplength=700,
        justify="left"
    )
    option2_desc.pack(anchor="w", pady=(5, 10))
    
    # Create a frame for the site buttons
    sites_frame = tk.Frame(option2_frame, bg="#f0f0f0")
    sites_frame.pack(anchor="w")
    
    # Function to open a website
    def open_site(url):
        webbrowser.open(url)
    
    # Add buttons for each site
    site1_button = tk.Button(
        sites_frame,
        text="This Person Does Not Exist",
        font=("Arial", 12),
        bg="#c8a415",
        fg="white",
        padx=10,
        pady=5,
        command=lambda: open_site("https://thispersondoesnotexist.com/")
    )
    site1_button.grid(row=0, column=0, padx=5, pady=5)
    
    site2_button = tk.Button(
        sites_frame,
        text="Artbreeder",
        font=("Arial", 12),
        bg="#c8a415",
        fg="white",
        padx=10,
        pady=5,
        command=lambda: open_site("https://www.artbreeder.com/")
    )
    site2_button.grid(row=0, column=1, padx=5, pady=5)
    
    site3_button = tk.Button(
        sites_frame,
        text="Generated Photos",
        font=("Arial", 12),
        bg="#c8a415",
        fg="white",
        padx=10,
        pady=5,
        command=lambda: open_site("https://generated.photos/")
    )
    site3_button.grid(row=0, column=2, padx=5, pady=5)
    
    # Option 3: Use Your Own Image
    option3_frame = tk.Frame(options_frame, bg="#f0f0f0", padx=10, pady=10, borderwidth=2, relief="ridge")
    option3_frame.pack(fill="x", pady=10)
    
    option3_title = tk.Label(
        option3_frame,
        text="Option 3: Use Your Own Image",
        font=("Arial", 16, "bold"),
        bg="#f0f0f0"
    )
    option3_title.pack(anchor="w")
    
    option3_desc = tk.Label(
        option3_frame,
        text="Select an image from your computer to use as the StarBot avatar. The image will be processed to fit the StarBot avatar style.",
        font=("Arial", 12),
        bg="#f0f0f0",
        wraplength=700,
        justify="left"
    )
    option3_desc.pack(anchor="w", pady=(5, 10))
    
    # Function to select and process an image
    def select_image():
        file_path = filedialog.askopenfilename(
            title="Select Avatar Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
        )
        
        if file_path:
            process_avatar(file_path)
            messagebox.showinfo("Success", "Avatar processed successfully! Restart StarBot to see the changes.")
    
    option3_button = tk.Button(
        option3_frame,
        text="Select Image",
        font=("Arial", 12, "bold"),
        bg="#1a3c8a",
        fg="white",
        padx=10,
        pady=5,
        command=select_image
    )
    option3_button.pack(anchor="w")
    
    # Add a status label
    status_label = tk.Label(
        root,
        text="Select an option to create a realistic avatar for StarBot",
        font=("Arial", 12),
        bg="#f0f0f0",
        pady=10
    )
    status_label.pack()
    
    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    # Import ImageDraw here to avoid circular import
    from PIL import ImageDraw
    open_ai_avatar_sites()
