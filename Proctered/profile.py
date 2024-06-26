import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import sqlite3

# Connect to the database
connection = sqlite3.connect("user_profiles.db")
cursor = connection.cursor()

# Create a table to store user profiles if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS profiles (
                    username TEXT PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    email TEXT,
                    linkedin TEXT,
                    github TEXT
                )''')
connection.commit()

class ProfilePage(tk.Toplevel):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.title("Profile")
        self.geometry("800x600")
        self.username = username  # Store the username

        # Add profile editing content here
        profile_label = tk.Label(self, text="Profile Editing Page")
        profile_label.pack(pady=10)

        # Add a label for profile picture
        self.profile_picture_label = tk.Label(self, text="Profile Picture:")
        self.profile_picture_label.pack(pady=5)

        # Add a button to upload profile picture
        self.upload_button = tk.Button(self, text="Upload Picture", command=self.upload_picture)
        self.upload_button.pack(pady=5)

        # Add personal details section
        personal_details_label = tk.Label(self, text="Personal Details:")
        personal_details_label.pack(pady=10)

        # Add entry fields for personal details
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)

        self.age_label = tk.Label(self, text="Age:")
        self.age_label.pack()
        self.age_entry = tk.Entry(self)
        self.age_entry.pack(pady=5)

        self.email_label = tk.Label(self, text="Email:")
        self.email_label.pack()
        self.email_entry = tk.Entry(self)
        self.email_entry.pack(pady=5)

        self.linkedin_label = tk.Label(self, text="LinkedIn:")
        self.linkedin_label.pack()
        self.linkedin_entry = tk.Entry(self)
        self.linkedin_entry.pack(pady=5)

        self.github_label = tk.Label(self, text="GitHub:")
        self.github_label.pack()
        self.github_entry = tk.Entry(self)
        self.github_entry.pack(pady=5)

        # Initialize variables to store image data
        self.image = None
        self.image_label = None

        # Retrieve profile information
        self.retrieve_profile_info()

        # Add buttons for save, edit, and back
        self.save_button = tk.Button(self, text="Save", command=self.save_profile)
        self.save_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.edit_button = tk.Button(self, text="Edit", command=self.edit_profile)
        self.edit_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.back_button = tk.Button(self, text="Back", command=self.go_back)
        self.back_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Initially lock the profile fields
        self.lock_profile()

    def retrieve_profile_info(self):
        # Retrieve profile information from the database based on the username
        cursor.execute("SELECT name, age, email, linkedin, github FROM profiles WHERE username=?", (self.username,))
        user_info = cursor.fetchone()
        if user_info:
            # Display the retrieved information in the entry fields
            self.name_entry.insert(tk.END, user_info[0])
            self.age_entry.insert(tk.END, user_info[1])
            self.email_entry.insert(tk.END, user_info[2])
            self.linkedin_entry.insert(tk.END, user_info[3])
            self.github_entry.insert(tk.END, user_info[4])

    def upload_picture(self):
        # Open a file dialog to select a profile picture
        file_path = filedialog.askopenfilename()

        if file_path:
            # Open the image file using PIL
            image = Image.open(file_path)
            # Resize the image
            image = image.resize((200, 200), Image.LANCZOS)
            # Convert the image for Tkinter
            photo = ImageTk.PhotoImage(image)
            # Display the image on a label
            self.profile_picture_label.config(image=photo)
            self.profile_picture_label.image = photo  # Keep a reference to prevent garbage collection

    def save_profile(self):
        # Save profile information to the database
        name = self.name_entry.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        linkedin = self.linkedin_entry.get()
        github = self.github_entry.get()

        cursor.execute("INSERT OR REPLACE INTO profiles VALUES (?, ?, ?, ?, ?, ?)",
                       (self.username, name, age, email, linkedin, github))
        connection.commit()
        messagebox.showinfo("Success", "Profile information saved successfully.")
        self.lock_profile()  # Lock profile fields after saving

    def edit_profile(self):
        # Enable entry fields for editing
        self.name_entry.config(state=tk.NORMAL)
        self.age_entry.config(state=tk.NORMAL)
        self.email_entry.config(state=tk.NORMAL)
        self.linkedin_entry.config(state=tk.NORMAL)
        self.github_entry.config(state=tk.NORMAL)

        # Enable save button
        self.save_button.config(state=tk.NORMAL)

    def lock_profile(self):
        # Disable entry fields after saving
        self.name_entry.config(state=tk.DISABLED)
        self.age_entry.config(state=tk.DISABLED)
        self.email_entry.config(state=tk.DISABLED)
        self.linkedin_entry.config(state=tk.DISABLED)
        self.github_entry.config(state=tk.DISABLED)

        # Disable save button
        self.save_button.config(state=tk.DISABLED)

    def go_back(self):
        self.destroy()  # Destroy the profile page
        # Recreate the main page
        open_page()

def open_profile(root, username):
    # Destroy any existing profile pages
    for widget in root.winfo_children():
        if isinstance(widget, ProfilePage):
            widget.destroy()
    # Open the profile page
    profile_window = ProfilePage(root, username)

def open_page():
    # Recreate the main page content here
    root = tk.Tk()
    root.title("Blank Page")  # Update title if needed
    header_label = tk.Label(root, text="Welcome to Your Page", font=("Arial", 18, "bold"))
    header_label.pack(pady=20)
    # Add other widgets and layout for the main page as needed

if __name__ == "__main__":
    root = tk.Tk()
    # Replace 'test_user' with the actual logged-in user's username
    open_profile(root, 'test_user')
    root.mainloop()
