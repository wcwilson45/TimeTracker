from tkinter import *
from tkinter.ttk import *
import tkinter as tk


class EditTaskWindow(tk.Tk):  # Inherit from tk.Tk to make it a standalone app
    def __init__(self):
        super().__init__()

        self.geometry("540x720")
        self.title("Edit Task")

        # Task Name
        Label(self, text="Task Name:").grid(row=0, column=0, sticky="w", padx=20, pady=10)
        Entry(self, width=40).grid(row=0, column=1, pady=10)

        # Task Description
        Label(self, text="Edit Description:").grid(row=1, column=0, sticky="nw", padx=20, pady=10)
        Text(self, height=5, width=40).grid(row=1, column=1, pady=10)

        # Tags
        Label(self, text="Edit Tags:").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        Entry(self, width=40).grid(row=2, column=1, pady=10)

        # Time of Completion
        Label(self, text="Edit Time of Completion (0:00am/pm month-day-year):").grid(row=3, column=0, sticky="w", padx=20, pady=10)
        Entry(self, width=40).grid(row=3, column=1, pady=10)

        # Time Complexity
        Label(self, text="Edit Time Complexity:").grid(row=4, column=0, sticky="w", padx=20, pady=10)
        Combobox(self, values=["Low", "Medium", "High"], width=17).grid(row=4, column=1, pady=10, sticky="w")

        # Date Completed
        Label(self, text="Edit Date Completed:").grid(row=5, column=0, sticky="w", padx=20, pady=10)
        Entry(self, width=20).grid(row=5, column=1, pady=10, sticky="w")

        # Buttons at Bottom-Right
        confirm_button = Button(self, text="Confirm", width=15)
        confirm_button.grid(row=6, column=1, pady=20, sticky="e")

        exit_button = Button(self, text="Exit", width=15, command=self.destroy)
        exit_button.grid(row=6, column=1, pady=20, sticky="w")


if __name__ == "__main__":
    app = EditTaskWindow()
    app.mainloop()

