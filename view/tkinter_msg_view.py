import tkinter as tk
from tkinter import ttk
from time import sleep

class message_window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Message Box Info")
        self.configure(bg="white",relief='raised')
        self.geometry('250x100')
        #self.resizable(False, False)
        # self.protocol("WM_DELETE_WINDOW", lambda : exit(0))
        self.eval('tk::PlaceWindow . center')
        self.error_list_tracker = []

        self.text_message_text_widget = tk.Label(master=self, text="Program Running Please Wait....", font=('Segoe UI',10),bg='white',justify='left')
        self.text_message_text_widget.place(relx=.5, rely=.5, anchor="center")

    def set_text_to_complete(self):
        if self.error_list_tracker == []:
            self.text_message_text_widget.config(text='Program Completed')
        else:
            self.error_list_tracker.insert(0,'Program Completed With Errors:\n')
            final_text = ''.join(self.error_list_tracker)
            self.text_message_text_widget.config(text=final_text)



