import tkinter as tk
from tkinter import messagebox
import sqlite3
import re
import os
import datetime

# Create a SQLite database connection
conn = sqlite3.connect('user_accounts.db')
cursor = conn.cursor()

# Create a table to store user accounts if not exists
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT UNIQUE,
                    phone TEXT UNIQUE,
                    username TEXT UNIQUE,
                    password TEXT
                  )''')
conn.commit()

# Function to log user actions
def log_action(action):
    with open('user_actions.log', 'a') as f:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'{timestamp}: {action}\n')

# Function to create user-specific databases
def create_user_database(username):
    conn = sqlite3.connect(f'{username}_data.db')
    cursor = conn.cursor()
    # Create tables or schema for user-specific data
    cursor.execute('''CREATE TABLE IF NOT EXISTS user_data (
                        id INTEGER PRIMARY KEY,
                        action TEXT,
                        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                      )''')
    conn.commit()
    conn.close()

# Function to log user actions to their database
def log_user_action(username, action):
    conn = sqlite3.connect(f'{username}_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_data (action) VALUES (?)", (action,))
    conn.commit()
    conn.close()

def on_enter_login(event):
    login_button.config(bg='green')

def on_leave_login(event):
    login_button.config(bg='red')

def on_enter_create(event):
    create_account_button.config(bg='yellow')

def on_leave_create(event):
    create_account_button.config(bg='blue')

def validate_email(email):
    # Email validation regex
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email)

def validate_phone(phone):
    # Phone number validation regex
    regex = r'^\d{10}$'
    return re.match(regex, phone)

def validate_password_strength(password):
    # Password strength checking logic
    if len(password) < 6:
        return "Weak"
    elif len(password) < 10:
        return "Medium"
    else:
        return "Strong"

def validate_login():
    username = username_entry.get().strip().lower()
    password = password_entry.get().strip()

    if not username or not password:  # Check if username or password is empty
        messagebox.showerror("Login Failed", "Please enter username and password.")
        return

    # Check if username and password are correct
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    if user and user[6] == password:
        messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        log_action(f'User {username} logged in')
        root.destroy()  # Close the login window
        open_blank_page(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def open_blank_page(username):
    os.system(f"python blank_page_creator.py {username}")

def create_account():
    def navigate_to_login():
        account_window.destroy()  # Close the account creation window
        root.deiconify()          # Show the main login window

    def insert_user():
        first_name = first_name_entry.get()
        last_name = last_name_entry.get()
        email = email_entry.get()
        phone = phone_entry.get()
        username = username_entry.get().strip().lower()
        password = password_entry.get()
        confirm_password = confirm_password_entry.get()

        # Validations
        if not (first_name and last_name and email and phone and username and password and confirm_password):
            messagebox.showerror("Incomplete Information", "All fields marked with '*' are required.")
            return
        if not validate_email(email):
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return
        if not validate_phone(phone):
            messagebox.showerror("Invalid Phone Number", "Please enter a valid 10-digit phone number.")
            return
        if password != confirm_password:
            messagebox.showerror("Password Mismatch", "Passwords do not match. Please re-enter.")
            return

        password_strength = validate_password_strength(password)

        # Database insertion
        try:
            cursor.execute("INSERT INTO users (first_name, last_name, email, phone, username, password) VALUES (?, ?, ?, ?, ?, ?)",
                           (first_name, last_name, email, phone, username, password))
            conn.commit()
            messagebox.showinfo("Account Created", f"Account created successfully! Password strength: {password_strength}")
            create_user_database(username)  # Create user-specific database
            log_action(f'User {username} created an account')
            navigate_to_login()
        except sqlite3.IntegrityError as e:
            messagebox.showerror("Account Creation Failed", str(e))

    # Create a new window for account creation
    account_window = tk.Toplevel(root)
    account_window.title("Create Account")

    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set fixed size for the window
    window_width = 600
    window_height = 530  # Increased height to accommodate the checkbox
    window_x = (screen_width - window_width) // 2
    window_y = (screen_height - window_height) // 2
    account_window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

    # Personal Information Tab
    first_name_label = tk.Label(account_window, text="First Name*:")
    first_name_label.grid(row=0, column=0, padx=5, pady=5)
    first_name_entry = tk.Entry(account_window)
    first_name_entry.grid(row=0, column=1, padx=5, pady=5)

    last_name_label = tk.Label(account_window, text="Last Name*:")
    last_name_label.grid(row=1, column=0, padx=5, pady=5)
    last_name_entry = tk.Entry(account_window)
    last_name_entry.grid(row=1, column=1, padx=5, pady=5)

    email_label = tk.Label(account_window, text="Email*:")
    email_label.grid(row=2, column=0, padx=5, pady=5)
    email_entry = tk.Entry(account_window)
    email_entry.grid(row=2, column=1, padx=5, pady=5)

    phone_label = tk.Label(account_window, text="Phone Number*:")
    phone_label.grid(row=3, column=0, padx=5, pady=5)
    phone_entry = tk.Entry(account_window)
    phone_entry.grid(row=3, column=1, padx=5, pady=5)

    # Login Information Tab
    username_label = tk.Label(account_window, text="Username*:")
    username_label.grid(row=0, column=2, padx=5, pady=5)
    username_entry = tk.Entry(account_window)
    username_entry.grid(row=0, column=3, padx=5, pady=5)

    password_label = tk.Label(account_window, text="Password*:")
    password_label.grid(row=1, column=2, padx=5, pady=5)
    password_entry = tk.Entry(account_window, show="*")
    password_entry.grid(row=1, column=3, padx=5, pady=5)

    confirm_password_label = tk.Label(account_window, text="Confirm Password*:")
    confirm_password_label.grid(row=2, column=2, padx=5, pady=5)
    confirm_password_entry = tk.Entry(account_window, show="*")
    confirm_password_entry.grid(row=2, column=3, padx=5, pady=5)

    # Terms and Conditions Checkbox
    terms_var = tk.BooleanVar()
    terms_check = tk.Checkbutton(account_window, text="I accept the terms and conditions", variable=terms_var)
    terms_check.grid(row=3, column=2, columnspan=2, pady=5)

    # Create Account button
    create_account_button = tk.Button(account_window, text="Create Account", command=insert_user)
    create_account_button.grid(row=4, column=2, columnspan=2, pady=5)
    create_account_button.bind("<Enter>", on_enter_create)
    create_account_button.bind("<Leave>", on_leave_create)

    # Run the main event loop for account creation window
    account_window.mainloop()

# Create main window
root = tk.Tk()
root.title("Login Page")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set fixed size for the window
window_width = 600
window_height = 450
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Username label and entry
username_label = tk.Label(root, text="Username:", font=("Arial", 12))
username_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
username_entry = tk.Entry(root)
username_entry.place(relx=0.5, rely=0.45, anchor=tk.CENTER)

# Password label and entry
password_label = tk.Label(root, text="Password:", font=("Arial", 12))
password_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
password_entry = tk.Entry(root, show="*")
password_entry.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

# Login button
login_button = tk.Button(root, text="Login", command=validate_login, font=("Arial", 12))
login_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
login_button.bind("<Enter>", on_enter_login)
login_button.bind("<Leave>", on_leave_login)

# Text label for creating account
create_account_text = tk.Label(root, text="If you don't have an account:", font=("Arial", 12))
create_account_text.place(relx=0.5, rely=0.65, anchor=tk.CENTER)

# Create Account button
create_account_button = tk.Button(root, text="Create Account", command=create_account, font=("Arial", 12))
create_account_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)
create_account_button.bind("<Enter>", on_enter_create)
create_account_button.bind("<Leave>", on_leave_create)

# Run the main event loop
root.mainloop()
