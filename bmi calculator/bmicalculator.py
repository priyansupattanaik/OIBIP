import tkinter as tk
from tkinter import messagebox, ttk
import csv

def calculate_bmi(event=None):
    try:
        name, weight, height = name_entry.get().strip(), float(weight_entry.get()), float(height_entry.get())
        bmi = round(weight / (height ** 2), 2)
        category = ("Underweight", "Normal weight", "Overweight", "Obese")[(bmi >= 18.5) + (bmi >= 24.9) + (bmi >= 29.9)]
        with open('bmidata.csv', 'a', newline='') as file:
            csv.writer(file).writerow([name, weight, height, bmi, category])
        messagebox.showinfo("BMI Result", f"Name: {name}\nBMI: {bmi}\nCategory: {category}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("BMI Calculator")
for i, label_text in enumerate(["Your Name", "Your Weight (kg)", "Your Height (m)"]):
    tk.Label(root, text=label_text).grid(row=i, column=0, padx=10, pady=10)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1, padx=10, pady=10)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="Calculate Your BMI", command=calculate_bmi).grid(row=3, column=0, columnspan=2, pady=20)
root.bind('<Return>', calculate_bmi)
root.mainloop()
