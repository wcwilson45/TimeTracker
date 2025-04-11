from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
import sqlite3
import csv
import json
from tkinter import messagebox
import pathlib
import os
from .utils import get_writable_db_path

background_color = "#A9A9A9"
green_btn_color = "#b2fba5"
org_btn_color = "#e99e56"

class TagsDB(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        #DATABASE SECTION ############################################

        # Get the path to the resource database
        self.db_resource_path = get_writable_db_path('app/ui/Databases/task_list.db')
        
        # Create user directory path for writable database
        self.user_db_dir = os.path.join(os.getenv("APPDATA"), "TimeTracker")
        os.makedirs(self.user_db_dir, exist_ok=True)
        
        # Path to user's database file
        self.path = os.path.join(self.user_db_dir, "tags.db")
        
        # Copy the database from resources to user directory if it doesn't exist
        if not os.path.exists(self.path):
            import shutil
            shutil.copyfile(self.db_resource_path, self.path)

        # Create or Connect to the database (using user's writable copy)
        conn = sqlite3.connect(self.path)

        # Create a cursor instance
        c = conn.cursor()

        c.execute("""
            CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name TEXT,
            description TEXT
            )
        """)

        # Commit changes
        conn.commit()

        c.execute("SELECT tag_name FROM tags")  # Fetch tag_names from tag database
        tags = c.fetchall()
        global values
        values = []

        # Add data to the list
        for tag in tags:
            values.append(tag[0])

        # Close connection to the database
        conn.close()
        
        def query_database():
            # Create or Connect to the database
            conn = sqlite3.connect(self.path)

            # Create a cursor instance
            c = conn.cursor()

            c.execute("SELECT rowid, * FROM tags")  # Fetch rowid as the first column
            tags = c.fetchall()

            # Add data to the screen
            global count
            count = 0

            for tag in tags:
                if count % 2 == 0:
                    # For even rows (0, 2, 4, ...) apply 'evenrow' tag
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(tag[0], tag[2], tag[3]), tags=('evenrow',""))
                else:
                    # For odd rows (1, 3, 5, ...) apply 'oddrow' tag
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(tag[0], tag[2], tag[3]), tags=('oddrow',""))
                
                # Increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close connection to the database
            conn.close()

        #END OF DATABASE SECTION #################################################


        # Set the main window 
        self.configure(bg=background_color)

        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=14, weight="bold"),
            'subheader': tkfont.Font(family="SF Pro Display", size=10, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=10)
        }

        # Style configurations
        style = ttk.Style(self)
        style.theme_use("alt")  
        style.configure('Input.TEntry', fieldbackground='#d3d3d3', font=("SF Pro Text", 10))
        style.configure('TLabel', background='#d3d3d3', font=("SF Pro Text", 10))  
        style.configure('TButton', background=background_color, font=("SF Pro Text", 10))

        # Create a Treeview Frame
        tree_frame = tk.Frame(self, bg=background_color)
        tree_frame.grid(row=1, column=0, sticky="nsew")

        # Make the tree_frame expand with the window
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Change color when a item is selected
        style.map("Treeview",
        background=[('selected', "#347083")])

        style.configure("Treeview",
        background="black",
        foreground="black",
        rowheight=25,
        fieldbackground="#d3d3d3",
        bd="black")

        # Ensure that tree_frame grid is configured properly
        tree_frame.grid_rowconfigure(0, weight=1)  # Allow row 0 to expand
        tree_frame.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.grid(row=1, column=1, sticky="ns")

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended", style="Treeview")
        my_tree.grid(row=1, column=0, sticky="nsew")

        # Configure the different rows for color
        my_tree.tag_configure('oddrow', background="#A9A9A9", foreground="black")
        my_tree.tag_configure('evenrow', background="#d3d3d3", foreground="black")

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ("ID", "Name", "Description")

        # Format Our Columns - Modified to make Name and Description take full space
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("ID", anchor=W, width=40, stretch=NO)  # Fixed width, no stretch
        my_tree.column("Name", anchor=W, width=100, stretch=YES)  # Will stretch with window
        my_tree.column("Description", anchor=W, width=300, stretch=YES)  # Will stretch with window

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Name", text="Name", anchor=W)
        my_tree.heading("Description", text="Description", anchor=W)
        
        # Add a hidden variable to store the selected tag ID
        self.selected_tag_id = tk.StringVar()
        
        # Modified data_frame section
        data_frame = tk.Frame(self, background=background_color)
        data_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        # Configure grid columns to properly distribute space
        data_frame.grid_columnconfigure(0, weight=1)  # For tag name
        data_frame.grid_columnconfigure(1, weight=1)  # For description (equal weight)

        # Tag Name Label & Text widget (instead of Entry) - Now positioned similar to description
        n_label = ttk.Label(data_frame, text="Tag Name", font=("SF Pro Text", 10, "bold"), background=background_color)
        n_label.grid(row=1, column=0, sticky="w")
        n_entry = Text(data_frame, font=("SF Pro Text", 10), bg="#d3d3d3", height=3, width=30)
        n_entry.grid(row=2, column=0, padx=(0, 20), pady=1, sticky="ew")

        # Description Label & Textbox - Now with scrollbar
        desc_label = Label(data_frame, text="Description", font=("SF Pro Text", 10, "bold"), background=background_color)
        desc_label.grid(row=1, column=1, padx=(10,0), sticky="w")
        
        # Create a frame to hold description text and scrollbar
        desc_frame = tk.Frame(data_frame, background=background_color)
        desc_frame.grid(row=2, column=1, padx=(10,0), pady=1, sticky="ew")
        
        # Create description text widget with same height as name entry
        desc_text = Text(desc_frame, font=("SF Pro Text", 10), height=3, width=40, background="#d3d3d3")
        desc_text.grid(row=0, column=0, sticky="ew")
        
        # Add scrollbar for description
        desc_scroll = Scrollbar(desc_frame, command=desc_text.yview)
        desc_scroll.grid(row=0, column=1, sticky="ns")
        desc_text.config(yscrollcommand=desc_scroll.set)
        
        # Configure desc_frame grid
        desc_frame.grid_columnconfigure(0, weight=1)
        desc_frame.grid_rowconfigure(0, weight=1)

        # START OF FUNCTION SECTION ##############################################

        # Clear entry boxes
        def clear_Tag():
            # Clear entry boxes
            n_entry.delete("1.0", END)
            desc_text.delete("1.0", END)
            # Clear the selected tag ID
            self.selected_tag_id.set("")
        
        # Select Record - Modified to populate entry fields
        def select_tag(event):
            # Clear any existing entries first
            n_entry.delete("1.0", END)
            desc_text.delete("1.0", END)
            
            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')
            
            if values:  # Check if values exist
                # Save ID in the hidden variable
                self.selected_tag_id.set(values[0])
                
                # Populate the entry fields with the selected tag data
                n_entry.insert("1.0", values[1])
                desc_text.insert("1.0", values[2])

        # Remove Tag
        def del_Tag():
            global values  # Move this to the top of the function
            
            # First check if a tag is selected
            selected = my_tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a tag to delete.")
                return
                
            # Get the selected item from the Treeview
            selected = selected[0]
            my_tree.delete(selected)

            # Get the ID from our hidden variable
            tag_id = self.selected_tag_id.get()

            if tag_id:  # Ensure that the ID exists
                # Connecting to the database and creating a cursor
                conn = sqlite3.connect(self.path)
                c = conn.cursor()

                # Delete the tag from the database using a parameterized query
                c.execute("DELETE FROM tags WHERE rowid = ?", (tag_id,))

                conn.commit()
                
                # Update the global values list
                c.execute("SELECT tag_name FROM tags")
                tags = c.fetchall()
                values = [tag[0] for tag in tags]
                
                conn.close()

                # Clear entry boxes
                n_entry.delete("1.0", END)
                desc_text.delete("1.0", END)
                self.selected_tag_id.set("")

        # Remove all Tags
        def remove_all_Tags():
            global values  # Move this to the top of the function
            
            # Add a little message box for fun
            response = messagebox.askyesno("Delete All Tags", "This Will Delete EVERYTHING from the database.\nAre You Sure?")

            #Add logic for message box
            if response == 1:
                # Clear the Treeview
                for tag in my_tree.get_children():
                    my_tree.delete(tag)

                # Create a database or connect to one that exists
                conn = sqlite3.connect(self.path)

                # Create a cursor instance
                c = conn.cursor()

                # Delete Everything From The Table
                c.execute("DROP TABLE tags")

                c.execute("""
                    CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tag_name TEXT,
                    description TEXT
                    )
                """)
                            
                # Commit changes
                conn.commit()
                
                # Update the global values list
                values = []
                
                # Close our connection
                conn.close()

                # Clear entry boxes if filled
                n_entry.delete("1.0", END)
                desc_text.delete("1.0", END)
                self.selected_tag_id.set("")

        # Add Tag to db
        def add_Tag():
            global values  # Move this to the top of the function
            
            tag_name = n_entry.get("1.0", "end-1c")  # Changed to get text from Text widget
            
            if tag_name not in values:
                #Create db connection
                conn = sqlite3.connect(self.path)

                # Create cursor
                c = conn.cursor()
                c.execute("INSERT INTO tags (tag_name, description) VALUES (:name, :desc)",
                {
                    'name': tag_name,
                    'desc': desc_text.get("1.0", "end-1c")
                })

                conn.commit()
                
                # Update the global values list
                c.execute("SELECT tag_name FROM tags")
                tags = c.fetchall()
                values = [tag[0] for tag in tags]
                
                conn.close()

                # Clear entry boxes
                n_entry.delete("1.0", END)
                desc_text.delete("1.0", END)
                self.selected_tag_id.set("")

                # Clear Treeview table
                my_tree.delete(*my_tree.get_children())

                # Query Data base to add data
                query_database()

            else:
                messagebox.showwarning("Warning", f"The tag you're adding already exists.")
            self.lift()
            self.focus_force()
            return

        # Update Tag
        def update_Tag():
            global values  # Move this to the top of the function
            
            # Check if a tag is selected
            if not self.selected_tag_id.get():
                messagebox.showwarning("Warning", "Please select a tag to update.")
                return
                
            # Grab the tag number
            selected = my_tree.focus()

            # Update tag in treeview
            my_tree.item(selected, text="", values=(self.selected_tag_id.get(), 
                                                   n_entry.get("1.0", "end-1c"), 
                                                   desc_text.get("1.0", "end-1c")))

            # Update the database
            conn = sqlite3.connect(self.path)
            c = conn.cursor()

            c.execute("""UPDATE tags SET
                tag_name = :name,
                description = :desc
                WHERE rowid = :id""",
                {
                    'name': n_entry.get("1.0", "end-1c"),
                    'desc': desc_text.get("1.0", "end-1c"),
                    'id': self.selected_tag_id.get(),
                }
            )

            conn.commit()
            
            # Update the global values list
            c.execute("SELECT tag_name FROM tags")
            tags = c.fetchall()
            values = [tag[0] for tag in tags]
            
            conn.close()

            # Clear entry boxes
            n_entry.delete("1.0", END)
            desc_text.delete("1.0", END)
            self.selected_tag_id.set("")

        def search_Tag(event):
            #Getting the name they entered
            lookup = search_entry.get()

            # Create or Connect to the database
            conn = sqlite3.connect(self.path)

            # Create a cursor instance
            c = conn.cursor()

            # Clear the Treeview
            for tag in my_tree.get_children():
                my_tree.delete(tag)

            if lookup == "":
                c.execute("SELECT rowid, * FROM tags")  # Fetch all rows
            else:
                c.execute("SELECT rowid, * FROM tags WHERE tag_name like ?", (f"%{lookup}%",)) 
                
            tags = c.fetchall()
            
            # Add data to the screen
            global count
            count = 0

            for tag in tags:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(tag[0], tag[2], tag[3]), tags=('evenrow',""))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(tag[0], tag[2], tag[3]), tags=('oddrow',""))

                # Increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close connection to the database
            conn.close()
            
        def import_Tags():
            global values  # Move this to the top of the function
            
            try:
                # Ask user for the file
                file_path = tk.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

                # If file has been selected, proceed
                if file_path:
                    # Open the file and read from it
                    with open(file_path, "r", encoding="utf-8-sig") as file:
                        csv_reader = csv.reader(file)
                        data = list(csv_reader)

                        # Check if the first row is a header (by comparing column names)
                        if data:
                            header = data[0]
                            expected_header = ["Tag Name", "Description"]

                            # If the first row matches the header, remove it
                            if header == expected_header:
                                data = data[1:]

                    # Fetch existing tag names from the database
                    conn = sqlite3.connect(self.path)
                    c = conn.cursor()
                    c.execute("SELECT tag_name FROM tags")
                    existing_tags = [tag[0] for tag in c.fetchall()]  # List of tag names already in the DB
                    
                    # Track successful imports and failures
                    imported_count = 0
                    duplicates = []
                    
                    # Import tags from CSV to the database
                    for tag in data:
                        tag_name = tag[0]
                        description = tag[1]
                        
                        # Check if the tag already exists in the database
                        if tag_name not in existing_tags:
                            # Insert data into the table
                            c.execute("INSERT INTO tags (tag_name, description) VALUES (?, ?)", (tag_name, description))
                            existing_tags.append(tag_name)  # Update our local list
                            imported_count += 1
                        else:
                            duplicates.append(tag_name)
                    
                    # Commit all changes at once
                    conn.commit()
                    
                    # Update the global values list
                    c.execute("SELECT tag_name FROM tags")
                    tags = c.fetchall()
                    values = [tag[0] for tag in tags]
                    
                    conn.close()
                    
                    # Report the results
                    if duplicates:
                        messagebox.showwarning("Import Results", 
                            f"Imported {imported_count} tags successfully.\n"
                            f"Skipped {len(duplicates)} duplicate tags: {', '.join(duplicates[:5])}"
                            f"{'...' if len(duplicates) > 5 else ''}")
                    elif imported_count > 0:
                        messagebox.showinfo("Import Success", f"Successfully imported {imported_count} tags.")
                    
                    # Clear Treeview table
                    my_tree.delete(*my_tree.get_children())
                    
                    # Query the database to update the Treeview with new data
                    query_database()
            except Exception as e:
                messagebox.showerror("Import Error", f"An error occurred during import: {str(e)}")
                # Ensure we lift and focus after error
                self.lift()
                self.focus_force()

        def export_Tags():
            try:
                # Connect to the database
                conn = sqlite3.connect(self.path)
                c = conn.cursor()
                
                # Fetch all tags
                c.execute("SELECT tag_name, description FROM tags")
                tags = c.fetchall()
                
                if not tags:
                    messagebox.showinfo("Export Info", "There are no tags to export.")
                    return
                    
                # Ask user where to save the file
                file_path = tk.filedialog.asksaveasfilename(
                    defaultextension=".csv", 
                    filetypes=[("CSV Files", "*.csv")]
                )
                
                if not file_path:  # User canceled the save dialog
                    return
                    
                # Open the CSV file for writing
                with open(file_path, "w", newline='', encoding='utf-8') as file:
                    csv_writer = csv.writer(file)
                    
                    # Write the header
                    csv_writer.writerow(["Tag Name", "Description"])
                    
                    # Write data rows
                    for tag in tags:
                        csv_writer.writerow(tag)
                        
                messagebox.showinfo("Export Success", f"Successfully exported {len(tags)} tags to {file_path}")
                
            except Exception as e:
                messagebox.showerror("Export Error", f"An error occurred during export: {str(e)}")
            finally:
                # Close the database connection
                if 'conn' in locals():
                    conn.close()
            
        #END OF FUNCTION SECTION ########################################

        # Modified search frame for Import/Export buttons
        search_frame = tk.Frame(self, bg=background_color)
        search_frame.grid(row=0, column=0, padx=1, pady=1, sticky="ew")

        # Configure grid columns for proper spacing
        search_frame.grid_columnconfigure(0, weight=0)  # Label
        search_frame.grid_columnconfigure(1, weight=1)  # Search entry
        search_frame.grid_columnconfigure(2, weight=0)  # Buttons container

        # Search bar label
        search_label = Label(search_frame, text="Search by Tag Name:", font=("SF Pro Text", 10, "bold"), background=background_color)
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Entry for search bar for user to input search
        search_entry = tk.Entry(search_frame, font=("SF Pro Text", 10), bg="#d3d3d3")
        search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        search_entry.bind("<KeyRelease>", search_Tag)

        # Button container for import/export buttons (right aligned)
        button_container = tk.Frame(search_frame, bg=background_color)
        button_container.grid(row=0, column=2, padx=(0, 5), pady=5, sticky="e")

        # Import Button
        import_btn = tk.Button(button_container, text=" Import ", command=import_Tags,
                                bg=green_btn_color, fg="#000000", font=("SF Pro Text", 10),
                                activebackground="#A8F0A8", activeforeground="#000000")
        import_btn.grid(row=0, column=0, pady=3, padx=(0, 10), sticky="e")

        # Export Button
        export_btn = tk.Button(button_container, text=" Export ", command=export_Tags,
                                bg=green_btn_color, fg="#000000", font=("SF Pro Text", 10),
                                activebackground="#A8F0A8", activeforeground="#000000")
        export_btn.grid(row=0, column=1, pady=3, padx=(0, 0), sticky="e")

        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_tag)

        # Button frame - now positioned below the entry boxes
        button_frame = tk.Frame(self, background=background_color)
        button_frame.grid(row=3, column=0, pady=10, padx=5, sticky="ew")  # Changed row from 7 to 3

        # Configure columns of the button_frame to properly distribute buttons
        button_frame.grid_columnconfigure(0, weight=1)  # Left side for standard buttons
        button_frame.grid_columnconfigure(1, weight=1)  # Right side for delete buttons

        # Left side frame for standard buttons
        left_buttons = tk.Frame(button_frame, bg=background_color)
        left_buttons.grid(row=0, column=0, sticky="w")

        # Right side frame for delete buttons
        right_buttons = tk.Frame(button_frame, bg=background_color)
        right_buttons.grid(row=0, column=1, sticky="e")

        # Add Tag Button - left side
        add_btn = tk.Button(left_buttons, text=" Add Tag ",  
                            bg=green_btn_color, fg="#000000", font=("SF Pro Text", 10), command=add_Tag,
                            activebackground="#A8F0A8", activeforeground="#000000")
        add_btn.grid(row=0, column=0, pady=2, padx=(0, 3), sticky="w")

        # Update Button - left side
        update_btn = tk.Button(left_buttons, text="Update Tag", command=update_Tag,
                            bg=green_btn_color, fg="#000000", font=("SF Pro Text", 10),
                            activebackground="#A8F0A8", activeforeground="#000000")
        update_btn.grid(row=0, column=1, pady=2, padx=3, sticky="w")

        # Clear Tag Button - left side
        clc_btn = tk.Button(left_buttons, text="Clear Tag", command=clear_Tag,
                            bg=green_btn_color, fg="#000000", font=("SF Pro Text", 10),
                            activebackground="#A8F0A8", activeforeground="#000000")
        clc_btn.grid(row=0, column=2, pady=2, padx=3, sticky="w")

        # Delete Tag Button - right side
        del_btn = tk.Button(right_buttons, text="Delete Tag", command=del_Tag,
                            bg=org_btn_color, fg="#000000", font=("SF Pro Text", 10),
                            activebackground="#FFB347", activeforeground="#000000")
        del_btn.grid(row=0, column=0, pady=2, padx=3, sticky="e")

        # Remove All Button - right side
        remove_all_btn = tk.Button(right_buttons, text="Remove All", command=remove_all_Tags,
                                    bg=org_btn_color, fg="#000000", font=("SF Pro Text", 10),
                                    activebackground="#FFB347", activeforeground="#000000")
        remove_all_btn.grid(row=0, column=1, pady=2, padx=3, sticky="e")

        # Run to pull data from database on start
        query_database()