import requests
import io
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from ttkbootstrap import Style
import os

# Set your Unsplash API key from environment variable
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY", "1n7sSMtCh8Hs_MrBOjhQ1SygTDA-BJ550UdX3rwLYZQ")
if not UNSPLASH_API_KEY:
    raise ValueError("Please set the UNSPLASH_API_KEY environment variable.")

# Create the main window
root = tk.Tk()
root.title("Image Generator")
root.geometry("1280x800")

# Apply a modern style
style = Style(theme="darkly")
root.config(bg=style.colors.bg)

# Function to retrieve and display an image based on the entered category
def display_image(category):
    try:
        url = f"https://api.unsplash.com/photos/random?query={category}&orientation=landscape&client_id=1n7sSMtCh8Hs_MrBOjhQ1SygTDA-BJ550UdX3rwLYZQ"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Fetch and display image
        img_data = requests.get(data["urls"]["regular"]).content
        image = Image.open(io.BytesIO(img_data))
        photo = ImageTk.PhotoImage(image.resize((1050, 450), resample=Image.LANCZOS))

        # Start scale-up animation
        scale_up_image(photo)
    except requests.exceptions.RequestException as e:
        print("Error fetching image:", e)
    except KeyError:
        print("Unexpected response structure.")

# Scale-up effect for the image
def scale_up_image(photo, scale=0.1):
    if scale < 1.0:
        # Increase scale
        label.config(image=photo)
        label.image = photo
        label.place(relx=0.5, rely=0.5, anchor="center", width=int(1050 * scale), height=int(450 * scale))
        scale += 0.05  # Increment scale value
        label.after(50, scale_up_image, photo, scale)  # Call again after 50ms
    else:
        # Ensure the final size is set correctly
        label.place(relx=0.5, rely=0.5, anchor="center", width=1050, height=450)

# Function to enable/disable the "Generate Image" button based on user input
def enable_button(*args):
    generate_button.config(state="normal" if category_var.get().strip() else "disabled")

# Animation function for header text (typing effect)
def animate_text(text, label, index=0):
    if index < len(text):
        label.config(text=text[:index + 1])
        root.after(100, animate_text, text, label, index + 1)  # 100 ms delay for typing effect

# Create the GUI elements
def create_gui():
    global category_var, generate_button, label

    # Add a header label with typing animation
    header_text = "Welcome to the Image Generator"
    header_label = tk.Label(root, text="", font=("Helvetica", 24, "bold"),
                            bg=style.colors.primary, fg="white")
    header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 10), sticky="nsew")

    # Start the text animation
    animate_text(header_text, header_label)

    # Create an entry box for typing the category
    category_var = tk.StringVar()
    category_entry = ttk.Entry(root, textvariable=category_var, font=("Helvetica", 12), width=30)
    category_entry.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
    category_entry.insert(0, "Enter category")  # Placeholder text
    category_entry.bind("<FocusIn>", lambda event: category_entry.delete(0, tk.END) if category_entry.get() == "Enter category" else None)
    category_var.trace_add("write", enable_button)  # Enable button when text is entered

    # Create a button for generating the image
    generate_button = ttk.Button(root, text="Generate Image", command=lambda: display_image(category_var.get()), style="success.TButton")
    generate_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
    generate_button.config(state="disabled")  # Initially disabled

    # Create a frame for displaying images
    frame = ttk.Frame(root, padding=10, relief="ridge", style="dark.TFrame")
    frame.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")

    # Create a label for displaying images within the frame
    label = tk.Label(frame, background=style.colors.bg)
    label.place(relx=0.5, rely=0.5, anchor="center", width=0, height=0)  # Start with size 0 for animation

    # Add a footer with information
    footer_label = tk.Label(root, text="Powered by Unsplash API", font=("Helvetica", 10),
                            bg=style.colors.bg, fg=style.colors.secondary)
    footer_label.grid(row=3, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="nsew")

    # Make columns/rows expandable
    root.columnconfigure([0, 1], weight=1)
    root.rowconfigure(2, weight=1)
    root.mainloop()

if __name__ == '__main__':
    create_gui()
    