from tkinter import ttk
import tkinter as tk


class EditTaskWindow(tk.Tk):  # Inherit from tk.Tk to make it a standalone app
    def __init__(self):
        super().__init__()

        self.geometry("720x400")
        self.title("Edit Task")
        self.configure(bg='#666666')

        style = ttk.Style()
        style.theme_use('alt')
        style.configure("TCombobox", fieldbackground="light blue", background="light blue", arrowcolor='black', foreground='black')

        # Task Name
        ttk.Label(self, text="Task Name:", background='#666666', foreground='#FFFFFF').grid(row=0, column=0, sticky="w", padx=20, pady=10)
        tk.Entry(self, width=40, bg='light blue').grid(row=0, column=1, padx=2, pady=2)

        # Task Description
        ttk.Label(self, text="Edit Description:", background='#666666', foreground='#FFFFFF').grid(row=1, column=0, sticky="nw", padx=20, pady=10)
        tk.Text(self, height=5, width=40, bg='light blue').grid(row=1, column=1, pady=10)

        # Tags
        ttk.Label(self, text="Edit Tags:", background='#666666', foreground='#FFFFFF').grid(row=2, column=0, sticky="w", padx=20, pady=10)
        tk.Entry(self, width=40, bg='light blue').grid(row=2, column=1, pady=10)

        # Time of Completion
        ttk.Label(self, text="Edit Time of Completion (0:00am/pm month-day-year):", background='#666666', foreground='#FFFFFF').grid(row=3, column=0, sticky="w", padx=20, pady=10)
        tk.Entry(self, width=40, bg='light blue').grid(row=3, column=1, pady=10)

        # Time Complexity
        ttk.Label(self, text="Edit Time Complexity:", background='#666666', foreground='#FFFFFF').grid(row=4, column=0, sticky="w", padx=20, pady=10)
        ttk.Combobox(self, values=["Low", "Medium", "High"], width=17, style='TCombobox').grid(row=4, column=1, pady=10, sticky="w")

        # Date Completed
        ttk.Label(self, text="Edit Date Completed:", background='#666666', foreground='#FFFFFF').grid(row=5, column=0, sticky="w", padx=20, pady=10)
        tk.Entry(self, width=20, bg='light blue').grid(row=5, column=1, pady=10, sticky="w")

        # Buttons at Bottom-Right
        confirm_button = tk.Button(self, text="Confirm", width=15, bg='#90EE90', fg='black')
        confirm_button.grid(row=6, column=1, pady=20, sticky="w")

        exit_button = tk.Button(self, text="Exit", width=15, bg='#F08080', fg='black', command=self.destroy)
        exit_button.grid(row=6, column=1, pady=20, sticky="e")

if __name__ == "__main__":
    app = EditTaskWindow()
    app.mainloop()
