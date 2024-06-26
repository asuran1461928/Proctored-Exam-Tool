import tkinter as tk
from tkinter import messagebox, simpledialog
from profile import open_profile
from mcq_page import MCQPracticePage
from coding_practice_page import CodingPracticePage
from conduct_exam_window import open_conduct_exam_window
from write_exam_window import open_write_exam_window

# Function to open the blank_page_creator.py
def open_blank_page_creator():
    import subprocess
    subprocess.Popen(["python", "blank_page_creator.py"])

# Function to create square buttons with different colors
def create_round_button(parent, text, command, bg_color, fg_color):
    button = tk.Button(parent, text=text, command=command, bg=bg_color, fg=fg_color, width=20, height=8, borderwidth=0, highlightthickness=0)
    button.pack(side=tk.LEFT, padx=10, pady=10)
    return button

# Function to open a new page
def open_page(page_func):
    # Destroy the current frame if it exists
    if hasattr(root, 'frame'):
        root.frame.destroy()
    # Create a new frame for the page
    root.frame = tk.Frame(root)
    root.frame.pack(pady=20)
    # Open the new page
    page_func(root.frame)

def open_mcq_practice(frame):
    MCQPracticePage(frame)

def open_coding_practice(frame):
    CodingPracticePage(frame)

def open_books():
    # Placeholder: Open books page
    pass

def open_apply_for_internship():
    # Placeholder: Open apply for internship page
    pass

def open_statistics():
    # Placeholder: Open statistics page
    pass

def logout():
    # Placeholder: Logout functionality
    pass

def open_chatbot():
    # Open message box with AI speaking about education
    messagebox.showinfo("Chatbot", "Hello! I'm an AI Chatbot. Let's talk about education.")
    # Allow chatting with the chatbot
    while True:
        user_input = simpledialog.askstring("Chat with Chatbot", "You: ")
        if user_input:
            # Placeholder: Process user input and generate response from the chatbot
            chatbot_response = "Chatbot: Your message is received. Thank you for chatting!"
            messagebox.showinfo("Chatbot", chatbot_response)
        else:
            break

# Create main window
root = tk.Tk()
root.title("Blank Page")

# Get screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set fixed size for the window
window_width = 800
window_height = 600
window_x = (screen_width - window_width) // 2
window_y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Header
header_label = tk.Label(root, text="Welcome to Your Page", font=("Arial", 18, "bold"))
header_label.pack(pady=20)

# Create button rows
row1 = tk.Frame(root)
row1.pack(pady=5)
row2 = tk.Frame(root)
row2.pack(pady=5)
row3 = tk.Frame(root)
row3.pack(pady=5)

# Profile button
profile_button = create_round_button(row1, "Profile", lambda: open_page(lambda frame: open_profile(frame, 'test_user')), "lightblue", "black")
mcq_practice_button = create_round_button(row1, "MCQ Practice", lambda: open_page(open_mcq_practice), "lightcoral", "black")
coding_practice_button = create_round_button(row1, "Coding Practice", lambda: open_page(open_coding_practice), "lightyellow", "black")

write_exam_button = create_round_button(row3, "Write Exam", open_write_exam_window, "lightcyan", "black")

# Books button
books_button = create_round_button(row2, "Books", open_books, "lightpink", "black")
apply_for_internship_button = create_round_button(row2, "Apply for Internship", open_apply_for_internship, "yellow", "black")
conduct_exam_button = create_round_button(row2, "Conduct Exam", open_conduct_exam_window, "lightgreen", "black")

# Statistics button
statistics_button = create_round_button(row3, "Statistics", open_statistics, "lightcyan", "black")
logout_button = create_round_button(row3, "Logout", logout, "lightgrey", "black")

# Footer
footer_label = tk.Label(root, text="© 2024 Your Company. All rights reserved.", font=("Arial", 10))
footer_label.pack(side=tk.BOTTOM, pady=5)

# Chatbot button
chatbot_button = tk.Button(root, text="Chatbot", command=open_chatbot, bg="lightblue", fg="black", width=10, height=2, borderwidth=0, highlightthickness=0)
chatbot_button.pack(side=tk.BOTTOM, pady=5)

# Back button
back_button = tk.Button(root, text="Back", command=open_blank_page_creator, bg="lightgrey", fg="black", width=10, height=2, borderwidth=0, highlightthickness=0)
back_button.pack(side=tk.BOTTOM, pady=5)

# Run the main event loop
root.mainloop()
