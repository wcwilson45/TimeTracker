from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk

def create_commit_history_page():
    root = tk.Tk()
    root.title("Commit History Page")
    root.geometry("500x600")
    root.configure(bg="white")

    # Title Label
    title_label = ttk.Label(root, text="Commit History Page", font=("Arial", 14, "bold"))
    title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")

    # Header Section
    changelog_label = ttk.Label(root, text="Changelog", font=("Arial", 12))
    changelog_label.grid(row=1, column=0, padx=10, sticky="w")

    date_time_label = ttk.Label(root, text="12/1/24    3:48:52", font=("Arial", 12))
    date_time_label.grid(row=1, column=1, columnspan=2, sticky="e", padx=10)

    # Back Button
    back_button = tk.Button(root, text="Back", bg="red", fg="white", font=("Arial", 10, "bold"))
    back_button.place(relx=0.9, rely=0.05, anchor="ne")  # Moves the button to the top-right

    # Main Layout
    labels = ["Task Name:", "Description:", "Tags:", "Completion Time:", "Time Complexity:", "Date Completed:"]
    for i, label in enumerate(labels):
        ttk.Label(root, text=label, font=("Arial", 10)).grid(row=2 + i * 2, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(root, text="→", font=("Arial", 10)).grid(row=2 + i * 2, column=1)
        ttk.Entry(root).grid(row=2 + i * 2, column=2, padx=10, pady=5)

    root.mainloop()

create_commit_history_page()
