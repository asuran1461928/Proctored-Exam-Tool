import tkinter as tk
from tkinter import messagebox

# Sample questions for different topics
questions = {
    "Operating Systems": [
        {
            "question": "What is the main purpose of an operating system?",
            "options": [
                "A. Manage computer hardware",
                "B. Run applications",
                "C. Provide user interface",
                "D. All of the above"
            ],
            "correct_answer": "D",
            "explanation": "The main purpose of an operating system is to manage computer hardware, run applications, and provide a user interface."
        },
        {
            "question": "What is virtual memory?",
            "options": [
                "A. Memory used by virtual machines",
                "B. Memory used for virtual reality applications",
                "C. A memory management technique",
                "D. A type of cache memory"
            ],
            "correct_answer": "C",
            "explanation": "Virtual memory is a memory management technique that provides an idealized abstraction of the storage resources that are actually available on a given machine."
        },
        {
            "question": "What is a process in the context of an operating system?",
            "options": [
                "A. A program in execution",
                "B. A folder containing files",
                "C. A device driver",
                "D. An input/output operation"
            ],
            "correct_answer": "A",
            "explanation": "In the context of an operating system, a process is a program in execution."
        }
    ],
    "Theory of Computation": [
        {
            "question": "What is a regular expression?",
            "options": [
                "A. A mathematical expression",
                "B. A sequence of characters that define a search pattern",
                "C. A type of formal language",
                "D. A representation of a finite automaton"
            ],
            "correct_answer": "B",
            "explanation": "A regular expression is a sequence of characters that define a search pattern, mainly for use in pattern matching with strings."
        },
        {
            "question": "What is the Pumping Lemma?",
            "options": [
                "A. A lemma in mathematical logic",
                "B. A theorem in computational complexity theory",
                "C. A principle in automata theory",
                "D. A property of regular languages"
            ],
            "correct_answer": "C",
            "explanation": "The Pumping Lemma is a principle in automata theory used to prove that certain languages are not regular."
        },
        {
            "question": "What is the Turing machine?",
            "options": [
                "A. A type of computer architecture",
                "B. A mathematical model of computation",
                "C. A programming language",
                "D. An operating system"
            ],
            "correct_answer": "B",
            "explanation": "The Turing machine is a mathematical model of computation that defines an abstract machine."
        }
    ],
    "Computer Networks": [
        {
            "question": "What is TCP/IP?",
            "options": [
                "A. A network protocol suite",
                "B. A type of computer hardware",
                "C. A programming language",
                "D. A data compression algorithm"
            ],
            "correct_answer": "A",
            "explanation": "TCP/IP (Transmission Control Protocol/Internet Protocol) is a network protocol suite that defines the protocols used in the Internet."
        },
        {
            "question": "What is a subnet mask?",
            "options": [
                "A. A hardware device used for routing",
                "B. A type of computer virus",
                "C. A security feature in operating systems",
                "D. A numerical identifier used to specify a subnet"
            ],
            "correct_answer": "D",
            "explanation": "A subnet mask is a numerical identifier used to specify a subnet, which is a logical subdivision of an IP network."
        },
        {
            "question": "What is OSI model and how many layers does it have?",
            "options": [
                "A. A programming language with 7 layers",
                "B. A network protocol with 5 layers",
                "C. A model that defines a networking framework with 7 layers",
                "D. An encryption algorithm with 10 layers"
            ],
            "correct_answer": "C",
            "explanation": "The OSI (Open Systems Interconnection) model is a conceptual model that defines a networking framework with 7 layers."
        }
    ],
    "Data Structures and Algorithms": [
        {
            "question": "What is a linked list?",
            "options": [
                "A. A data structure that stores elements in contiguous memory locations",
                "B. A data structure that consists of a sequence of nodes, each containing arbitrary data fields and one or more references (or links) to the next node",
                "C. A sorting algorithm",
                "D. A type of binary tree"
            ],
            "correct_answer": "B",
            "explanation": "A linked list is a data structure that consists of a sequence of nodes, each containing arbitrary data fields and one or more references (or links) to the next node."
        },
        {
            "question": "What is a stack?",
            "options": [
                "A. A linear data structure that follows the Last In, First Out (LIFO) principle",
                "B. A sorting algorithm",
                "C. A type of binary tree",
                "D. An algorithm for traversing graphs"
            ],
            "correct_answer": "A",
            "explanation": "A stack is a linear data structure that follows the Last In, First Out (LIFO) principle, where elements are added and removed from the same end."
        },
        {
            "question": "What is a binary search?",
            "options": [
                "A. A search algorithm that finds the position of a target value within a sorted array",
                "B. A data structure for storing key-value pairs",
                "C. A type of graph traversal algorithm",
                "D. A technique for optimizing database queries"
            ],
            "correct_answer": "A",
            "explanation": "Binary search is a search algorithm that finds the position of a target value within a sorted array by repeatedly dividing the search interval in half."
        }
    ]
}

