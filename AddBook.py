import customtkinter
import tkinter as tk
from database import LMS
from tkinter.messagebox import showerror, showwarning, showinfo
from tkcalendar import DateEntry
import datetime
import os
import sys

db= LMS("lms.db")
class AddBook(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Add New Book")
        self.geometry("600x500")
        self.configure(bg="black")  # Set background color
        self.setup_ui()

    def setup_ui(self):
        # Define colors
        bg_color = "black"
        fg_color = "white"
        button_bg_color = "white"  # Button background color
        button_fg_color = "black"  # Button foreground color

        # Create and configure widgets
        heading_frame = tk.Frame(self, bg=bg_color)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        label = tk.Label(heading_frame, text="Add New Book", font=("Robot", 25, "bold"), bg=bg_color, fg=fg_color)
        label.pack(ipady=10)

        main_frame = tk.Frame(self, bg=bg_color)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

        # Labels
        labels = ["Book ID", "Book Name", "Book Author", "Book Edition", "Book Price"]
        for i, label_text in enumerate(labels, start=1):
            label = tk.Label(main_frame, text=f"{label_text} *", bg=bg_color, fg=fg_color)
            label.grid(column=1, row=i, padx=5, pady=5, sticky="e")
            label.configure(font=("Robot", 12, "normal"))

        # Entry fields
        self.book_id_input = tk.Entry(main_frame, width=30)
        self.book_id_input.grid(column=2, row=1, padx=5, pady=5)
        self.book_nme_input = tk.Entry(main_frame, width=30)
        self.book_nme_input.grid(column=2, row=2, padx=5, pady=5)
        self.book_author_input = tk.Entry(main_frame, width=30)
        self.book_author_input.grid(column=2, row=3, padx=5, pady=5)
        self.book_edition_input = tk.Entry(main_frame, width=30)
        self.book_edition_input.grid(column=2, row=4, padx=5, pady=5)
        self.book_price_input = tk.Entry(main_frame, width=30)
        self.book_price_input.grid(column=2, row=5, padx=5, pady=5)

        # Purchased Date
        purchase_dt_label = tk.Label(main_frame, text="Purchased Date *", bg=bg_color, fg=fg_color)
        purchase_dt_label.grid(column=1, row=6, padx=5, pady=5, sticky="e")
        purchase_dt_label.configure(font=("Robot", 12, "normal"))
        dt = datetime.datetime.now()
        dt_year = dt.year
        self.purch_dt_var = tk.StringVar(self)
        self.purchase_dt = DateEntry(main_frame, width=30, borderwidth=2, year=dt_year, textvariable=self.purch_dt_var)
        self.purchase_dt.grid(column=2, row=6, padx=5, pady=5)

        # Add Book Button
        add_new_book_btn = tk.Button(main_frame, text="Add Book", font=("Verdana", 16, "bold" ), bg=button_bg_color,
                                     fg=button_fg_color, command=self.save_new_book)
        add_new_book_btn.grid(column=2, row=7, padx=10, pady=5, ipadx=10, ipady=10)

    def save_new_book(self):
        book_id = self.book_id_input.get()
        book_nme = self.book_nme_input.get()
        book_author = self.book_author_input.get()
        book_edition = self.book_edition_input.get()
        book_price = self.book_price_input.get()
        purchase_dt = self.purch_dt_var.get()

        # Check if book ID already exists
        existing_book = db.get_book_by_id(book_id)
        if existing_book:
            showerror(title="Duplicate Book ID", message="Book ID already exists")
            return
        if not book_id.isdigit():
            showerror(title="Book ID", message="Please enter a correct Book ID")
        if not self.validate_input(book_nme):
            showerror(title="Book Name", message="Please enter a correct Book Name")
            return
        if not self.validate_input(book_author):
            showerror(title="Book Author", message="Please enter a correct Book Author")
            return
        if not self.validate_input(book_edition):
            showerror(title="Book Edition", message="Please enter a correct Book Edition")
            return
        if not self.validate_input(book_price, allow_decimal=True):
            showerror(title="Book Price", message="Please enter a correct Book Price")
            return

        if book_id != "" and book_nme != "" and book_author != "" and book_edition != "" and book_price != "" and purchase_dt != "":
            data = (
                book_id,
                book_nme,
                book_author,
                book_edition,
                book_price,
                purchase_dt,
                "available"
            )
            
            res = db.add_new_book(data)
            if res != None or res != '':
                self.book_id_input.delete(0,'end')
                self.book_nme_input.delete(0,'end')
                self.book_author_input.delete(0,'end')
                self.book_edition_input.delete(0,'end')
                self.book_price_input.delete(0,'end')
                #self.purchase_dt_inp.delete(0,'end')
                showinfo(title="Saved",message="New book saved successfully.")
            else:
                showerror(title="Not Saved",message="Something went wrong. Please try again...")
        else:
            showerror(title="Empty Fields",message="Please fill all the details then submit!")

    def validate_input(self, value, allow_decimal=False):
        # Function to validate text input, allowing only letters, digits, and optionally a decimal point
        if allow_decimal:
            return all(char.isalnum() or char == '.' or char.isspace() for char in value)
        else:
            return all(char.isalnum() or char.isspace() for char in value)
if __name__ == "__main__":
    root = tk.Tk()
    app = AddBook(root)
    app.mainloop()