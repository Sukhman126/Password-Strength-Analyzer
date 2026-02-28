import tkinter as tk
from tkinter import ttk
import re
import random
import string
import math

# Common passwords list (sample)
common_passwords = {"123456", "password", "12345678", "qwerty", "abc123"}

def calculate_entropy(password):
    pool = 0
    if re.search(r'[a-z]', password):
        pool += 26
    if re.search(r'[A-Z]', password):
        pool += 26
    if re.search(r'\d', password):
        pool += 10
    if re.search(r'[!@#$%^&*(),.?":{|}<>]', password):
        pool += 32
    if pool == 0:
        return 0
    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)

def update_strength(event=None):
    password = password_var.get()
    
    criteria = {
        'length': len(password) >= 8,
        'upper': bool(re.search(r'[A-Z]', password)),
        'lower': bool(re.search(r'[a-z]', password)),
        'digit': bool(re.search(r'\d', password)),
        'special': bool(re.search(r'[!@#$%^&*(),.?":{|}<>]', password))
    }

    score = sum(criteria.values())
    
    # Common password check
    if password.lower() in common_passwords:
        strength_label.config(text="❌ Very Weak - Common Password!", fg="red")
        progress['value'] = 10
        return

    # Entropy
    entropy = calculate_entropy(password)

    # Strength logic
    if entropy > 60 and score == 5:
        strength = "Strong Password 💪"
        color = "green"
        progress['value'] = 100
    elif entropy > 40:
        strength = "Moderate Password 🙂"
        color = "orange"
        progress['value'] = 70
    else:
        strength = "Weak Password ⚠"
        color = "red"
        progress['value'] = 40

    strength_label.config(text=f"{strength}\nEntropy: {entropy} bits", fg=color)

    # Suggestions
    suggestions = [
        f"{'✅' if criteria['length'] else '❌'} At least 8 characters",
        f"{'✅' if criteria['upper'] else '❌'} Uppercase letter (A-Z)",
        f"{'✅' if criteria['lower'] else '❌'} Lowercase letter (a-z)",
        f"{'✅' if criteria['digit'] else '❌'} Number (0-9)",
        f"{'✅' if criteria['special'] else '❌'} Special character (!@#$%)"
    ]

    suggestions_label.config(text="\n".join(suggestions))

def toggle_visibility():
    if show_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")

def generate_password():
    length = 12
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"
    generated = ''.join(random.choice(characters) for _ in range(length))
    password_var.set(generated)
    update_strength()

# GUI Setup
root = tk.Tk()
root.title("Advanced Password Strength Analyzer")
root.geometry("520x500")
root.resizable(False, False)

tk.Label(root, text="🔐 Password Strength Analyzer", 
         font=("Arial", 16, "bold")).pack(pady=20)

password_var = tk.StringVar()

tk.Label(root, text="Enter Password:", font=("Arial", 12)).pack()
password_entry = tk.Entry(root, textvariable=password_var,
                          width=40, show="*", font=("Arial", 12))
password_entry.pack(pady=10)
password_entry.bind('<KeyRelease>', update_strength)

show_var = tk.BooleanVar()
tk.Checkbutton(root, text="Show Password",
               variable=show_var,
               command=toggle_visibility).pack()

ttk.Label(root, text="Strength Level:").pack(pady=(15,5))
progress = ttk.Progressbar(root, length=350, mode='determinate')
progress.pack(pady=5)

tk.Button(root, text="Generate Secure Password 🔑",
          command=generate_password,
          bg="#2ecc71", fg="white").pack(pady=10)

strength_label = tk.Label(root,
                          text="Start typing to analyze...",
                          font=("Arial", 13, "bold"))
strength_label.pack(pady=10)

tk.Label(root, text="Security Criteria:",
         font=("Arial", 12, "bold")).pack(anchor=tk.W, padx=20)

suggestions_label = tk.Label(root,
                             text="Waiting for input...",
                             justify=tk.LEFT,
                             wraplength=480)
suggestions_label.pack(padx=20, pady=5)

root.mainloop()