class MCQPracticePage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("MCQ Practice")
        self.geometry("800x600")  # Set window size

        # Create a frame to hold topic buttons
        self.topic_frame = tk.Frame(self)
        self.topic_frame.pack(pady=20)

        # Create buttons for each topic
        for topic in questions.keys():
            topic_button = tk.Button(self.topic_frame, text=topic, command=lambda t=topic: self.open_topic(t))
            topic_button.pack(side=tk.LEFT, padx=10)

        # Label to display selected topic
        self.selected_topic_label = tk.Label(self, text="", font=("Arial", 14))
        self.selected_topic_label.pack(pady=10)

        # Label to display questions
        self.question_label = tk.Label(self, text="", font=("Arial", 12), wraplength=700)  # Adjust wraplength
        self.question_label.pack(pady=10)

        # Create radio buttons for options
        self.option_var = tk.StringVar()
        self.option_buttons = []
        for i in range(4):
            option_button = tk.Radiobutton(self, text="", variable=self.option_var, value=str(i), command=self.update_option_color)
            option_button.pack(anchor=tk.W)
            self.option_buttons.append(option_button)

        # Create a frame to display explanation
        self.explanation_frame = tk.Frame(self)
        self.explanation_frame.pack(pady=10)

        # Label to display explanation
        self.explanation_label = tk.Label(self.explanation_frame, text="", font=("Arial", 12), wraplength=700)  # Adjust wraplength
        self.explanation_label.pack(pady=10)

        # Create a frame to display key
        self.key_frame = tk.Frame(self)
        self.key_frame.pack(pady=10)

        # Label to display key
        self.key_label = tk.Label(self.key_frame, text="", font=("Arial", 12), wraplength=700)  # Adjust wraplength
        self.key_label.pack(pady=10)

        # Create a frame to hold navigation buttons
        self.nav_frame = tk.Frame(self)
        self.nav_frame.pack(pady=20)

        # Submit button
        self.submit_button = tk.Button(self.nav_frame, text="Submit", command=self.check_answer)
        self.submit_button.pack(side=tk.LEFT, padx=10)

        # Previous and next buttons
        self.prev_button = tk.Button(self.nav_frame, text="Previous", command=self.prev_question)
        self.prev_button.pack(side=tk.LEFT, padx=10)
        self.next_button = tk.Button(self.nav_frame, text="Next", command=self.next_question)
        self.next_button.pack(side=tk.LEFT, padx=10)

        # Score label
        self.score_label = tk.Label(self.nav_frame, text="Score: 0", font=("Arial", 12))
        self.score_label.pack(side=tk.RIGHT, padx=10)

        # Reset button
        self.reset_button = tk.Button(self.nav_frame, text="Reset", command=self.reset_quiz)
        self.reset_button.pack(side=tk.RIGHT, padx=10)

        # Initialize topic index and question index
        self.current_topic_index = 0
        self.current_question_index = 0
        self.score = 0

        # Show the first topic
        self.show_topic(list(questions.keys())[0])

    def show_topic(self, topic):
        # Update selected topic label
        self.selected_topic_label.config(text=f"Topic: {topic}")

        # Update question label with the first question of the selected topic
        self.current_topic_index = list(questions.keys()).index(topic)
        self.current_question_index = 0
        self.show_question()

    def show_question(self):
        # Update question label with the current question
        topic = list(questions.keys())[self.current_topic_index]
        question_data = questions[topic][self.current_question_index]
        question_text = question_data["question"]
        self.question_label.config(text=question_text)

        # Update option buttons
        for i, option_text in enumerate(question_data["options"]):
            self.option_buttons[i].config(text=option_text, fg="black")

        # Clear previous explanation
        self.explanation_label.config(text="")

        # Hide key initially
        self.key_label.config(text="")

    def update_option_color(self):
        for button in self.option_buttons:
            button.config(fg="black")

    def check_answer(self):
        # Get the selected option
        selected_option = self.option_var.get()

        # Check if an option is selected
        if selected_option:
            # Disable option buttons
            for button in self.option_buttons:
                button.config(state=tk.DISABLED)

            # Get correct answer
            correct_answer = questions[list(questions.keys())[self.current_topic_index]][self.current_question_index]["correct_answer"]

            # Convert correct answer to index
            correct_index = ord(correct_answer) - ord('A')

            # Check if the selected option is correct
            if selected_option == correct_answer:
                self.option_buttons[correct_index].configure(fg="green")
                self.show_explanation(correct_answer)
                self.score += 1
                self.score_label.config(text=f"Score: {self.score}")  # Update score label
                messagebox.showinfo("Correct", "Your answer is correct!")
            else:
                # Mark the selected option as red
                self.option_buttons[int(selected_option)].configure(fg="red")
                # Mark the correct option as green
                self.option_buttons[correct_index].configure(fg="green")
                self.show_explanation(correct_answer)
                messagebox.showinfo("Incorrect", "Your answer is incorrect.")

            # Show the key
            self.key_label.config(text=f"Key: {correct_answer}")

            # Reset option selection
            self.option_var.set(None)


    def show_explanation(self, correct_answer):
        # Display explanation for the correct answer
        topic = list(questions.keys())[self.current_topic_index]
        explanation_text = questions[topic][self.current_question_index]["explanation"]
        self.explanation_label.config(text=f"Explanation: {explanation_text}")

    def prev_question(self):
        # Show the previous question
        self.current_question_index = (self.current_question_index - 1) % len(questions[list(questions.keys())[self.current_topic_index]])
        self.show_question()

    def next_question(self):
        # Show the next question
        self.current_question_index = (self.current_question_index + 1) % len(questions[list(questions.keys())[self.current_topic_index]])
        self.show_question()

    def open_topic(self, topic):
        # Show questions for the selected topic
        self.show_topic(topic)

    def reset_quiz(self):
        # Reset the quiz
        self.score = 0
        self.score_label.config(text="Score: 0")
        for button in self.option_buttons:
            button.config(state=tk.NORMAL)
        self.show_question()

if __name__ == "__main__":
    root = tk.Tk()
    mcq_page = MCQPracticePage(root)
    root.mainloop()
