import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import os

def caesar_cipher_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_amount = shift % 26
            if char.islower():
                start = ord('a')
                encrypted_text += chr((ord(char) - start + shift_amount) % 26 + start)
            elif char.isupper():
                start = ord('A')
                encrypted_text += chr((ord(char) - start + shift_amount) % 26 + start)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_cipher_decrypt(text, shift):
    return caesar_cipher_encrypt(text, -shift)

def encrypt_message():
    message = message_entry.get()
    try:
        shift = int(shift_entry.get())
        if not message:
            messagebox.showerror("Input Error", "Message cannot be empty.")
            return
        encrypted_message = caesar_cipher_encrypt(message, shift)
        result_text.insert(tk.END, f"Encrypted: {encrypted_message}\n")
        save_history(f"Encrypted: {encrypted_message}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Shift value must be an integer.")

def decrypt_message():
    message = message_entry.get()
    try:
        shift = int(shift_entry.get())
        if not message:
            messagebox.showerror("Input Error", "Message cannot be empty.")
            return
        decrypted_message = caesar_cipher_decrypt(message, shift)
        result_text.insert(tk.END, f"Decrypted: {decrypted_message}\n")
        save_history(f"Decrypted: {decrypted_message}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Shift value must be an integer.")

def save_history(data):
    with open("history.txt", "a") as file:
        file.write(data + "\n")

def load_history():
    if os.path.exists("history.txt"):
        with open("history.txt", "r") as file:
            history = file.read()
        result_text.insert(tk.END, history)
    else:
        result_text.insert(tk.END, "No history found.\n")

def clear_history():
    if messagebox.askyesno("Clear History", "Are you sure you want to clear the history?"):
        open("history.txt", "w").close()
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "History cleared.\n")

def clear_inputs():
    message_entry.delete(0, tk.END)
    shift_entry.delete(0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Caesar Cipher")

# Set the background color
root.configure(bg="#e0f7fa")

frame = tk.Frame(root, bg="#e0f7fa")
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Message:", bg="#e0f7fa", fg="#00796b", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky=tk.E, pady=5)
message_entry = tk.Entry(frame, width=50, font=("Arial", 12))
message_entry.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Shift:", bg="#e0f7fa", fg="#00796b", font=("Arial", 12, "bold")).grid(row=1, column=0, sticky=tk.E, pady=5)
shift_entry = tk.Entry(frame, width=10, font=("Arial", 12))
shift_entry.grid(row=1, column=1, sticky=tk.W, padx=5)

button_frame = tk.Frame(root, bg="#e0f7fa")
button_frame.pack(pady=10)

encrypt_button = tk.Button(button_frame, text="Encrypt", command=encrypt_message, bg="#00796b", fg="white", font=("Arial", 12, "bold"))
encrypt_button.grid(row=0, column=0, padx=5)

decrypt_button = tk.Button(button_frame, text="Decrypt", command=decrypt_message, bg="#00796b", fg="white", font=("Arial", 12, "bold"))
decrypt_button.grid(row=0, column=1, padx=5)

clear_button = tk.Button(button_frame, text="Clear Inputs", command=clear_inputs, bg="#00796b", fg="white", font=("Arial", 12, "bold"))
clear_button.grid(row=0, column=2, padx=5)

history_button = tk.Button(button_frame, text="Clear History", command=clear_history, bg="#00796b", fg="white", font=("Arial", 12, "bold"))
history_button.grid(row=0, column=3, padx=5)

result_frame = tk.Frame(root, bg="#e0f7fa")
result_frame.pack(padx=10, pady=10)

result_text = scrolledtext.ScrolledText(result_frame, width=60, height=20, font=("Arial", 12))
result_text.pack()

# Load history on startup
load_history()

root.mainloop()
