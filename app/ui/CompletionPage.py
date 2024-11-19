from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from tkinter import ttk
import tkinter as tk


class CompletedTasksWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("540x320")
        self.title("Completed Tasks")

        self.header_label = tk.Label(
            self,
            text="Make Daniel Happy",  # Your text here
            font=("Arial", 20, "bold"),  # Font family, size, and weight
            anchor="w",  # 'w' means west (left) alignment
        )
        self.header_label.pack(side="top", fill="x", padx=2, pady=2)  # Add padding around text

        # Description Box
        self.description_frame = ttk.Frame(self)
        self.description_frame.pack(anchor="w", padx=2)

        # Description Label
        self.description_label = ttk.Label(
            self.description_frame,
            text="Description:",
            font=("Arial", 10)
        )
        self.description_label.pack(anchor="w")

        # Text Area for Description
        self.description_text = tk.Text(
            self.description_frame,
            height=4,  # Number of lines visible
            width=30,  # Width in characters
            wrap="word"  # Wrap by word instead of character
        )
        self.description_text.pack(pady=5)
        self.description_text.insert("1.0", "make good app and people happy")

        ttk.Button(self, text='Close', command=self.destroy).pack(expand=True)


#def open_completedtaskswindow(parent):
 # window = CompletedTasksWindow(parent)
  #  window.grab.set()


if __name__ == "__main__":
    app = CompletedTasksWindow()
    app.mainloop()
