import tkinter as tk
from tkinter import ttk
import sys

textample = '''
 ____                     _ _       ____   ___  _ 
|  _ \ __ _ _ __ ___  ___(_| )___  / ___| / _ \| | 
| |_) / _` | '_ ` _ \|_  / |// __| \___ \| | | | | 
|  _ < (_| | | | | | |/ /| | \__ \  ___) | |_| | |___ 
|_| \_\__,_|_| |_|_|_/___|_| |___/ |____/_\__\_\_____|
'''

textample_2 = '''
 ____                     _ _       ____   ___  _                           
|  _ \ __ _ _ __ ___  ___(_| )___  / ___| / _ \| |                          
| |_) / _` | '_ ` _ \|_  / |// __| \___ \| | | | |                          
|  _ < (_| | | | | | |/ /| | \__ \  ___) | |_| | |___                       
|_| \_\__,_|_| |_| |_/___|_| |___/ |____/ \__\_\_____|    _____           _ 
                    \ \      / / __(_) |_(_)_ __   __ _  |_   _|__   ___ | |
                     \ \ /\ / / '__| | __| | '_ \ / _` |   | |/ _ \ / _ \| |
                      \ V  V /| |  | | |_| | | | | (_| |   | | (_) | (_) | |
                       \_/\_/ |_|  |_|\__|_|_| |_|\__, |   |_|\___/ \___/|_|
                                                  |___/                     
'''

textample_3 = '''
      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)  
'''

class main_window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Ramzi's Delimited File SQL Script Writing Tool Version 1.0")
        self.geometry('700x375')
        self.resizable(False, False)
        # self.protocol("WM_DELETE_WINDOW", lambda : exit(0))
        self.eval('tk::PlaceWindow . center')
        self.configure(relief='raised')
        self.protocol("WM_DELETE_WINDOW", sys.exit)

        style = ttk.Style()
        #style.configure('Style.TLabel', font='TkFixedFont')
        style.configure('Style.TLabel', font=('Courier',20))
        top_label = ttk.Label(master = self, text = textample_3, justify='left', style='Style.TLabel') # use ttk to make ASCII art look nicer
        top_label.pack()
        art_by_label = tk.Label(master=self, text = 'ASCII Art by Felix Lee', justify='right',font=('Courier',8))
        art_by_label.place(in_=top_label, relx=0.80,x=25, rely=0.75 )
        self.input_frame_grid = tk.Frame()

        self.row_1_list = self.make_delimiter_section()
        self.row_2_list = self.make_text_input_frames('Target Directory       ','Browse',1)
        self.row_3_list = self.make_text_input_frames('File Export Directory', 'Browse', 2)


        self.input_frame_grid.pack()

        self.bottom_frame = tk.Frame()
        self.run_button = tk.Button(master=self.bottom_frame, text="   Run   ")
        self.run_button.pack(side=tk.RIGHT, padx=(550, 0), pady=20)
        self.bottom_frame.pack()

        bottom_left_label = tk.Label(master=self, text="Designed, Written, and Developed by Ramzi Reilly Adil")
        bottom_left_label.place(relx=0, rely=1, anchor="sw")

        '''
        self.upper_user_frame = tk.Frame(master=self)
        self.upper_user_frame.pack(fill="both", expand=1)
        self.current_user = ""
        self.user_label = tk.Label(master=self.upper_user_frame, text="Current Account: ")
        self.user_label.pack(side=tk.RIGHT, padx=15, pady=(5, 0))
        '''

    def make_text_input_frames(self, left_side_label: str, button_label: str, row: int):
        '''
        Make the entry, text, and button widgets to place on one row of a grid
        for main window
        :param self:
        :param left_side_label: @str label on the left side
        :param row: @int which row on the grid to place the label on
        :return:
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
        label = tk.Label(master=self.input_frame_grid, text='Delimiter', justify='left')
        string_var = tk.StringVar()
        entry = tk.Entry(master=self.input_frame_grid, width=10, justify='center', textvariable=string_var)
        label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry.grid(row=0, column=1, padx=5, pady=5, sticky= "w")
        return [label, entry, string_var]

    def get_delimiter_entry_widget(self):
        return self.row_1_list[1]

    def get_delimiter_entry_stringvar(self):
        return self.row_1_list[2]

    def get_target_dir_entry_widget(self):
        return self.row_2_list[1]

    def get_target_dir_entry_stringvar(self):
        return self.row_2_list[2]
    def get_target_dir_browse_button(self):
        return self.row_2_list[3]

    def get_export_path_entry_widget(self):
        return self.row_3_list[1]

    def get_export_path_entry_stringvar(self):
        return self.row_3_list[2]

    def get_export_path_browse_button(self):
        return self.row_3_list[3]

    def get_main_window_run_btn(self):
        return self.run_button
