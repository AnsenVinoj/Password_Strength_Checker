import re
import tkinter as tk
from tkinter import messagebox, scrolledtext

def evaluate_password(password):
    COMMON_DICT_WORDS = ['password', 'admin', '123456', 'qwerty', 'letmein']
    BREACHED_PASSWORDS = ['123456', 'password', '123456789', '12345678', 'qwerty']

    suggestions = []
    score = 0
    password_lower = password.lower()

    if len(password)>12:
        score +=2
    elif len(password) >= 8:
        score += 1
    else:
        suggestions.append("Increase password length to at least 8 characters.")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        suggestions.append("Add at least one uppercase letter.")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        suggestions.append("Add at least one lowercase letter.")

    if re.search(r'\d', password):
        score += 1
    else:
        suggestions.append("Include at least one digit.")

    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        suggestions.append("Use at least one special character / Symbols.")

    
    if any(word in password_lower for word in COMMON_DICT_WORDS):
        suggestions.append("Avoid using common dictionary words.")
        score -= 1

    if password_lower in BREACHED_PASSWORDS:
        suggestions.append("This password is in known breached lists. Choose a different one.")
        score = 0

    if score >= 6:
        strength = "Strong"
    elif 4 <= score < 6:
        strength = "Moderate"
    else:
        strength = "Weak"

    return strength, suggestions




def check_password():
    password = password_entry.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    strength, suggestions = evaluate_password(password)

    result_label.config(text=f"Strength: {strength}", fg=("green" if strength == "Strong" else "orange" if strength == "Moderate" else "red"))
    
    suggestions_box.delete(1.0, tk.END)
    if suggestions:
        for suggestion in suggestions:
            suggestions_box.insert(tk.END, f"- {suggestion}\n")
    else:
        suggestions_box.insert(tk.END, "Great job! Your password is strong.")



root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x400")
root.resizable(False, False)

tk.Label(root, text="Enter Password:", font=("Arial", 12)).pack(pady=10)
password_entry = tk.Entry(root, width=40, show="*", font=("Arial", 12))
password_entry.pack()

tk.Button(root, text="Check Strength", command=check_password, font=("Arial", 12), bg="blue", fg="white").pack(pady=10)

result_label = tk.Label(root, text="Strength: ", font=("Arial", 14))
result_label.pack(pady=5)

tk.Label(root, text="Suggestions:", font=("Arial", 12)).pack()
suggestions_box = scrolledtext.ScrolledText(root, width=50, height=10, font=("Arial", 10))
suggestions_box.pack(pady=5)

root.mainloop()
