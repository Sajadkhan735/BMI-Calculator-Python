import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Database Setup ---
def init_db():
    try:
        conn = sqlite3.connect("bmi_database.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                weight REAL NOT NULL,
                height REAL NOT NULL,
                bmi REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to initialize database: {e}")

# --- BMI Logic ---
def calculate_bmi(weight, height):
    return weight / (height ** 2)

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight", "#3498db" # Blue
    elif 18.5 <= bmi <= 24.9:
        return "Normal", "#2ecc71"      # Green
    elif 25.0 <= bmi <= 29.9:
        return "Overweight", "#f39c12"  # Orange
    else:
        return "Obese", "#e74c3c"       # Red

# --- Main Application GUI ---
class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator & Tracker")
        self.root.geometry("500x550+100+50")
        self.root.config(bg="#f8f9fa")

        # Title Label
        title_label = tk.Label(root, text="Health & BMI Tracker", font=("Arial", 18, "bold"), bg="#f8f9fa", fg="#333333")
        title_label.pack(pady=15)

        # Input Frame
        input_frame = tk.Frame(root, bg="#f8f9fa")
        input_frame.pack(pady=10)

        # User Name
        tk.Label(input_frame, text="User Name:", font=("Arial", 11), bg="#f8f9fa").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.name_entry = tk.Entry(input_frame, font=("Arial", 11), width=18)
        self.name_entry.grid(row=0, column=1, pady=5, padx=5)

        # Weight
        tk.Label(input_frame, text="Weight (kg):", font=("Arial", 11), bg="#f8f9fa").grid(row=1, column=0, sticky="w", pady=5, padx=5)
        self.weight_entry = tk.Entry(input_frame, font=("Arial", 11), width=18)
        self.weight_entry.grid(row=1, column=1, pady=5, padx=5)

        # Height
        tk.Label(input_frame, text="Height (m):", font=("Arial", 11), bg="#f8f9fa").grid(row=2, column=0, sticky="w", pady=5, padx=5)
        self.height_entry = tk.Entry(input_frame, font=("Arial", 11), width=18)
        self.height_entry.grid(row=2, column=1, pady=5, padx=5)

        # Buttons Frame
        btn_frame = tk.Frame(root, bg="#f8f9fa")
        btn_frame.pack(pady=15)

        calc_btn = tk.Button(btn_frame, text="Calculate & Save", font=("Arial", 11, "bold"), bg="#2ecc71", fg="white", width=15, command=self.process_bmi)
        calc_btn.grid(row=0, column=0, padx=5)

        graph_btn = tk.Button(btn_frame, text="View Trend Graph", font=("Arial", 11, "bold"), bg="#3498db", fg="white", width=15, command=self.show_trend_graph)
        graph_btn.grid(row=0, column=1, padx=5)

        # Result Display Area
        self.result_frame = tk.Frame(root, bg="#ffffff", bd=2, relief="groove")
        self.result_frame.pack(pady=10, fill="x", padx=30)

        self.result_label = tk.Label(self.result_frame, text="Enter details and click Calculate", font=("Arial", 12), bg="#ffffff", fg="#555555")
        self.result_label.pack(pady=15)

    def process_bmi(self):
        name = self.name_entry.get().strip()
        weight_str = self.weight_entry.get().strip()
        height_str = self.height_entry.get().strip()

        # Validation
        if not name:
            messagebox.showerror("Error", "Please enter a user name.")
            return

        try:
            weight = float(weight_str)
            height = float(height_str)
            if weight <= 0 or height <= 0:
                raise ValueError("Values must be greater than zero.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numeric values for weight and height.")
            return

        # Calculation
        bmi = calculate_bmi(weight, height)
        category, color = classify_bmi(bmi)
        date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Save to Database
        try:
            conn = sqlite3.connect("bmi_database.db")
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO records (username, weight, height, bmi, category, date)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, weight, height, round(bmi, 2), category, date_str))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not save record: {e}")
            return

        # Display Result on GUI
        self.result_label.config(
            text=f"User: {name}\nBMI: {bmi:.2f}\nCategory: {category}",
            fg=color
        )

    def show_trend_graph(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a user name to view their trend graph.")
            return

        try:
            conn = sqlite3.connect("bmi_database.db")
            cursor = conn.cursor()
            cursor.execute("SELECT date, bmi FROM records WHERE username = ? ORDER BY id ASC", (name,))
            rows = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not retrieve records: {e}")
            return

        if not rows:
            messagebox.showinfo("No Data", f"No historical records found for user '{name}'.")
            return

        dates = [row[0] for row in rows]
        bmis = [row[1] for row in rows]

        # Plotting with Matplotlib inside a new Toplevel Window
        graph_window = tk.Toplevel(self.root)
        graph_window.title(f"BMI Trend - {name}")
        graph_window.geometry("600x400+100+50")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(dates, bmis, marker="o", color="#2c3e50", linestyle="-", linewidth=2)
        ax.set_title(f"BMI Progress Over Time ({name})")
        ax.set_xlabel("Date")
        ax.set_ylabel("BMI Value")
        plt.xticks(rotation=45, ha="right")
        ax.grid(True, linestyle="--", alpha=0.6)
        fig.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- Run Application ---
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()