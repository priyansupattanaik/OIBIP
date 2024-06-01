import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import csv

def calculate_bmi():
    try:
        name, weight, height = name_entry.get().strip(), float(weight_entry.get()), float(height_entry.get())
        if not name or weight <= 0 or height <= 0:
            raise ValueError("Please enter a valid name, weight, and height.")

        bmi = round(weight / (height ** 2), 2)
        category = ("Underweight" if bmi < 18.5 else "Normal weight" if bmi < 24.9 else "Overweight" if bmi < 29.9 else "Obese")

        with open('bmidata.csv', 'a', newline='') as file:
            csv.writer(file).writerow([name, weight, height, bmi, category])

        messagebox.showinfo("BMI Result", f"Name: {name}\nBMI: {bmi}\nCategory: {category}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_bmi_history():
    def clear_history():
        if messagebox.askyesno("Clear History", "Are you sure you want to clear the entire history?"):
            open('bmidata.csv', 'w').close()
            for item in tree.get_children():
                tree.delete(item)
            messagebox.showinfo("History Cleared", "BMI history has been cleared.")

    try:
        with open('bmidata.csv', 'r') as file:
            history_data = [row for row in csv.reader(file) if len(row) == 5]
        if not history_data:
            messagebox.showwarning("No Data", "No BMI data found.")
            return

        history_window = Toplevel(root)
        history_window.title("BMI History")

        tree = ttk.Treeview(history_window, columns=('Name', 'Weight', 'Height', 'BMI', 'Category'), show='headings')
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for row in history_data:
            tree.insert('', tk.END, values=row)

        tree.pack(fill=tk.BOTH, expand=True)
        ttk.Scrollbar(history_window, orient=tk.VERTICAL, command=tree.yview).pack(side=tk.RIGHT, fill=tk.Y)
        tk.Button(history_window, text="Clear History", command=clear_history).pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", str(e))

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("400x300")

tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=10)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Weight (kg)").grid(row=1, column=0, padx=10, pady=10)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Height (m)").grid(row=2, column=0, padx=10, pady=10)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1, padx=10, pady=10)

tk.Button(root, text="Calculate BMI", command=calculate_bmi).grid(row=3, column=0, columnspan=2, pady=20)
tk.Button(root, text="View BMI History", command=show_bmi_history).grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()