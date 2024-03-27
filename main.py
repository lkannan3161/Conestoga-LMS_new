import tkinter
import tkinter as tk
from tkinter import filedialog
from tkinter.constants import RIGHT

from AddBook import *
from BookReport import *
from DeleteBook import *
from EditBook import *
from IssueBook import *
from ReturnBook import *
from ViewBooks import *
from tkinter import messagebox

# Define the LMSApp class
class LMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.state('zoomed')
        self.geometry('1920x1080')
        self.configure(bg="black")

        # Logo label
        self.logo_image = tk.PhotoImage(file="Logo.png")
        self.logo_image = self.logo_image.subsample(2)
        self.logo_label = tk.Label(self, image=self.logo_image, bg="black")
        self.logo_label.pack(pady=20)

        # Header Frame
        heading_frame = tk.Frame(master=self, bg="black")
        heading_frame.pack(padx=1, pady=1, ipadx=5, ipady=2, fill="x", anchor="n")
        label = tk.Label(master=heading_frame, text="Library Management System", font=("Robot", 25, "bold"), bg="black", fg="white")
        label.pack(ipady=10)

        # Main Frame
        main_frame = tk.Frame(master=self, bg="black")
        main_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True)

        # Left Frame
        left_frame = tk.Frame(master=main_frame, bg="black")
        left_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True, side="left")

        # Right Frame
        right_frame = tk.Frame(master=main_frame, bg="black")
        right_frame.pack(padx=10, pady=10, ipadx=5, ipady=5, fill="both", expand=True, side="right")

        # Buttons
        button_texts = ["Add new Book", "Book List", "Edit Book", "Delete Book", "Issue Book", "Return Book", "Report", "Import Student"]
        button_commands = [self.add_book_win, self.view_book_win, self.edit_book_win, self.delete_book_win,  self.issue_book_win, self.return_book_win, self.book_report_win, self.import_student]

        for i in range(len(button_texts)):
            button = tk.Button(master=left_frame if i < len(button_texts)//2 else right_frame,
                               text=button_texts[i], command=button_commands[i],
                               bg="white", fg="black", padx=20, pady=10)
            button.pack(fill="x", pady=10)

        # Exit Button
        exit_button = tk.Button(master=right_frame, text="Exit", padx=20, pady=10, bg="chartreuse3", font=("Roboto", 16, "bold"),
                                command=self.exit_screen)
        exit_button.pack(side="right", pady=1)

        # Footer Frame
        footer_frame = tk.Frame(master=self, bg="black")
        footer_frame.pack(fill="x", pady=5)
        dev_by_label = tk.Label(master=footer_frame, text="@Copyrights reserved April 2024", bg="black", fg="white")
        dev_by_label.pack()

    # Methods to open windows
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

    def exit_screen(self):
        self.destroy()

    def import_student(self):
        try:
            filetypes = (('excel files', '*.xlsx'),)
            file = filedialog.askopenfilename(title="Import Students", filetypes=filetypes)
            res = db.add_new_student(file)
            if res is not None:
                showinfo(title="Success", message="Students imported successfully")
            else:
                showerror(title="Error", message="Something went wrong. Try Again!")
        except Exception as e:
            showerror(title="Error", message=f"An error occurred: {e}")

# Main function to start the application
if __name__ == '__main__':
    # Create the login screen
    login_window = tk.Tk()
    login_window.title("Login")
    login_window.configure(bg='black')
    login_window.state('zoomed')
    login_window.geometry('1920x1080')

    # Define login function
    def login():
        usernameList = ["admin", "student"]
        passwordList = ["admin", "student"]

        if username_entry.get() in usernameList:
            indexUser = usernameList.index(username_entry.get())
            if password_entry.get() == passwordList[indexUser]:
                login_window.destroy()
                app = LMSApp()
                app.mainloop()
            else:
                messagebox.showerror(title="Error", message="Invalid password.")
        else:
            messagebox.showerror(title="Error", message="Invalid username.")

        # Cancel button function
    def cancel_login():
            login_window.destroy()
    # Logo label
    logo_image = tk.PhotoImage(file="Logo.png")
    logo_image = logo_image.subsample(2)
    logo_label = tk.Label(login_window, image=logo_image, bg="black")
    logo_label.pack(pady=30)

    # Username label and entry
    username_frame = tk.Frame(login_window, bg='#000000')
    username_frame.pack(pady=10)
    username_label = tk.Label(username_frame, text="Username  ", bg='#000000', fg="white", font=("Roboto", 16, 'bold'))
    username_label.pack(side="left")
    username_entry = tk.Entry(username_frame, font=("Roboto", 16))
    username_entry.pack(side="left")

    # Password label and entry
    password_frame = tk.Frame(login_window, bg='#000000')
    password_frame.pack(pady=10)
    password_label = tk.Label(password_frame, text="Password  ", bg='#000000', fg="white", font=("Roboto", 16, 'bold'))
    password_label.pack(side="left")
    password_entry = tk.Entry(password_frame, show="*", font=("Roboto", 16))
    password_entry.pack(side="left")

    # Create a frame for the buttons
    button_frame = tk.Frame(login_window, bg="black")
    button_frame.pack(pady=30)

    # Login button
    login_button = tk.Button(button_frame, text="Login", font=("Roboto", 16, "bold"), command=login, bg="white",
                             fg="black")
    login_button.pack(side="left", padx=(50, 10))  # Adjust padx here

    # Cancel button
    cancel_button = tk.Button(button_frame, text="Cancel", font=("Roboto", 16, "bold"), command=cancel_login,
                              bg="white",
                              fg="black")
    cancel_button.pack(side="left", padx=(10, 10))  # Adjust padx here

    # Start the login window
    login_window.mainloop()
