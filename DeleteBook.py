import customtkinter
import tkinter as tk
from database import LMS
from tkinter.messagebox import showerror, showinfo
import os
import sys

db = LMS("lms.db")

class DeleteBook(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Delete Book")
        self.configure(bg="black")
        self.minsize(400,250)
        self.maxsize(400,250)
        self.geometry('400x250')
        self.attributes("-topmost", True)
        
        heading_frame = customtkinter.CTkFrame(master=self,corner_radius=10, bg_color="black", fg_color="black")
        heading_frame.pack(padx=10,pady=10, ipadx=20, ipady=5,fill="x",anchor="n")
        
        label = customtkinter.CTkLabel(master=heading_frame, text="Delete Book",font=customtkinter.CTkFont(family="Robot",size=25, weight="bold"), bg_color="black", fg_color="black")
        label.pack(ipady=10)
        
        main_frame = customtkinter.CTkFrame(master=self,corner_radius=10, bg_color="black", fg_color="black")
        main_frame.pack(padx=10,pady=10, ipadx=5, ipady=5,fill="both",expand=True)
        
        book_id_lbel = customtkinter.CTkLabel(master=main_frame,text="Book ID", font=customtkinter.CTkFont(family="Verdana",size=18))
        book_id_lbel.pack()
        
        self.book_id_input = customtkinter.CTkEntry(master=main_frame, width=200)
        self.book_id_input.pack(padx=5, pady=10)
        
        delete_book_btn = tk.Button(master=main_frame,text="Delete Book", font=("Verdana", 16, "bold"), command=self.delete_book)
        delete_book_btn.pack(padx=10,pady=10)
    
    def delete_book(self):

        if self.book_id_input.get().isdigit():
            id_lists = db.all_book_id()
            new_id_lists = [t[0] for t in id_lists]
            if int(self.book_id_input.get()) in new_id_lists:
                res = db.delete_book(self.book_id_input.get())
                if res == 'deleted':
                    showinfo(title="Deleted",message=f"Book ID : {self.book_id_input.get()}, deleted successfully.")
                    self.book_id_input.delete(0,'end')
                else:
                    showerror(title="Error",message=f"Book ID : {self.book_id_input.get()}, not deleted. Try Again!")
            else:
                showerror(title="Not Found",message="Book not found")

        else:
            showerror(title="Book ID", message="Please enter a correct Book ID")