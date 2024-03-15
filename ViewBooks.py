import tkinter as tk
from tkinter import ttk
from database import LMS
import datetime

db = LMS("lms.db")

class ViewBooks(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("View Books")
        self.state('zoomed')
        self.geometry('1920x1080')
        self.config(bg="black")

        # Create a custom style for the treeview
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Verdana", 12, "bold"))

        heading_frame = tk.Frame(self, bg="black")
        heading_frame.pack(pady=(20, 10))

        label = tk.Label(heading_frame, text="View Books", font=("Roboto", 25, "bold"), fg="white", bg="black")
        label.pack()

        main_frame = tk.Frame(self, bg="black")
        main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        columns = ('Book ID', 'Name', 'Author', 'Edition', 'Price', 'Purchased Date', 'Status')

        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', selectmode="browse")

        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)

        self.load_book_data()

        self.tree.pack(side="left", fill="both", expand=True)

        # Add vertical scrollbar
        vscrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        vscrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=vscrollbar.set)

        # Add horizontal scrollbar
        hscrollbar = ttk.Scrollbar(main_frame, orient="horizontal", command=self.tree.xview)
        hscrollbar.pack(side="bottom", fill="x")
        self.tree.configure(xscrollcommand=hscrollbar.set)

        self.tree.bind('<<TreeviewSelect>>', self.item_selected)

    def load_book_data(self):
        book_list = db.view_book_list()
        for i in book_list:
            self.tree.insert('', 'end', values=i)

    def item_selected(self, event):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)
            record = item['values']
            self.details_win(record)

    def details_win(self, record):
        window = tk.Toplevel(self)
        window.title("Book Details")
        window.geometry('400x300')
        window.config(bg="black")

        labels = ["Book ID", "Name", "Author", "Edition", "Price", "Purchased Date", "Status"]

        for i, label_text in enumerate(labels):
            label = tk.Label(window, text=label_text + ":", font=("Verdana", 12), fg="white", bg="black")
            label.grid(row=i, column=0, padx=10, pady=5, sticky="e")

            value = tk.StringVar(window, record[i])
            entry = tk.Entry(window, font=("Verdana", 12), textvariable=value, state='readonly', bg="white", fg="black")
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
