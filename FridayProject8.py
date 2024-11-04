import tkinter as tk
from tkinter import messagebox
import sqlite3
import tkinter.simpledialog as simpledialog

# Initialize the database and create the feedback table if it doesn't exist
connection = sqlite3.connect("feedback.db")
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    feedback TEXT NOT NULL
)
''')
connection.commit()
connection.close()

class FeedbackApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Feedback Page")
        self.root.geometry("500x500")

        # Create label and entry for name
        self.name_label = tk.Label(root, text="Name:", font=("System", 16), foreground="grey1")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(root, width=30, font=("System", 16))
        self.name_entry.pack(pady=5)

        # Create label and entry for email
        self.email_label = tk.Label(root, text="Email:", font=("System", 16))
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(root, width=30, font=("System", 16))
        self.email_entry.pack(pady=5)

        # Create label and entry for feedback
        self.feedback_label = tk.Label(root, text="Please enter your feedback:", font=("System", 16))
        self.feedback_label.pack(pady=10)
        self.feedback_entry = tk.Text(root, height=10, width=50, font=("System", 16))
        self.feedback_entry.pack(pady=10)

        # Create submit and retrieve buttons
        self.submit_button = tk.Button(root, text="Submit Feedback", command=self.submit_feedback)
        self.submit_button.pack(pady=10)
        self.retrieve_button = tk.Button(root, text="Retrieve Feedback", command=self.retrieve_feedback)
        self.retrieve_button.pack(pady=10)

    def submit_feedback(self):
        # Get data from entries
        name = self.name_entry.get().strip()
        email = self.email_entry.get().strip()
        feedback = self.feedback_entry.get("1.0", tk.END).strip()

        # Insert into database if fields are filled
        if name and email and feedback:
            with sqlite3.connect("feedback.db") as connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO feedback (name, email, feedback) VALUES (?, ?, ?)", 
                               (name, email, feedback))
                connection.commit()
            messagebox.showinfo("Success", "Thank you for your feedback!")
            # Clear input fields
            self.name_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.feedback_entry.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "All fields must be filled out.")

    def retrieve_feedback(self):
    # Ask for password in a dialog box
        password = simpledialog.askstring("Password", "Enter password to retrieve data:", show='*')
    
    # Check if the password is correct
        if password == "password":
            with sqlite3.connect("feedback.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT name, email, feedback FROM feedback")
                rows = cursor.fetchall()
            
                print("\nAll Feedback Entries:")
                for row in rows:
                    print(f"Name: {row[0]}, Email: {row[1]}, Feedback: {row[2]}")
        else:
            messagebox.showerror("Access Denied", "Incorrect password.")

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FeedbackApp(root)
    root.mainloop()
