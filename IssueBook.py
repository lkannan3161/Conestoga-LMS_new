import customtkinter
import tkinter as tk
from database import LMS
from tkinter.messagebox import showerror, showinfo
import datetime
import requests

db = LMS("lms.db")

settings_file_url = "https://raw.githubusercontent.com/lkannan3161/Conestoga-LMS_new/main/config/settings.json"

response = requests.get(settings_file_url)
if response.status_code == 200:
    settings = response.json()
else:
    print("Using default settings.")
    # Define default settings here if needed

class IssueBook(customtkinter.CTkToplevel):
    def __init__(self, master=None, settings=None):
        super().__init__(master)
        self.title("Library Management System")
        self.minsize(400, 250)
        self.maxsize(400, 250)
        self.geometry('300x250')
        self.attributes("-topmost", True)

        self.settings = settings
        self.no_expiry_days = getattr(self.settings, "get", lambda key, default: default)("issue_duration", 30)
        # Default to 30 days if not found

        self.setup_ui()

    def setup_ui(self):
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        label = customtkinter.CTkLabel(master=heading_frame, text="Issue Book",
                                       font=customtkinter.CTkFont(family="Robot", size=25, weight="bold"))
        label.pack(ipady=10)

        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)

        book_id_label = customtkinter.CTkLabel(master=main_frame, text="Book ID")
        book_id_label.grid(column=1, row=0, padx=5, pady=5)

        self.book_id_var = customtkinter.StringVar(self)
        self.book_id_input = customtkinter.CTkEntry(master=main_frame, width=200, textvariable=self.book_id_var)
        self.book_id_input.grid(column=2, row=0, padx=5, pady=10)

        student_id_label = customtkinter.CTkLabel(master=main_frame, text="Student ID")
        student_id_label.grid(column=1, row=1, padx=5, pady=5)

        self.student_id_var = customtkinter.StringVar(self)
        self.student_id_input = customtkinter.CTkEntry(master=main_frame, width=200, textvariable=self.student_id_var)
        self.student_id_input.grid(column=2, row=1, padx=5, pady=5)

        issue_book_btn = customtkinter.CTkButton(master=main_frame, text="Issue Book", command=self.issue_book)
        issue_book_btn.grid(column=2, row=2, padx=10, pady=5)

    def issue_book(self):
        book_id = self.book_id_var.get()
        student_id = self.student_id_var.get()

        if book_id and student_id:
            book_id = int(book_id)
            student_id = int(student_id)

            if book_id in self.all_book_id() and student_id in self.all_student_id():
                status = 'available'
                if status in db.select_book_status(book_id):
                    cur_dt = datetime.datetime.now()
                    std_cur_dt = cur_dt.isoformat(' ', 'seconds')
                    data = (
                        book_id,
                        student_id,
                        std_cur_dt,
                        self.expiry_datetime()
                    )

                    res1 = db.issue_book(data)
                    res2 = db.update_book_status(book_id, "issued")

                    if res1 is not None:
                        showinfo(title="Issued", message=f"Book issued successfully to {student_id}")
                    else:
                        showerror(title="Error", message="Something went wrong! Try Again..")
                else:
                    showerror(title="Not Available", message="This book is not available or it is issued to another one.")
            else:
                showerror(title="Not Found",
                          message="Book not found! or Student Not found! Please Check Book ID or Student ID and try again...")
        else:
            showerror(title="Incomplete Information", message="Please enter both Book ID and Student ID.")

    def all_book_id(self):
        return [i[0] for i in db.all_book_id()]

    def all_student_id(self):
        return [i[0] for i in db.all_student_id()]

    def expiry_datetime(self):
        exp_datetime = datetime.datetime.now()
        exp_datetime += datetime.timedelta(days=self.no_expiry_days)
        std_exp_dt = exp_datetime.isoformat(' ', 'seconds')
        return std_exp_dt

# Fetch settings
settings_file_url = "https://raw.githubusercontent.com/lkannan3161/Conestoga-LMS_new/main/config/settings.json"
response = requests.get(settings_file_url)
if response.status_code == 200:
    settings = response.json()
else:
    print("Failed to fetch settings from GitHub. Using default settings.")
    settings = {}  # Define default settings here if needed

# Create LMS database instance
db = LMS("lms.db")

if __name__ == "__main__":
    app = IssueBook(settings=settings)
    app.mainloop()
