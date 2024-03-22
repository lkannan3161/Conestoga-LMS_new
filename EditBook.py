import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from tkcalendar import DateEntry
from database import LMS
import datetime
import re

db = LMS("lms.db")

class EditBook(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Edit Book")
        self.geometry("600x500")
        self.configure(bg="black")  # Set background color

        # Initialize StringVars
        self.id_var = tk.StringVar(self)
        self.name_var = tk.StringVar(self)
        self.author_var = tk.StringVar(self)
        self.edition_var = tk.StringVar(self)
        self.price_var = tk.StringVar(self)
        self.purchase_dt_var = tk.StringVar(self)

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

        label = tk.Label(heading_frame, text="Edit Book", font=("Robot", 25, "bold"), bg=bg_color, fg=fg_color)
        label.pack(ipady=10)

        main_frame = tk.Frame(self, bg=bg_color)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

        # Search fields
        search_frame = tk.Frame(main_frame, bg=bg_color)
        search_frame.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        # Entry field
        self.book_id_input1 = tk.Entry(search_frame, width=30, bg=fg_color, fg=bg_color)
        self.book_id_input1.pack(side="left", padx=(10, 5))  # Increased padx value to add more space

        # Button
        search_btn = tk.Button(search_frame, text="Search ID", font=("Verdana", 12, "bold"), bg=button_bg_color,
                               fg=button_fg_color, command=self.search_book_detail, height=2)
        search_btn.pack(side="left", padx=(5, 0))  # Decreased padx value to move the button to the right

        # Labels
        labels = ["Book ID", "Book Name", "Book Author", "Book Edition", "Book Price", "Purchased Date"]
        for i, label_text in enumerate(labels, start=1):
            label = tk.Label(main_frame, text=f"{label_text}", bg=bg_color, fg=fg_color)
            label.grid(column=1, row=i, padx=5, pady=5, sticky="e")
            label.configure(font=("Robot", 12, "normal"))

        # Entry fields
        self.book_id_input = tk.Entry(main_frame, width=30, textvariable=self.id_var, state='disabled')
        self.book_id_input.grid(column=2, row=1, padx=5, pady=5)
        self.book_nme_input = tk.Entry(main_frame, width=30, textvariable=self.name_var)
        self.book_nme_input.grid(column=2, row=2, padx=5, pady=5)
        self.book_author_input = tk.Entry(main_frame, width=30, textvariable=self.author_var)
        self.book_author_input.grid(column=2, row=3, padx=5, pady=5)
        self.book_edition_input = tk.Entry(main_frame, width=30, textvariable=self.edition_var)
        self.book_edition_input.grid(column=2, row=4, padx=5, pady=5)
        self.book_price_input = tk.Entry(main_frame, width=30, textvariable=self.price_var)
        self.book_price_input.grid(column=2, row=5, padx=5, pady=5)

        # Purchased Date
        purchase_dt_label = tk.Label(main_frame, text="Purchased Date", bg=bg_color, fg=fg_color)
        purchase_dt_label.grid(column=1, row=6, padx=5, pady=5, sticky="e")
        purchase_dt_label.configure(font=("Robot", 12, "normal"))
        dt = datetime.datetime.now()
        dt_year = dt.year
        self.purchase_dt = DateEntry(main_frame, width=30, borderwidth=2, year=dt_year, textvariable=self.purchase_dt_var)
        self.purchase_dt.grid(column=2, row=6, padx=5, pady=5)

        # Update Book Button
        update_book_btn = tk.Button(main_frame, text="Update Book", font=("Verdana", 16, "bold"), bg=button_bg_color,
                                     fg=button_fg_color, command=self.update_book)
        update_book_btn.grid(column=2, row=7, padx=10, pady=5, ipadx=10, ipady=10)

    def search_book_detail(self):
        book_id = self.book_id_input1.get()
        if book_id.isdigit():
            book_id = int(book_id)
            book_details = db.select_book_detail(book_id)
            if book_details:
                self.id_var.set(book_details[0])
                self.name_var.set(book_details[1])
                self.author_var.set(book_details[2])
                self.edition_var.set(book_details[3])
                self.price_var.set(book_details[4])
                self.purchase_dt_var.set(book_details[5])
            else:
                showerror(title="Not Found", message="Book Not Found")
        else:
            showerror(title="Book ID", message="Please enter a correct Book ID")

    def update_book(self):
        book_id = self.id_var.get()
        book_nme = self.name_var.get()
        book_author = self.author_var.get()
        book_edition = self.edition_var.get()
        book_price = self.price_var.get()
        purchase_dt = self.purchase_dt_var.get()

        # Validate book price format
        if not self.validate_price(book_price):
            showerror(title="Invalid Price", message="Please enter a valid price.")
            return

        # Validate special characters in all fields
        fields = [book_nme, book_author, book_edition, book_price]
        if not self.validate_special_characters(fields):
            showerror(title="Invalid Input", message="Special characters are not allowed.")
            return

        # Validate future dates
        if self.is_future_date(purchase_dt):
            showerror(title="Invalid Date", message="Future dates are not allowed.")
            return

        if all([book_id, book_nme, book_author, book_edition, book_price, purchase_dt]):
            data = (
                book_id,
                book_nme,
                book_author,
                book_edition,
                book_price,
                purchase_dt,
                book_id
            )

            res = db.update_book_details(data)
            res = db.update_book_details(data)
            if res != None or res != '':
                showinfo(title="Saved", message="Book updated successfully.")
            else:
                showerror(title="Not Saved", message="Something went wrong. Please try again...")
        else:
            showerror(title="Empty Fields", message="Please fill all the details then submit!")

    def validate_price(self, price):
        try:
            float(price)
            return True
        except ValueError:
            return False

    def validate_special_characters(self, fields):
        for field in fields:
            if not re.match(r'^[a-zA-Z0-9\s\-\'\.]+$', field):
                return False
        return True

    def is_future_date(self, date_str):
        try:
            selected_date = datetime.datetime.strptime(date_str, "%m/%d/%y").date()
            today_date = datetime.datetime.now().date()
            is_future = selected_date > today_date
            return is_future
        except ValueError:
            return False
if __name__ == "__main__":
    root = tk.Tk()
    app = EditBook(root)
    app.mainloop()



