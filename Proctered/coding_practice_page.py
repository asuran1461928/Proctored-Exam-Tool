import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import random
import os

# Sample coding questions categorized by difficulty and DSA subtopics
coding_questions = {
    "easy": {
        "factorial": {
            "question": "Write a Python program to find the factorial of a number.",
            "answer": """
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

num = 5
print("Factorial of", num, "is", factorial(num))
"""
        },
        "prime": {
            "question": "Write a Python program to check if a number is prime.",
            "answer": """
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

num = 11
if is_prime(num):
    print(num, "is prime")
else:
    print(num, "is not prime")
"""
        }
    },
    "moderate": {
        "reverse_string": {
            "question": "Write a Python program to reverse a string.",
            "answer": """
def reverse_string(s):
    return s[::-1]

string = "hello"
print("Reversed string:", reverse_string(string))
"""
        },
        "sum_of_digits": {
            "question": "Write a Python program to find the sum of digits in a number.",
            "answer": """
def sum_of_digits(n):
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total

num = 12345
print("Sum of digits:", sum_of_digits(num))
"""
        }
    },
    "hard": {
        "binary_search": {
            "question": "Write a Python program to implement binary search in a sorted list.",
            "answer": """
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
target = 6
print("Index of target element:", binary_search(arr, target))
"""
        },
        "merge_sort": {
            "question": "Write a Python program to implement merge sort algorithm.",
            "answer": """
def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]
        merge_sort(left_half)
        merge_sort(right_half)
        
        i = j = k = 0
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1
        
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1
        
        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

arr = [12, 11, 13, 5, 6, 7]
merge_sort(arr)
print("Sorted array:", arr)
"""
        }
    },
    "DSA": {
        "arrays": {
            "question": "Write a Python program to rotate an array to the right by k steps.",
            "answer": """
def rotate_array(nums, k):
    k = k % len(nums)
    nums[:] = nums[-k:] + nums[:-k]

arr = [1, 2, 3, 4, 5, 6, 7]
rotate_array(arr, 3)
print("Rotated array:", arr)
"""
        },
        "trees": {
            "question": "Write a Python program to implement binary search tree.",
            "answer": """
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, val):
        if not self.root:
            self.root = TreeNode(val)
        else:
            self._insert(self.root, val)

    def _insert(self, node, val):
        if val < node.val:
            if not node.left:
                node.left = TreeNode(val)
            else:
                self._insert(node.left, val)
        else:
            if not node.right:
                node.right = TreeNode(val)
            else:
                self._insert(node.right, val)

bst = BST()
bst.insert(5)
bst.insert(3)
bst.insert(7)
"""
        },
        "linked_lists": {
            "question": "Write a Python program to reverse a linked list.",
            "answer": """
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_linked_list(head):
    prev = None
    while head:
        next_node = head.next
        head.next = prev
        prev = head
        head = next_node
    return prev

# Example usage
head = ListNode(1)
head.next = ListNode(2)
head.next.next = ListNode(3)
reversed_head = reverse_linked_list(head)
"""
        }
    }
}

