import random
import string
import tkinter as tk
from tkinter import messagebox
import pyperclip

def generate_password():
    try:
        length = int(length_entry.get())
        password = generate(length, uppercase_var.get(), numbers_var.get(), symbols_var.get(), exclude_entry.get())
        result_label.config(text=password)
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

def generate(length, include_uppercase, include_numbers, include_symbols, exclude_chars=""):
    character_set = string.ascii_lowercase
    if include_uppercase:
        character_set += string.ascii_uppercase
    if include_numbers:
        character_set += string.digits
    if include_symbols:
        character_set += string.punctuation

    character_set = ''.join(c for c in character_set if c not in exclude_chars)

    if length < 1:
        raise ValueError("Password length must be at least 1")

    while True:
        password = ''.join(random.choice(character_set) for _ in range(length))
        if (any(c.islower() for c in password) and 
            (not include_uppercase or any(c.isupper() for c in password)) and
            (not include_numbers or any(c.isdigit() for c in password)) and
            (not include_symbols or any(c in string.punctuation for c in password))):
            break

    return password

def copy_to_clipboard():
    pyperclip.copy(result_label.cget("text"))
    messagebox.showinfo("Copied", "Password copied to clipboard!")

def on_enter(event):
    generate_password()

app = tk.Tk()
app.title("Password Generator")
app.geometry("400x300")
app.resizable(False, False)

frame = tk.Frame(app, padx=10, pady=10)
frame.pack(expand=True)

tk.Label(frame, text="Password Length:").grid(row=0, column=0, sticky="w")
length_entry = tk.Entry(frame, width=10)
length_entry.grid(row=0, column=1, pady=5)
length_entry.bind("<Return>", on_enter)

uppercase_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Include Uppercase", variable=uppercase_var).grid(row=1, column=0, columnspan=2, sticky="w")

numbers_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Include Numbers", variable=numbers_var).grid(row=2, column=0, columnspan=2, sticky="w")

symbols_var = tk.BooleanVar()
tk.Checkbutton(frame, text="Include Symbols", variable=symbols_var).grid(row=3, column=0, columnspan=2, sticky="w")

tk.Label(frame, text="Exclude Characters:").grid(row=4, column=0, sticky="w")
exclude_entry = tk.Entry(frame, width=10)
exclude_entry.grid(row=4, column=1, pady=5)

tk.Button(frame, text="Generate Password", command=generate_password).grid(row=5, column=0, columnspan=2, pady=10)

result_label = tk.Label(frame, text="", wraplength=300, justify="center")
result_label.grid(row=6, column=0, columnspan=2)

tk.Button(frame, text="Copy to Clipboard", command=copy_to_clipboard).grid(row=7, column=0, columnspan=2, pady=5)

app.mainloop()
