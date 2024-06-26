import tkinter as tk
from tkinter import simpledialog, messagebox, Radiobutton
import random
import sqlite3
import cv2

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

# Function to check if the entered code exists in the database
def check_code_in_database(code):
    conn = sqlite3.connect('exam_codes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM exam_codes WHERE code=?", (code,))
    result = c.fetchone()
    conn.close()
    return result is not None

# Function to ask random multiple-choice questions during the exam
def ask_random_questions():
    questions = [
        {
            "question": "What is the capital of France?",
            "options": ["Paris", "London", "Berlin", "Rome"],
            "answer": "Paris"
        },
        {
            "question": "Who wrote 'To Kill a Mockingbird'?",
            "options": ["Harper Lee", "J.K. Rowling", "Charles Dickens", "Jane Austen"],
            "answer": "Harper Lee"
        },
        {
            "question": "What is the chemical symbol for gold?",
            "options": ["Au", "Ag", "Hg", "Pt"],
            "answer": "Au"
        },
        # Add more questions as needed
    ]
    # Ask a random question
    question_data = random.choice(questions)
    question = question_data["question"]
    options = question_data["options"]

    # Create a new window for the question
    question_window = tk.Toplevel()
    question_window.title("Question")
    question_window.geometry("400x200")

    # Display the question
    question_label = tk.Label(question_window, text=question)
    question_label.pack()

    # Create radio buttons for options
    var = tk.StringVar()
    for option in options:
        option_button = Radiobutton(question_window, text=option, variable=var, value=option)
        option_button.pack()

    # Function to check the selected option
    def check_answer():
        selected_option = var.get()
        correct_answer = question_data["answer"]
        if selected_option == correct_answer:
            messagebox.showinfo("Result", "Correct!")
        else:
            messagebox.showinfo("Result", f"Incorrect! The correct answer is {correct_answer}")

    # Button to check the answer
    check_button = tk.Button(question_window, text="Check", command=check_answer)
    check_button.pack()

# Function to detect faces using Haar Cascade Classifier
def detect_faces(frame):
    # Load the Haar Cascade Classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Draw rectangles around the detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return frame

# Function to open the write exam window
def open_write_exam_window():
    # Ask the user to enter the exam code
    user_code = simpledialog.askstring("Exam Code", "Please enter the exam code:")

    # Check if the entered code exists in the database
    if check_code_in_database(user_code):
        # Initialize video capture
        cap = cv2.VideoCapture(0)

        # Main loop for the exam window
        attempts = 0
        while True:
            ret, frame = cap.read()

            # Perform face detection to check for cheating behavior
            frame = detect_faces(frame)

            # Display the frame with detected faces
            cv2.imshow('Exam Monitoring', frame)

            # Ask random multiple-choice questions during the exam
            ask_random_questions()

            # Check for cheating behavior and alert if detected

            # Break the loop if the user closes the window or attempts exceed 3
            if cv2.waitKey(1) & 0xFF == ord('q') or attempts >= 3:
                break
            attempts += 1

        # Release video capture and close windows
        cap.release()
        cv2.destroyAllWindows()
    else:
        messagebox.showerror("Error", "Invalid exam code. Please enter a valid code.")

# Create a random code and store it in the database
random_code = generate_random_code()
store_code_in_database(random_code)

# Create main window
root = tk.Tk()
root.title("Main Window")

# Set the size of the main window to 600x400
root.geometry("600x400")

# Button to open write exam window
write_exam_button = tk.Button(root, text="Write Exam", command=open_write_exam_window)
write_exam_button.pack(pady=20)

root.mainloop()
