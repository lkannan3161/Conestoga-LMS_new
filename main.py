import tkinter as tk
import customtkinter
import requests

from AddBook import *
from EditBook import *
from DeleteBook import *
from ViewBooks import *
from IssueBook import *
from ReturnBook import *
from BookReport import *
import os
import sys
from tkinter import filedialog, messagebox

class LMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry('800x600')
        self.configure(bg="black")  # Set background color to black

        def download_image(url, file_path):
            response = requests.get(url)
            with open(file_path, 'wb') as file:
                file.write(response.content)

        # Example usage
        url = 'https://raw.githubusercontent.com/lkannan3161/Conestoga-LMS_new/main/Logo.png'
        local_file_path = 'Logo.png'  # Specify the local file path where you want to save the image
        download_image(url, local_file_path)
        # Logo label
        self.logo_image = tk.PhotoImage(file=local_file_path)
        self.logo_image = self.logo_image.subsample(2)  # Adjust logo size
        self.logo_label = tk.Label(self, image=self.logo_image, bg="black")
        self.logo_label.pack(pady=20)

        heading_frame = tk.Frame(master=self, bg="black")
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        label = tk.Label(master=heading_frame, text="Library Management System",
                         font=("Robot", 25, "bold"), bg="black", fg="white")
        label.pack(ipady=10)

        main_frame = tk.Frame(master=self, bg="black")
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        left_frame = tk.Frame(master=main_frame, bg="black")
        left_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True, side="left")

        right_frame = tk.Frame(master=main_frame, bg="black")
        right_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True, side="right")

        button_1 = tk.Button(master=left_frame, text="Add new Book",
                             command=self.add_book_win, bg="white", fg="black", padx=20, pady=10)
        button_1.pack(fill="x", pady=10)

        button_2 = tk.Button(master=left_frame, text="Delete Book",
                             command=self.delete_book_win, bg="white", fg="black", padx=20, pady=10)
        button_2.pack(fill="x", pady=10)

        button_3 = tk.Button(master=left_frame, text="Book List",
                             command=self.view_book_win, bg="white", fg="black", padx=20, pady=10)
        button_3.pack(fill="x", pady=10)

        button_4 = tk.Button(master=right_frame, text="Issue Book",
                             command=self.issue_book_win, bg="white", fg="black", padx=20, pady=10)
        button_4.pack(fill="x", pady=10)

        button_5 = tk.Button(master=right_frame, text="Return Book",
                             command=self.return_book_win, bg="white", fg="black", padx=20, pady=10)
        button_5.pack(fill="x", pady=10)

        button_6 = tk.Button(master=right_frame, text="Report",
                             command=self.book_report_win, bg="white", fg="black", padx=20, pady=10)
        button_6.pack(fill="x", pady=10)

        button_7 = tk.Button(master=left_frame, text="Edit Book",
                             command=self.edit_book_win, bg="white", fg="black", padx=20, pady=10)
        button_7.pack(fill="x", pady=10)

        button_8 = tk.Button(master=right_frame, text="Import Student",
                             command=self.import_student, bg="white", fg="black", padx=20, pady=10)
        button_8.pack(fill="x", pady=10)

        footer_frame = tk.Frame(master=self, bg="black")
        footer_frame.pack(fill="x", pady=10)

        dev_by_label = tk.Label(master=footer_frame, text="@Copyrights reserved April 2024", bg="black", fg="white")
        dev_by_label.pack()

       # watermark = tk.Label(master=self, text="Conestoga LMS")
       # watermark.place(relx=0.7, rely=0.9, anchor='sw')
    def add_book_win(self):
        app = AddBook(self)
        app.focus()

    def edit_book_win(self):
        app = EditBook(self)
        app.focus()

    def delete_book_win(self):
        app = DeleteBook(self)
        app.focus()

    def view_book_win(self):
        app = ViewBooks(self)
        app.focus()

    def issue_book_win(self):
        app = IssueBook(self)
        app.focus()

    def return_book_win(self):
        app = ReturnBook(self)
        app.focus()

    def book_report_win(self):
        app = BookReport(self)
        app.focus()

    def import_student(self):
        try:
            filetypes = (
                ('exel files', '*.xlsx'),
            )
            file = filedialog.askopenfilename(title="Import Students", filetypes=filetypes)
            res = db.add_new_student(file)
            if res != None:
                showinfo(title="Success", message="Students imported successfully")
            else:
                showerror(title="Error", message="Something went wrong. Try Again!")
        except:
            showerror(title="Error", message="File is not in correct form or file not selected")


if __name__ == '__main__':
    app = LMSApp()
    app.mainloop()