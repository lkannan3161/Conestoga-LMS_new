import tkinter
import customtkinter
from AddBook import *
from EditBook import *
from DeleteBook import *
from ViewBooks import *
from IssueBook import *
from ReturnBook import *
from BookReport import *
import os
import sys
settings_file_path = "/Users/layak/PycharmProjects/Conestoga-LMS/config/settings.json"
with open(settings_file_path, "r") as settings_file:
    settings = json.load(settings_file)

customtkinter.set_appearance_mode(settings["theme"])
customtkinter.set_default_color_theme(settings["color_theme"])


class LMSApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.minsize(600, 430)
        self.maxsize(600, 430)
        self.geometry('600x430')

        heading_frame = customtkinter.CTkFrame(master=self, corner_radius=10)
        heading_frame.pack(padx=10, pady=10, ipadx=20, ipady=5, fill="x", anchor="n")

        label = customtkinter.CTkLabel(master=heading_frame, text="Library Management System",
                                       font=customtkinter.CTkFont(family="Robot", size=25, weight="bold"))
        label.pack(ipady=10)

        main_frame = customtkinter.CTkFrame(master=self, corner_radius=10, fg_color='transparent')
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        left_frame = customtkinter.CTkFrame(master=main_frame, corner_radius=10)
        left_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True, side="left")

        right_frame = customtkinter.CTkFrame(master=main_frame, corner_radius=10)
        right_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True, side="right")

        button_1 = customtkinter.CTkButton(master=left_frame, text="Add new Book", corner_radius=3,
                                           command=self.add_book_win)
        button_1.pack(padx=20, pady=10)

        button_2 = customtkinter.CTkButton(master=left_frame, text="Delete Book", corner_radius=3,
                                           command=self.delete_book_win)
        button_2.pack(padx=20, pady=10)

        button_3 = customtkinter.CTkButton(master=left_frame, text="Book List", corner_radius=3,
                                           command=self.view_book_win)
        button_3.pack(padx=20, pady=10)

        button_4 = customtkinter.CTkButton(master=right_frame, text="Issue Book", corner_radius=3,
                                           command=self.issue_book_win)
        button_4.pack(padx=20, pady=10)

        button_5 = customtkinter.CTkButton(master=right_frame, text="Return Book", corner_radius=3,
                                           command=self.return_book_win)
        button_5.pack(padx=20, pady=10)

        button_6 = customtkinter.CTkButton(master=right_frame, text="Report", corner_radius=3,
                                           command=self.book_report_win)
        button_6.pack(padx=20, pady=10)

        button_7 = customtkinter.CTkButton(master=left_frame, text="Edit Book", corner_radius=3,
                                           command=self.edit_book_win)
        button_7.pack(padx=20, pady=10)

        button_8 = customtkinter.CTkButton(master=right_frame, text="Import Student", corner_radius=3,
                                           command=self.import_student)
        button_8.pack(padx=20, pady=10)

        footer_frame = customtkinter.CTkFrame(master=self, corner_radius=8, fg_color="#f55d5d")
        footer_frame.pack(padx=20, pady=10, fill="x", anchor="s")
        dev_by_label = customtkinter.CTkLabel(master=footer_frame, text=settings["footer_txt"], bg_color="#f55d5d")
        dev_by_label.pack()

        watermark = customtkinter.CTkLabel(master=self, text="Conestoga LMS")
        watermark.place(relx=0.7, rely=0.9, anchor='sw')

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