class CodingPracticePage(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Coding Practice")
        self.geometry("800x600")  # Set window size

        # Set background color
        self.config(bg="lightgrey")

        # Language selection
        self.language_label = tk.Label(self, text="Select Programming Language:", font=("Arial", 12))
        self.language_label.pack(pady=10)
        self.language_var = tk.StringVar()
        self.language_combobox = ttk.Combobox(self, textvariable=self.language_var, values=["Python", "Java", "C++"])
        self.language_combobox.pack()

        # Difficulty level selection
        self.difficulty_label = tk.Label(self, text="Select Difficulty Level:", font=("Arial", 12))
        self.difficulty_label.pack(pady=10)
        self.difficulty_var = tk.StringVar()
        self.difficulty_combobox = ttk.Combobox(self, textvariable=self.difficulty_var, values=["Easy", "Moderate", "Hard", "DSA"])
        self.difficulty_combobox.pack()

        # DSA subtopic selection (visible when DSA is selected as difficulty)
        self.dsa_label = tk.Label(self, text="Select DSA Subtopic:", font=("Arial", 12))
        self.dsa_label.pack(pady=10)
        self.dsa_var = tk.StringVar()
        self.dsa_combobox = ttk.Combobox(self, textvariable=self.dsa_var, values=["Arrays", "Trees", "Linked Lists"])
        self.dsa_combobox.pack()

        # Question label
        self.question_label = tk.Label(self, text="", font=("Arial", 12), wraplength=700)
        self.question_label.pack(pady=20)

        # Code entry with scrollbar
        self.code_frame = tk.Frame(self)
        self.code_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.code_text = tk.Text(self.code_frame, height=15, width=80, bg="black", fg="white")  # Set background to black
        self.code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.code_frame, command=self.code_text.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.code_text.config(yscrollcommand=self.scrollbar.set)

        # Save and Load buttons
        self.save_button = tk.Button(self, text="Save Code", command=self.save_code)
        self.save_button.pack(pady=5)
        self.load_button = tk.Button(self, text="Load Code", command=self.load_code)
        self.load_button.pack(pady=5)

        # Compile button
        self.compile_button = tk.Button(self, text="Compile & Run", command=self.compile_and_run)
        self.compile_button.pack(pady=10)

        # Output label
        self.output_label = tk.Label(self, text="", font=("Arial", 12), wraplength=700)
        self.output_label.pack(pady=10)

        # Timer
        self.timer_label = tk.Label(self, text="Time Elapsed: 00:00", font=("Arial", 12))
        self.timer_label.pack(pady=10)
        self.timer_running = False
        self.time_elapsed = 0

        # Initialize current question index
        self.current_question_index = None
        self.show_question()

    def show_question(self):
        # Get selected difficulty level and DSA subtopic (if applicable)
        selected_difficulty = self.difficulty_var.get()
        selected_dsa_subtopic = self.dsa_var.get()

        # Get questions based on selected difficulty and DSA subtopic
        if selected_difficulty == "DSA" and selected_dsa_subtopic:
            questions = coding_questions[selected_difficulty].get(selected_dsa_subtopic, {})
        elif selected_difficulty in coding_questions:
            questions = coding_questions[selected_difficulty]
        else:
            questions = {}

        # Choose a random question
        if questions:
            self.current_question_index = random.choice(list(questions.keys()))
            question = questions[self.current_question_index]["question"]
            self.question_label.config(text=question)
        else:
            self.question_label.config(text="No questions available for the selected difficulty and subtopic.")

        # Clear the code entry and output
        self.code_text.delete(1.0, tk.END)
        self.output_label.config(text="")
        self.reset_timer()

    def compile_and_run(self):
        # Start the timer if not already running
        if not self.timer_running:
            self.start_timer()

        # Get the selected language
        selected_language = self.language_var.get()

        # Get the code from the code entry
        code = self.code_text.get(1.0, tk.END)

        # Execute the code based on the selected language
        try:
            if selected_language == "Python":
                exec(code)
            elif selected_language == "Java":
                # Placeholder for Java compilation and execution
                pass
            elif selected_language == "C++":
                # Placeholder for C++ compilation and execution
                pass
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def save_code(self):
        # Save user-written code to a file
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                code = self.code_text.get(1.0, tk.END)
                file.write(code)
            messagebox.showinfo("Success", "Code saved successfully.")

    def load_code(self):
        # Load user-written code from a file
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                code = file.read()
                self.code_text.delete(1.0, tk.END)
                self.code_text.insert(tk.END, code)
            messagebox.showinfo("Success", "Code loaded successfully.")

    def start_timer(self):
        # Start the timer
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        # Update the timer label every second
        if self.timer_running:
            self.time_elapsed += 1
            minutes = self.time_elapsed // 60
            seconds = self.time_elapsed % 60
            self.timer_label.config(text=f"Time Elapsed: {minutes:02d}:{seconds:02d}")
            self.after(1000, self.update_timer)

    def reset_timer(self):
        # Reset the timer
        self.timer_running = False
        self.time_elapsed = 0
        self.timer_label.config(text="Time Elapsed: 00:00")

if __name__ == "__main__":
    root = tk.Tk()
    coding_practice_page = CodingPracticePage(root)
    root.mainloop()
