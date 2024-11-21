from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk

class CommitHistoryWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Commit History")
        self.geometry("500x600")
        self.configure(bg="white")

        # Title Label
        self.title_label = ttk.Label(self, text="Commit History Page", font=("Arial", 14, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")

        # Header Section
        self.changelog_label = ttk.Label(self, text="Changelog", font=("Arial", 12))
        self.changelog_label.grid(row=1, column=0, padx=10, sticky="w")

        self.date_time_label = ttk.Label(self, text="12/1/24    3:48:52", font=("Arial", 12))
        self.date_time_label.grid(row=1, column=1, columnspan=2, sticky="e", padx=10)

        # Back Button
        self.back_button = tk.Button(self, text="Back",command = self.destroy, bg="red", fg="white", font=("Arial", 10, "bold"))
        self.back_button.place(relx=0.9, rely=0.05, anchor="ne")  # Moves the button to the top-right

        # Main Layout
        self.labels = ["Task Name:", "Description:", "Tags:", "Completion Time:", "Time Complexity:", "Date Completed:"]
        for i, label in enumerate(self.labels):
            ttk.Label(self, text=label, font=("Arial", 10)).grid(row=2 + i * 2, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(self, text="→", font=("Arial", 10)).grid(row=2 + i * 2, column=1)
            ttk.Entry(self).grid(row=2 + i * 2, column=2, padx=10, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = CommitHistoryWindow()
    root.mainloop()



