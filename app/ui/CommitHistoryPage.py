import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont

class CommitHistoryWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the main window geometry and title
        self.geometry("630x600")  # Set the window size
        self.title("Commit History")  # Set the title of the window
        self.configure(bg="#5DADE2")  # Set background color for the window

        # Create fonts for header and body texts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=16, weight="bold"),  # Header font style
            'body': tkfont.Font(family="SF Pro Text", size=12)  # Body font style
        }

        # Configure the default styles for widgets (e.g., buttons, labels, etc.)
        self.configure_styles()

        # Header section of the window
        self.create_header()
        
        # Main layout for the data
        self.create_main_layout()

    def configure_styles(self):
        """Set default styles for widgets."""
        # Set default font for buttons, labels, and entries across the app
        self.option_add("*TButton*font", "SF Pro Text 10")
        self.option_add("*TLabel*font", "SF Pro Text 12")
        self.option_add("*TEntry*font", "SF Pro Text 10")

        # Apply a modern theme
        style = ttk.Style(self)
        style.theme_use("alt")
        style.configure("Vertical.TScrollbar", troughcolor="#E0E0E0", background="#AED6F1", bordercolor="#5DADE2", arrowcolor="#5DADE2")

    def create_header(self):
        """Create the header section with date and time, and an exit button."""        
        header_frame = tk.Frame(self, bg="#5DADE2")  # Create a header frame with a specific background color
        header_frame.pack(fill="x", pady=10, padx=10)  # Pack the header frame to span horizontally

        # Date and time label
        date_label = tk.Label(
            header_frame,
            text="December 1, 2024    3:48:52",  # Example date and time
            font=self.fonts["header"],  # Use the header font style
            bg="#5DADE2"  # Background color matches the window
        )
        date_label.pack(side="top", pady=(0, 5))  # Place the label at the top of the header frame with padding

        # Exit Button
        exit_btn = tk.Button(
            self,
            text="Exit",  # Text displayed on the button
            command=self.destroy,  # Function to call when the button is clicked
            bg="#F08080",  # Button background color
            fg="#000000",  # Button text color
            font=("SF Pro Text", 10),  # Button font
            # relief="flat",  # No border around the button
            activebackground="#F49797",  # Background color when the button is active (clicked)
            activeforeground="#000000"  # Text color when the button is active
        )
        exit_btn.place(relx=0.98, rely=0.02, anchor="ne")  # Place the button near the top-right corner

    def create_main_layout(self):
        """Create the main layout of the window with two frames for data."""
        main_frame = tk.Frame(self, bg="#5DADE2")  # Create a frame for the main content with a blue background
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)  # Pack the main frame to fill the window

        # Left Frame: Original Data
        original_frame = tk.Frame(main_frame, bg="#d3d3d3", relief="groove", borderwidth=2)  # Create a frame for original data
        original_frame.pack(side="left", fill="both", expand=False, padx=10, ipadx=10)  # Adjust frame size

        tk.Label(
            original_frame,
            text="Original Data",  # Title label for original data
            font=self.fonts["header"],  # Use the header font
            bg="#d3d3d3"  # Background color for the label
        ).pack(pady=5)  # Add padding around the label

        # Populate the original data frame with labels and data fields
        self.populate_frame(
            original_frame,
            [
                ("Task Name:", "Save lives"),
                ("Description:", "Save all lives"),
                ("Tags:", "Important"),
                ("Completion Time:", "10 years"),
                ("Time Complexity:", ":)"),
                ("Date Completed:", "December 1, 2035")
            ]
        )

        # Right Frame: Changed Data
        changed_frame = tk.Frame(main_frame, bg="#d3d3d3", relief="groove", borderwidth=2)  # Create a frame for changed data
        changed_frame.pack(side="left", fill="both", expand=False, padx=10, ipadx=10)  # Adjust frame size

        tk.Label(
            changed_frame,
            text="Changed Data",  # Title label for changed data
            font=self.fonts["header"],  # Use the header font
            bg="#d3d3d3"  # Background color for the label
        ).pack(pady=5)  # Add padding around the label

        # Populate the changed data frame with labels and data fields
        self.populate_frame(
            changed_frame,
            [
                ("Task Name:", "Save some lives"),
                ("Description:", "Some lives might not be saved"),
                ("Tags:", "Somewhat important"),
                ("Completion Time:", "Probably not possible"),
                ("Time Complexity:", ":("),
                ("Date Completed:", "December 2, 2035")
            ]
        )

    def populate_frame(self, frame, data_list):
        for label_text, data in data_list:
            # Create and pack labels with the data list
            tk.Label(
                frame,
                text=label_text,  # Label for each data field
                font=self.fonts["body"],  # Use body font
                bg="#d3d3d3"  # Background color for labels
            ).pack(anchor="w", padx=10, pady=5)  # Align labels to the left and add padding

            # Create entry boxes for all fields except "Description:"
            if label_text != "Description:":
                entry_box = tk.Entry(frame, font=("SF Pro Text", 10), width=30, bg="#d3d3d3")  # Set consistent width
                entry_box.insert(0, data)  # Insert the data into the entry box
                entry_box.pack(anchor="w", padx=10, pady=5, fill="x")  # Pack the entry box and align with the text box width

            else:
                # Special case for "Description:" field to use a text box with a scrollbar
                desc_frame = tk.Frame(frame, bg="#AED6F1")  # Create a frame for the description field
                desc_frame.pack(fill="x", padx=10, pady=5)  # Adjust padding to match other fields

                # Scrollbar for the description text
                desc_scrollbar = ttk.Scrollbar(desc_frame, orient="vertical", style="Vertical.TScrollbar")
                desc_scrollbar.pack(side="right", fill="y")  # Pack the scrollbar to the right

                # Text box (Text widget) for multi-line description
                desc_text = tk.Text(
                    desc_frame,
                    height=5,  # Height of the text box
                    width=30,  # Match width to entry boxes
                    bg='#d3d3d3',  # Background color of the text box
                    font=("SF Pro Text", 10),  # Font for the text box
                    yscrollcommand=desc_scrollbar.set,  # Link the scrollbar to the text box
                    wrap="word"  # Enable word wrapping in the text box
                )
                desc_text.insert(tk.END, data)  # Insert the description data into the text box
                desc_text.pack(side='left', fill='x', expand=True)  # Align and expand to fill horizontally

                # Link the scrollbar to the text box
                desc_scrollbar.config(command=desc_text.yview)


# Run the application
if __name__ == "__main__":
    app = CommitHistoryWindow()  # Create an instance of the CommitHistoryWindow class
    app.mainloop()  # Start the Tkinter main loop to display the window
