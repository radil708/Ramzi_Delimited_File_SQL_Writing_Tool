import tkinter as tk
from tkinter import ttk
import sys
from model.exceptions_and_constants import *

'''
This class acts as the view for Ramzi's Delimited File SQL Writing Tool program.
'''
class main_window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Ramzi's Delimited File SQL Script Writing Tool Version 1.1")
        self.geometry('700x400')
        self.resizable(False, False)
        #self.eval('tk::PlaceWindow . center')
        self.configure(relief='raised')

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates for the window to be centered
        x = (screen_width - 700) // 2
        y = (screen_height - 400) // 2

        # Set the window's position
        self.geometry(f"+{x}+{y}")

        self.protocol("WM_DELETE_WINDOW", sys.exit)

        style = ttk.Style()
        style.configure('Style.TLabel', font=('Courier',20))
        top_label = ttk.Label(master = self, text = image_2, justify='left', style='Style.TLabel') #use ttk to make ASCII art look nicer
        top_label.pack()
        art_by_label = tk.Label(master=self, text = 'ASCII Art by Felix Lee', justify='right',font=('Courier',8))
        art_by_label.place(in_=top_label, relx=0.80,x=25, rely=0.75 )
        self.input_frame_grid = tk.Frame()

        self.row_1_list = self.make_delimiter_section()
        self.row_2_list = self.make_row_terminator_section()
        self.row_3_list = self.make_text_input_frames('Target Directory       ','Browse',2)
        self.row_4_list = self.make_text_input_frames('File Export Directory', 'Browse', 3)


        self.input_frame_grid.pack()

        self.bottom_frame = tk.Frame()
        self.run_button = tk.Button(master=self.bottom_frame, text="   Run   ")
        self.run_button.pack(side=tk.RIGHT, padx=(550, 0), pady=20)
        self.bottom_frame.pack()

        bottom_left_label = tk.Label(master=self, text="Designed, Written, and Developed by Ramzi Reilly Adil")
        bottom_left_label.place(relx=0, rely=1, anchor="sw")

        #set row terminator default
        row_term_stringvar = self.get_row_terminator_dropdown_stringvar()
        row_term_stringvar.set('\\n')

    def __new__(cls):
        '''
        Enforce singleton pattern
        '''
        if not hasattr(cls, 'instance'):
            cls.instance = super(main_window, cls).__new__(cls)
        return cls.instance

    def make_text_input_frames(self, left_side_label: str, button_label: str, row: int):
        '''
        Make the entry, text, and button widgets to place on one row of a grid
        for main window
        :param self:
        :param left_side_label: @str label on the left side
        :param row: @int which row on the grid to place the label on
        :return: @None
        '''
        label = tk.Label(master=self.input_frame_grid, text=left_side_label)
        button = tk.Button(master=self.input_frame_grid, text=button_label)
        string_var = tk.StringVar()
        entry = tk.Entry(master=self.input_frame_grid, width=45, textvariable=string_var)

        label.grid(row=row, column=0, padx=5, pady=5, sticky="e")
        entry.grid(row=row, column=1, padx=5, pady=5)
        button.grid(row=row, column=2, padx=5, pady=5)

        return [label, entry, string_var, button]

    def make_delimiter_section(self):
        '''
        Creates the label and entry widgets for the delimiter section. Also creates the StringVar object
        instance for the delimiter.
        :return: @None
        '''
        label = tk.Label(master=self.input_frame_grid, text='Delimiter', justify='left')
        string_var = tk.StringVar()
        entry = tk.Entry(master=self.input_frame_grid, width=10, justify='center', textvariable=string_var)
        label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry.grid(row=0, column=1, padx=5, pady=5, sticky= "w")
        return [label, entry, string_var]

    def make_row_terminator_section(self):
        '''
        Creates the label, drop down entry and StringVar instance for the row
        terminator.
        :return: @None
        '''
        label = tk.Label(master=self.input_frame_grid, text='Row Terminator', justify='left')
        row_terminator_dropdown_value = tk.StringVar()
        self.row_terminator_options = ["\\n", "0x0A", "\\r", "\\r\\n"]
        row_terminator_dropdown_entry = ttk.Combobox(master=self.input_frame_grid, state="readonly",
                                            values=self.row_terminator_options, width=5,
                                            textvariable=row_terminator_dropdown_value )  # can use get method to get value
        row_terminator_dropdown_value.set("\n")
        label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        row_terminator_dropdown_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        return[label, row_terminator_dropdown_entry, row_terminator_dropdown_value]


    def get_delimiter_entry_widget(self):
        '''
        Shortcut fxn to access the delimiter entry widget.
        :return: @None
        '''
        return self.row_1_list[1]

    def get_delimiter_entry_stringvar(self):
        '''
        Shortcut fxn to access the stringvar instance for the delimiter
        :return: @None
        '''
        return self.row_1_list[2]

    def get_row_terminator_dropdown_widget(self):
        '''
        Shortcut fxn to access the dropdown entry widget for the delimiter
        :return: @None
        '''
        return self.row_2_list[1]

    def get_row_terminator_dropdown_stringvar(self):
        '''
        Shortcut fxn to access the stringvar instance for the row terminator
        :return: @None
        '''
        return self.row_2_list[2]

    def get_target_dir_entry_widget(self):
        '''
        Shortcut fxn to access the entry widget for the target directory
        :return: @None
        '''
        return self.row_3_list[1]

    def get_target_dir_entry_stringvar(self):
        '''
        Shortcut fxn to access the stringvar instance of the target directory
        :return: @None
        '''
        return self.row_3_list[2]

    def get_target_dir_browse_button(self):
        '''
        Shortcut fxn to access the button widget for the target directory
        :return: @None
        '''
        return self.row_3_list[3]

    def get_export_path_entry_widget(self):
        '''
        Shortcut fxn to access the entry widget for the export directory/path
        :return: @None
        '''
        return self.row_4_list[1]

    def get_export_path_entry_stringvar(self):
        '''
        Shortcut fxn to access the stringvar instance for the export directory/path
        :return: @None
        '''
        return self.row_4_list[2]

    def get_export_path_browse_button(self):
        '''
        Shortcut fxn to access the button widget for the export directory/path
        :return: @None
        '''
        return self.row_4_list[3]

    def get_main_window_run_btn(self):
        '''
        Shortcut fxn to access the run button widget from the main window
        :return: @None
        '''
        return self.run_button

# Designed, Written, and Tested By Ramzi Reilly Adil