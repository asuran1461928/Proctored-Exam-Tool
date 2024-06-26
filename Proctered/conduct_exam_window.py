import tkinter as tk
import random
import sqlite3
import pyperclip  # Import pyperclip for copying text to clipboard

# Function to generate a random code
def generate_random_code():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=8))

# Function to store the generated code in the database
def store_code_in_database(code):
    conn = sqlite3.connect('exam_codes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS exam_codes (code TEXT PRIMARY KEY)''')
    c.execute("INSERT INTO exam_codes (code) VALUES (?)", (code,))
    conn.commit()
    conn.close()

def open_conduct_exam_window():
    def generate_code_and_open_exam():
        # Generate and store a random code
        code = generate_random_code()
        store_code_in_database(code)

        # Close the option window
        option_window.destroy()

        # Create a new window for conducting exams
        exam_window = tk.Toplevel()
        exam_window.title("Conduct Exam")
        exam_window.geometry("600x400")  # Set window size

        # Add exam-related widgets and functionality here
        exam_label = tk.Label(exam_window, text="Conduct Exam Window", font=("Arial", 18, "bold"))
        exam_label.pack(pady=20)

        code_label = tk.Label(exam_window, text="Exam Code: " + code, font=("Arial", 12))
        code_label.pack(pady=10)

        # Function to copy the code to clipboard
        def copy_code_to_clipboard():
            pyperclip.copy(code)
            messagebox.showinfo("Copy", "Code copied to clipboard!")

        # Copy button
        copy_button = tk.Button(exam_window, text="Copy", command=copy_code_to_clipboard, bg="lightgrey", fg="black", width=10, height=2, borderwidth=0, highlightthickness=0)
        copy_button.pack(pady=10)

        # Placeholder: Add exam-related widgets and functionality

        # Function to close the exam window
        def close_exam_window():
            exam_window.destroy()

        # Close button
        close_button = tk.Button(exam_window, text="Close", command=close_exam_window, bg="lightgrey", fg="black", width=10, height=2, borderwidth=0, highlightthickness=0)
        close_button.pack(pady=10)

    # Create a new window for exam options
    option_window = tk.Toplevel()
    option_window.title("Exam Options")
    option_window.geometry("600x400")  # Set window size

    # Add options for exam types
    option_label = tk.Label(option_window, text="Select Exam Type:", font=("Arial", 14))
    option_label.pack(pady=20)

    general_button = tk.Button(option_window, text="General Exam", command=generate_code_and_open_exam, bg="lightblue", fg="black", width=15, height=2, borderwidth=0, highlightthickness=0)
    general_button.pack(pady=5)

    premium_button = tk.Button(option_window, text="Premium Exam", command=generate_code_and_open_exam, bg="lightgreen", fg="black", width=15, height=2, borderwidth=0, highlightthickness=0)
    premium_button.pack(pady=5)

if __name__ == "__main__":
    open_conduct_exam_window()
