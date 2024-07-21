import tkinter as tk
import re
import random
import string

def assess_password_strength(password):
    strength_criteria = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "digits": bool(re.search(r'\d', password)),
        "special_characters": bool(re.search(r'[@$!%*?&#]', password))
    }
    
    strength_levels = {
        5: "Very Strong",
        4: "Strong",
        3: "Moderate",
        2: "Weak",
        1: "Very Weak",
        0: "Very Weak"
    }
    
    score = sum(strength_criteria.values())
    return strength_levels[score], strength_criteria

def check_password():
    password = password_entry.get()
    strength, criteria = assess_password_strength(password)
    
    criteria_feedback = (
        f"Length (>= 8 characters): {'✓' if criteria['length'] else '✗'}\n"
        f"Uppercase Letter: {'✓' if criteria['uppercase'] else '✗'}\n"
        f"Lowercase Letter: {'✓' if criteria['lowercase'] else '✗'}\n"
        f"Digits: {'✓' if criteria['digits'] else '✗'}\n"
        f"Special Characters (@$!%*?&#): {'✓' if criteria['special_characters'] else '✗'}"
    )
    
    strength_label.config(text=f"Password Strength: {strength}")
    criteria_label.config(text=criteria_feedback)
    
    if strength in ["Very Weak", "Weak"]:
        suggestion = generate_strong_password()
        suggestion_label.config(text=f"Suggested Password: {suggestion}")
    else:
        suggestion_label.config(text="")

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def toggle_password_visibility():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        toggle_button.config(text="Hide Password")
    else:
        password_entry.config(show='*')
        toggle_button.config(text="Show Password")

# GUI setup
root = tk.Tk()
root.title("Password Strength Checker")

# Set the background color
root.configure(bg="#ecf0f1")

frame = tk.Frame(root, bg="#ecf0f1")
frame.pack(padx=10, pady=10)

# Title Label
title_label = tk.Label(frame, text="Password Strength Checker", bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, columnspan=3, pady=(0, 20))

# Password Entry
tk.Label(frame, text="Enter Password:", bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 12 , "bold")).grid(row=1, column=0, pady=5)
password_entry = tk.Entry(frame, width=30, show='*', font=("Helvetica", 12))
password_entry.grid(row=1, column=1, pady=5)

# Toggle Password Visibility Button
toggle_button = tk.Button(frame, text="Show Password", command=toggle_password_visibility, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
toggle_button.grid(row=1, column=2, padx=4)

# Check Button
check_button = tk.Button(frame, text="Check Strength", command=check_password, bg="#3498db", fg="white", font=("Helvetica", 12, "bold"))
check_button.grid(row=2, columnspan=3, pady=10)

# Password Strength Label
strength_label = tk.Label(frame, text="", bg="#ecf0f1", fg="#e74c3c", font=("Helvetica", 16, "bold"))
strength_label.grid(row=3, columnspan=3, pady=(10, 0))

# Criteria Feedback Label
criteria_label = tk.Label(frame, text="", bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 12))
criteria_label.grid(row=4, columnspan=3, pady=(0, 10))

# Suggested Password Label
suggestion_label = tk.Label(frame, text="", bg="#ecf0f1", fg="#2c3e50", font=("Helvetica", 12, "italic"))
suggestion_label.grid(row=5, columnspan=3, pady=(0, 10))

root.mainloop()
