import customtkinter
import tkinter as tk
from database import LMS
from tkinter.messagebox import showerror, showinfo
import datetime
import requests
import json

db = LMS("lms.db")

settings_web_url= "https://github.com/lkannan3161/Conestoga-LMS_new/blob/main/settings.json"

try:
    # Attempt to fetch settings from the web URL
    response = requests.get(settings_web_url)
    response.raise_for_status()  # Raise an error for bad response status codes
    settings = response.json()
    print("Settings loaded successfully from web.")
except Exception as e:
    print(f"Error fetching settings from web URL: {e}")
    print("Attempting to load settings from local file...")

    # Define the path to your local settings.json file
    settings_file_path = "settings.json"

    try:
        # Attempt to open and read the local settings file
        with open(settings_file_path, "r") as file:
            settings = json.load(file)
        print("Settings loaded successfully from local file.")
    except FileNotFoundError:
        print(f"Settings file '{settings_file_path}' not found. Using default settings.")
        settings = {}
    except json.decoder.JSONDecodeError:
        print(f"Error decoding JSON in '{settings_file_path}'. Using default settings.")
        settings = {}
class IssueBook(tk.Toplevel):
    def __init__(self, master=None, settings=None):
        super().__init__(master)
        self.title("Issue Book")
        self.minsize(400, 250)
        self.maxsize(400, 250)
        self.geometry('300x250')
        self.attributes("-topmost", True)
        self.configure(bg="black")

        self.settings = settings
        self.no_expiry_days = getattr(self.settings, "get", lambda key, default: default)("issue_duration", 30)
        # Default to 30 days if not found

        self.setup_ui()

    def setup_ui(self, bg_color=None):
        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10, bg_color="black", fg_color="black")
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        label = tk.Label(heading_frame, text="Return Book", font=("Robot", 25, "bold"), bg=bg_color, fg=fg_color)
        label.pack(ipady=10)

        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10, bg_color="black", fg_color="black")
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
    settings = {}  # Define default settings here if needed
