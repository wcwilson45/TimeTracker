# inter_roboto_window.py
from tkinter import *
from tkinter.ttk import *
import tkinter as tk
import tkinter.font as tkfont

class InterRobotoWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("600x350")
        self.title("Task Manager")
        self.configure(bg='#f0f0f0')

        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="Inter", size=32, weight="bold"),
            'subheader': tkfont.Font(family="Inter", size=11, weight="bold"),
            'body': tkfont.Font(family="Roboto", size=10)
        }
        
        # Style configurations
        style = Style()
        style.configure('MainFrame.TFrame', background='#f0f0f0')
        style.configure('Input.TFrame', background='#f0f0f0')
        style.configure('Input.TEntry', fieldbackground='white', font=("Roboto", 10))
        style.configure('Input.TCombobox', fieldbackground='white', font=("Roboto", 10))
        style.configure('TLabel', background='#f0f0f0', font=("Roboto", 10))
        
        # Main container
        main_frame = Frame(self, style='MainFrame.TFrame')
        main_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Header frame
        header_frame = Frame(main_frame, style='MainFrame.TFrame')
        header_frame.pack(fill='x', pady=(0,10))
        
        # Task Name Label
        Label(header_frame, text="Task Name", font=self.fonts['header'],
              style='TLabel').pack(side='left')

        # Content container
        content_frame = Frame(main_frame, style='MainFrame.TFrame')
        content_frame.pack(fill='both', expand=True)
        
        # Left column
        left_frame = Frame(content_frame, style='MainFrame.TFrame')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0,10))
        
        # Description
        Label(left_frame, text="Edit Description:", 
              font=self.fonts['subheader'], style='TLabel').pack(anchor='w')
        desc_text = tk.Text(left_frame, height=8, width=30, bg='white', 
                           relief="solid", bd=1, font=self.fonts['body'])
        desc_text.pack(fill='x', pady=(5,10))
        
        # Tags
        Label(left_frame, text="Edit Tags:", 
              font=self.fonts['subheader'], style='TLabel').pack(anchor='w')
        Entry(left_frame, style='Input.TEntry').pack(fill='x', pady=(5,10))
        
        # Right column
        right_frame = Frame(content_frame, style='MainFrame.TFrame')
        right_frame.pack(side='left', fill='both', expand=True)
        
        # Time of Completion
        Label(right_frame, text="Edit Time of Completion:", 
              font=self.fonts['subheader'], style='TLabel').pack(anchor='w')
        Entry(right_frame, style='Input.TEntry').pack(fill='x', pady=(5,10))
        
        # Time Complexity
        Label(right_frame, text="Edit Time Complexity:", 
              font=self.fonts['subheader'], style='TLabel').pack(anchor='w')
        combo = Combobox(right_frame, values=["Low", "Medium", "High"], 
                        style='Input.TCombobox')
        combo.pack(fill='x', pady=(5,10))
        
        # Date Completed
        Label(right_frame, text="Edit Date Completed:", 
              font=self.fonts['subheader'], style='TLabel').pack(anchor='w')
        Entry(right_frame, style='Input.TEntry').pack(fill='x', pady=(5,10))

        # Bottom buttons frame
        buttons_frame = Frame(main_frame, style='MainFrame.TFrame')
        buttons_frame.pack(fill='x', pady=(10,0))
        
        # Container for right-aligned buttons
        right_buttons = Frame(buttons_frame, style='MainFrame.TFrame')
        right_buttons.pack(side='right')
        
        # Cancel button
        Label(right_buttons, text="Cancel:", 
              font=self.fonts['body'], style='TLabel').pack(side='left', padx=(0,5))
        cancel_btn = tk.Label(right_buttons, text="✕", bg="#ff4444", fg="white", width=2,
                            font=self.fonts['body'])
        cancel_btn.pack(side='left', padx=(0,20))
        
        # Confirm button
        Label(right_buttons, text="Confirm:", 
              font=self.fonts['body'], style='TLabel').pack(side='left', padx=(0,5))
        confirm_btn = tk.Label(right_buttons, text="✓", bg="#44ff44", fg="white", width=2,
                             font=self.fonts['body'])
        confirm_btn.pack(side='left')

if __name__ == "__main__":
    app = InterRobotoWindow()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()