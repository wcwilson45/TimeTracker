from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk


class CommitHistoryWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Commit History")
        self.geometry("600x300")
        self.configure(bg="#5DADE2")

        # Create a style for labels with light gray background
        style = ttk.Style(self)
        style.configure("Custom.TLabel",background="#5DADE2", font=("SF Pro Text", 12))  # Light gray color

        # Title Label
        self.title_label = ttk.Label(self, text="Commit History Page", background="#5DADE2", font=("SF Pro Text", 24, ))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")

        # Header Section
        self.changelog_label = ttk.Label(self, text="Changelog",background="#5DADE2", font=("SF Pro Text", 12))
        self.changelog_label.grid(row=1, column=0, padx=10, sticky="w")

        # Date and Time Label
        self.date_time_label = ttk.Label(self, text="December 1, 2024    3:48:52", background="#5DADE2", font=("SF Pro Text", 12))
        self.date_time_label.grid(row=1, column=1, columnspan=2, sticky="e", padx=10)

        # Back Button
        self.back_button = tk.Button(self, text="Cancel", command=self.destroy, bg="#F08080", fg="#000000",
                                     font=("SF Pro Text", 12, "bold"), relief = "flat")
        self.back_button.place(relx=0.9, rely=0.05, anchor="ne")  # Moves the button to the top-right

        # Main Layout
        self.labels = [
            "Task Name: Save lives","Description: Save all lives","Tags:Important", "Completion Time: 10 years", "Time Complexity: :)", "Date Completed: December 1 2035"
        ]
        example_data = [
            "Save Some lives","All lives might not be saved","Somewhat important","Probably not possible", ":(", "December 2, 2035"
        ]

        for i, (label, data) in enumerate(zip(self.labels, example_data)):
            ttk.Label(self, text=label, style="Custom.TLabel").grid(row=2 + i * 2, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(self, text="→", style="Custom.TLabel").grid(row=2 + i * 2, column=1)
            ttk.Label(self, text=data, style="Custom.TLabel").grid(row=2 + i * 2, column=2, padx=10, pady=5, sticky="w")


if __name__ == "__main__":
    app = CommitHistoryWindow()
    app.mainloop()
