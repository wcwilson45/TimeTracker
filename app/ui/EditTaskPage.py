from tkinter import ttk
import tkinter as tk


class EditTaskWindow(tk.Tk):  # Inherit from tk.Tk to make it a standalone app
    def __init__(self):
        super().__init__()

        self.geometry("620x400")
        self.title("Edit Task")
        self.configure(bg='#444444')


        self.style = ttk.Style()
        self.style.theme_use('alt')
        self.style.configure("Custom.TCombobox", fieldbackground="light blue", background="light blue", arrowcolor='black'
                             , foreground='black',  font=("SF Pro", 12))
        self.style.configure("Custom.TLabel", background='#444444', foreground='#FFFFFF', font=("SF Pro", 12))

        # Task Name
        ttk.Label(self, text="Task Name:", style="Custom.TLabel").grid(row=0, column=0, sticky="w", padx=20, pady=10)
        tk.Entry(self, width=40, bg='light blue', font=("SF Pro ", 12)).grid(row=0, column=1, padx=2, pady=2, sticky='W')

        # Task Description
        ttk.Label(self, text="Edit Description:", style="Custom.TLabel").grid(row=1, column=0, sticky="nw", padx=20, pady=10)
        tk.Text(self, height=5, width=40, bg='light blue', font=("SF Pro", 12)).grid(row=1, column=1, pady=10, sticky="W")

        # Tags
        ttk.Label(self, text="Edit Tags:", style="Custom.TLabel").grid(row=2, column=0, sticky="w", padx=20, pady=10)
        tk.Entry(self, width=40, bg='light blue', font=("SF Pro", 12)).grid(row=2, column=1, pady=10, sticky="W")

        # Time of Completion
        ttk.Label(self, text="Edit Time of Completion:", style="Custom.TLabel").grid(row=3, column=0, sticky="w", padx=20, pady=10)
        tk.Entry(self, width=40, bg='light blue', font=("SF Pro", 12)).grid(row=3, column=1, pady=10, sticky="W")

        # Time Complexity
        ttk.Label(self, text="Edit Time Complexity:", style="Custom.TLabel").grid(row=4, column=0, sticky="w", padx=20, pady=10)
        ttk.Combobox(self, values=["Low", "Medium", "High"], width=17, style='Custom.TCombobox').grid(row=4, column=1, pady=10, sticky="w")

        # Date Completed
        ttk.Label(self, text="Edit Date Completed:", style="Custom.TLabel").grid(row=5, column=0, sticky="w", padx=20, pady=10)
        tk.Entry(self, width=20, bg='light blue', font=("SF Pro", 12)).grid(row=5, column=1, pady=10, sticky="w")

        # Buttons at Bottom-Right
        confirm_button = tk.Button(self, text="Confirm", width=15, bg='#90EE90', fg='black')
        confirm_button.grid(row=6, column=1, pady=20, sticky="w")

        exit_button = tk.Button(self, text="Exit", width=15, bg='#F08080', fg='black', command=self.destroy)
        exit_button.grid(row=6, column=1, pady=20, sticky="e")

if __name__ == "__main__":
    app = EditTaskWindow()
    app.mainloop()