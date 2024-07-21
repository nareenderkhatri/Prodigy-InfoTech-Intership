import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

def key_to_int(key):
    return sum(ord(char) for char in key)

def encrypt_image(image_path, key):
    image = Image.open(image_path)
    pixels = image.load()
    key_int = key_to_int(key)

    for i in range(image.width):
        for j in range(image.height):
            pixel = pixels[i, j]
            if len(pixel) == 3:  # RGB
                r, g, b = pixel
                pixels[i, j] = ((r + key_int) % 256, (g + key_int) % 256, (b + key_int) % 256)
            elif len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
                pixels[i, j] = ((r + key_int) % 256, (g + key_int) % 256, (b + key_int) % 256, a)

    encrypted_path = "encrypted_" + os.path.basename(image_path)
    image.save(encrypted_path)
    return encrypted_path

def decrypt_image(image_path, key):
    image = Image.open(image_path)
    pixels = image.load()
    key_int = key_to_int(key)

    for i in range(image.width):
        for j in range(image.height):
            pixel = pixels[i, j]
            if len(pixel) == 3:  # RGB
                r, g, b = pixel
                pixels[i, j] = ((r - key_int) % 256, (g - key_int) % 256, (b - key_int) % 256)
            elif len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
                pixels[i, j] = ((r - key_int) % 256, (g - key_int) % 256, (b - key_int) % 256, a)

    decrypted_path = "decrypted_" + os.path.basename(image_path)
    image.save(decrypted_path)
    return decrypted_path

def load_image(path):
    image = Image.open(path)
    image.thumbnail((300, 300))
    return ImageTk.PhotoImage(image)

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        global original_image_path
        original_image_path = file_path
        img = load_image(file_path)
        original_image_label.config(image=img, text="")
        original_image_label.image = img

def encrypt_action():
    if original_image_path:
        key = key_entry.get()
        if not key:
            messagebox.showerror("Input Error", "Key cannot be empty.")
            return
        global encrypted_image_path
        encrypted_image_path = encrypt_image(original_image_path, key)
        img = load_image(encrypted_image_path)
        encrypted_image_label.config(image=img, text="")
        encrypted_image_label.image = img
    else:
        messagebox.showerror("File Error", "No image file selected.")

def decrypt_action():
    if original_image_path:
        key = key_entry.get()
        if not key:
            messagebox.showerror("Input Error", "Key cannot be empty.")
            return
        decrypted_path = decrypt_image(original_image_path, key)
        img = load_image(decrypted_path)
        encrypted_image_label.config(image=img, text="")
        encrypted_image_label.image = img
    else:
        messagebox.showerror("File Error", "No image file selected.")

def download_image():
    if encrypted_image_path:
        download_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"),
                                                                ("JPEG files", "*.jpg;*.jpeg"),
                                                                ("All files", "*.*")])
        if download_path:
            os.rename(encrypted_image_path, download_path)
            messagebox.showinfo("Success", "File downloaded successfully!")
    else:
        messagebox.showerror("File Error", "No encrypted image to download.")

# GUI setup
root = tk.Tk()
root.title("Image Encryption Tool")

# Set the background color
root.configure(bg="#ecf0f1")

frame = tk.Frame(root, bg="#ecf0f1")
frame.pack(padx=10, pady=10)

original_image_label = tk.Label(frame, text="Original Image", bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 14))
original_image_label.grid(row=0, column=0, padx=10, pady=10)

encrypted_image_label = tk.Label(frame, text="Encrypted/Decrypted Image", bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 14))
encrypted_image_label.grid(row=0, column=1, padx=10, pady=10)

load_button = tk.Button(root, text="Load Image", command=open_file, bg="#3498db", fg="white", font=("Helvetica", 12))
load_button.pack(pady=5)

key_frame = tk.Frame(root, bg="#ecf0f1")
key_frame.pack(pady=5)

tk.Label(key_frame, text="Key:", bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 12)).pack(side=tk.LEFT)
key_entry = tk.Entry(key_frame, width=20, font=("Helvetica", 12))
key_entry.pack(side=tk.LEFT)

button_frame = tk.Frame(root, bg="#ecf0f1")
button_frame.pack(pady=10)

encrypt_button = tk.Button(button_frame, text="Encrypt", command=encrypt_action, bg="#e74c3c", fg="white", font=("Helvetica", 12))
encrypt_button.grid(row=0, column=0, padx=5)

decrypt_button = tk.Button(button_frame, text="Decrypt", command=decrypt_action, bg="#2ecc71", fg="white", font=("Helvetica", 12))
decrypt_button.grid(row=0, column=1, padx=5)

download_button = tk.Button(button_frame, text="Download Encrypted Image", command=download_image, bg="#f39c12", fg="white", font=("Helvetica", 12))
download_button.grid(row=0, column=2, padx=5)

original_image_path = None
encrypted_image_path = None

root.mainloop()
