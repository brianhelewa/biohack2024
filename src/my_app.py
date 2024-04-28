import tkinter as tk
from PIL import Image, ImageTk

def create_window():
    root = tk.Tk()
    root.title("Figma Design Display")

    # Adjust the path below to match the location and name of your exported Figma design
    image_path = 'data/OcEsda.png'
    img = Image.open(image_path)
    tk_img = ImageTk.PhotoImage(img)

    # Resize the image using the LANCZOS filter
    img = img.resize((1800, 1000), Image.Resampling.LANCZOS)  # Resize to 300x200 pixels using high-quality downsampling

    # Convert the image to a format that Tkinter can use
    tk_img = ImageTk.PhotoImage(img)


    # Create a label to display the image
    label = tk.Label(root, image=tk_img)
    label.image = tk_img  # Keep a reference to avoid garbage collection
    label.pack()

    root.mainloop()

if __name__ == "__main__":
    create_window()
