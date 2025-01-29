from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import tkinter as tk
import tkinter.font as tkfont
import sqlite3
from tkinter import messagebox




class TagsDB(tk.Toplevel):
    def __init__(self,parent):
        super().__init__(parent)
        #DATABASE SECTION

        # Create or Connect to database
        conn = sqlite3.connect("tags.db")

        #Create a cursor instnace
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

        # Close connection to database
        conn.close()

        def create_table_again():
            # Create a database or connect to one that exists
            conn = sqlite3.connect('tree_crm.db')

            # Create a cursor instance
            c = conn.cursor()

            # Create Table
            c.execute("""
            CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tag_name TEXT,
            description TEXT
            )
        """)
            # Commit changes
            conn.commit()

            # Close our connection
            conn.close()

        def query_database():
            # Create or Connect to the database
            conn = sqlite3.connect('tags.db')

            # Create a cursor instance
            c = conn.cursor()

            c.execute("SELECT rowid, * FROM tags")  # Fetch rowid as the first column
            tags = c.fetchall()

            # Add data to the screen
            global count
            count = 0

            for tag in tags:
                if count % 2 == 0:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(tag[0], tag[2], tag[3]), tags=('evenrow',))
                else:
                    my_tree.insert(parent='', index='end', iid=count, text='', values=(tag[0], tag[2], tag[3]), tags=('oddrow',))

                # Increment counter
                count += 1

            # Commit changes
            conn.commit()

            # Close connection to the database
            conn.close()

        #END OF DATABASE SECTION

        # Main container
        main_frame = tk.Frame(self, bg='#5DADE2', bd=0)
        main_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # Set the main window geometry and title
        self.geometry("660x620")  
        self.title("Tag DataBase")
        self.configure(bg='#5DADE2')
        self.resizable(False, False)

        # Create fonts
        self.fonts = {
            'header': tkfont.Font(family="SF Pro Display", size=14, weight="bold"),
            'subheader': tkfont.Font(family="SF Pro Display", size=10, weight="bold"),
            'body': tkfont.Font(family="SF Pro Text", size=10)
        }

        # Style configurations
        self.style = ttk.Style(self)
        self.style.theme_use("alt")  
        self.style.configure('Input.TEntry', fieldbackground='#d3d3d3', font=("SF Pro Text", 10))
        self.style.configure('TLabel', background='#d3d3d3', font=("SF Pro Text", 10))  
        self.style.configure('TButton', background='#5DADE2', font=("SF Pro Text", 10))

        # Create a Treeview Frame
        tree_frame = tk.Frame(main_frame, bg='#D3D3D3')
        tree_frame.grid(row=0, column=0, padx=1, pady=1, columnspan=4, sticky="nsew")

        # Create a Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create The Treeview
        my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        my_tree.pack()

        # Configure the Scrollbar
        tree_scroll.config(command=my_tree.yview)

        # Define Our Columns
        my_tree['columns'] = ("ID", "Name", "Description")

        # Format Our Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Name", anchor=W, width=80)
        my_tree.column("Description", anchor=W, width=240)
        my_tree.column("ID", anchor=W, width=20)

        # Create Headings
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("ID", text="ID", anchor=W)
        my_tree.heading("Name", text="Name", anchor=W)
        my_tree.heading("Description", text="Description", anchor=W)

        data_frame = LabelFrame(self, text="Tag")
        data_frame.grid(row=1, column=0, padx=10, pady=10, columnspan=4, sticky="nsew")

     
        # ID Label
        id_label = Label(data_frame, text="ID", font=("SF Pro Text", 10))
        id_label.grid(row=0, column=0, padx=1, pady=5, sticky="w")

        # Change the ID entry to a Label to hold the ID (non-editable)
        id_display = Label(data_frame, font=("SF Pro Text", 10))
        id_display.grid(row=1, column=0, padx=1, pady=5, sticky="w")

        # Tag Name Label & Entry
        n_label = Label(data_frame, text="Tag Name", font=("SF Pro Text", 10))
        n_label.grid(row=2, column=0, padx=1, pady=5, sticky="w")
        n_entry = Entry(data_frame, font=("SF Pro Text", 10))
        n_entry.grid(row=3, column=0, padx=1, pady=5, sticky="w")

        # Description Label & Textbox
        desc_label = Label(data_frame, text="Description", font=("SF Pro Text", 10))
        desc_label.grid(row=4, column=0, padx=1, pady=5, sticky="w")
        desc_text = Text(data_frame, font=("SF Pro Text", 10), height=5, width=40)
        desc_text.grid(row=5, column=0, padx=1, pady=5, sticky="w")

        # START OF FUNCTION SECTION

        # Clear entry boxes
        def clear_Tag():
            # Clear entry boxes
            n_entry.delete(0, END)
            desc_text.delete("1.0", END)
        
        # Select Record
        def select_tag(event):
            # Clear entry boxes
            n_entry.delete(0, END)
            desc_text.delete("1.0", END)
            id_display.configure(text="")

            # Grab record Number
            selected = my_tree.focus()
            # Grab record values
            values = my_tree.item(selected, 'values')

            # Populate entry boxes
            id_display.configure(text=values[0])  # Insert ID
            n_entry.insert(0, values[1])  # Insert name
            desc_text.insert("1.0", values[2])  # Insert description



        # Remove Tag
        def del_Tag():
            # Get the selected item from the Treeview
            selected = my_tree.selection()[0]
            my_tree.delete(selected)

            # Get the ID from the label (this will hold the ID for the selected tag)
            tag_id = id_display.cget("text")

            if tag_id:  # Ensure that the ID exists
                # Connecting to the database and creating a cursor
                conn = sqlite3.connect('tags.db')
                c = conn.cursor()

                # Delete the tag from the database using a parameterized query
                c.execute("DELETE FROM tags WHERE rowid = ?", (tag_id,))

                conn.commit()
                conn.close()

                # Clear entry boxes
                n_entry.delete(0, END)
                desc_text.delete("1.0", END)
                id_display.configure(text="")
            

        # Remove all Tags
        def remove_all_Tags():
            # Add a little message box for fun
            response = messagebox.askyesno("WOAH!!!!", "This Will Delete EVERYTHING From The Table\nAre You Sure?!")

            #Add logic for message box
            if response == 1:
                # Clear the Treeview
                for tag in my_tree.get_children():
                    my_tree.delete(tag)

                # Create a database or connect to one that exists
                conn = sqlite3.connect('tags.db')

                # Create a cursor instance
                c = conn.cursor()

                # Delete Everything From The Table
                c.execute("DROP TABLE tags")
                    


                # Commit changes
                conn.commit()

                # Close our connection
                conn.close()

                # Clear entry boxes if filled
                n_entry.delete(0, END)
                desc_text.delete("1.0", END)
                id_display.configure(text="")


                # Recreate The Table
                create_table_again()

                

            

        # Move Row Up
        def up():
            rows = my_tree.selection()
            for row in rows:
                my_tree.move(row, my_tree.parent(row), my_tree.index(row)-1)

        # Move Row Down
        def down():
            rows = my_tree.selection()
            for row in reversed(rows):
                my_tree.move(row, my_tree.parent(row), my_tree.index(row)+1)


        # Add Tag to db
        def add_Tag():
            #Create db connection
            conn = sqlite3.connect('tags.db')

            # Create cursor
            c = conn.cursor()

            c.execute("INSERT INTO tags (tag_name, description) VALUES (:name, :desc)",
              {
                'name': n_entry.get(),
                'desc': desc_text.get("1.0", "end-1c")
              })

            conn.commit()
            conn.close()

            # Clear entry boxes
            n_entry.delete(0, END)
            desc_text.delete("1.0", END)
            id_display.configure(text="")

            # Clear Treeview table
            my_tree.delete(*my_tree.get_children())

            # Query Data base to add data
            query_database()


        # Update Tag
        def update_Tag():
            # Grab the tag number
            selected = my_tree.focus()

            # Update tag in treeview
            my_tree.item(selected, text="", values=(id_display.cget("text"), n_entry.get(), desc_text.get("1.0", "end-1c")))

            # Update the database
            conn = sqlite3.connect('tags.db')
            c = conn.cursor()

            c.execute("""UPDATE tags SET
                tag_name = :name,
                description = :desc
                WHERE rowid = :id""",
                {
                    'name': n_entry.get(),
                    'desc': desc_text.get("1.0", "end-1c"),
                    'id': id_display.cget("text"),
                }
            )

            conn.commit()
            conn.close()

            # Clear entry boxes
            n_entry.delete(0, END)
            desc_text.delete("1.0", END)
            id_display.configure(text="")

            

        #END OF FUNCTION SECTION

        # Bind the treeview
        my_tree.bind("<ButtonRelease-1>", select_tag)

        # Frame for the buttons
        button_frame = tk.Frame(data_frame)
        button_frame.grid(row=6, column=0, columnspan=4, pady=5, padx=5, sticky="w")

        # Configure columns of the button_frame to prevent stretching
        button_frame.grid_columnconfigure(0, weight=0, minsize=80)  # Set a smaller minimum size for each column
        button_frame.grid_columnconfigure(1, weight=0, minsize=80)
        button_frame.grid_columnconfigure(2, weight=0, minsize=80)
        button_frame.grid_columnconfigure(3, weight=0, minsize=80)

        # Add Tag Button
        add_btn = tk.Button(button_frame, text="Add Tag",  
                            bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),command= add_Tag,
                            relief="flat", activebackground="#A8F0A8", activeforeground="#000000")
        add_btn.grid(row=0, column=0, pady=2, padx=3, sticky="w")

        # Delete Tag Button
        del_btn = tk.Button(button_frame, text="Delete Tag", command=del_Tag,
                            bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),
                            relief="flat", activebackground="#A8F0A8", activeforeground="#000000")
        del_btn.grid(row=0, column=1, pady=2, padx=3, sticky="w")


        # Clear Task Button
        clc_btn = tk.Button(button_frame, text="Clear Task", command=clear_Tag,
                            bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),
                            relief="flat", activebackground="#A8F0A8", activeforeground="#000000")
        clc_btn.grid(row=0, column=2, pady=2, padx=3, sticky="w")

        # Move Up Button
        up_btn = tk.Button(button_frame, text="Move Up", command=up,
                        bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),
                        relief="flat", activebackground="#A8F0A8", activeforeground="#000000")
        up_btn.grid(row=0, column=3, pady=2, padx=3, sticky="w")

        # Move Down Button
        dwn_btn = tk.Button(button_frame, text="Move Down", command=down,
                            bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),
                            relief="flat", activebackground="#A8F0A8", activeforeground="#000000")
        dwn_btn.grid(row=0, column=4, pady=2, padx=3, sticky="w")

        # Remove All Button
        dwn_btn = tk.Button(button_frame, text="Remove All", command=remove_all_Tags,
                            bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),
                            relief="flat", activebackground="#A8F0A8", activeforeground="#000000")
        dwn_btn.grid(row=0, column=5, pady=2, padx=3, sticky="w")

        # Update Button
        dwn_btn = tk.Button(button_frame, text="Update Tag", command=update_Tag,
                            bg="#90EE90", fg="#000000", font=("SF Pro Text", 10),
                            relief="flat", activebackground="#A8F0A8", activeforeground="#000000")
        dwn_btn.grid(row=0, column=6, pady=2, padx=3, sticky="w")

        # Run to pull data from database on start
        query_database()
        