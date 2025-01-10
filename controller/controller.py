from model.model import *
from view.tkinter_view import *
from tkinter import filedialog
from view.tkinter_msg_view import *

'''
This class acts as the controller for Ramzi's Delimited File SQL Writing Tool program.
'''
class script_writer_controller():
    def __init__(self):
        self.model = script_writer_model()
        self.main_window = main_window()

        #assign button fxns
        self.assign_main_window_button_functions()

        self.msg_window = None

    def fix_dir_strings(self,filepath_in:str) -> str:
        """
        Helper function to make the path correct by replace '/' with '\'
        :param filepath_in: @str filepath to a directory
        :return: @str filepath where '/' is replaced by '\'
        """
        filepath = filepath_in
        return filepath.replace('/','\\')
    def target_dir_btn_fxn(self):
        """
        The function to activate when user clicks the target directory path browse button
        :return: @None
        """
        directory = filedialog.askdirectory()
        directory = self.fix_dir_strings(directory)
        self.model.target_dir_path = directory
        target_dir_entry_string_var = self.main_window.get_target_dir_entry_stringvar()
        target_dir_entry_string_var.set(directory)

    def export_dir_btn_fxn(self):
        """
        The function to activate when the user clicks the export directory path browse button
        :return: @NOne
        """
        directory = filedialog.askdirectory()
        directory = self.fix_dir_strings(directory)
        self.model.export_directory_path = directory
        target_export_entry_string_var = self.main_window.get_export_path_entry_stringvar()
        target_export_entry_string_var.set(directory)

    def run_btn_fxn(self):
        #reset if using more than once in one instantiation
        self.model.reset_file_model_parameters()

        delimiter_entry_string_var = self.main_window.get_delimiter_entry_stringvar()
        target_dir_entry_string_var = self.main_window.get_target_dir_entry_stringvar()
        target_export_entry_string_var = self.main_window.get_export_path_entry_stringvar()
        row_term_entry_string_var = self.main_window.get_row_terminator_dropdown_stringvar()

        #TODO no checks if values are empty want that
        self.model.delimiter = delimiter_entry_string_var.get()
        self.model.target_dir_path = target_dir_entry_string_var.get()
        self.model.export_directory_path = target_export_entry_string_var.get()
        self.model.row_terminator = row_term_entry_string_var.get()

        #so only one message window exists at a time
        #TODO make this better should not rely on setting variable to None line 84
        if self.msg_window != None:
            self.msg_window.destroy()
        else:
            self.msg_window = message_window()

        self.msg_window.update() #need this because label update won't update quick enough otherwise

        self.model.run()

        if self.model.error_tracker != []:
            self.msg_window.error_list_tracker.extend(self.model.error_tracker)

        self.msg_window.set_text_to_complete()

        #temp fix
        self.msg_window = None

    def assign_main_window_button_functions(self):
        """
        Assigning the functions to the buttons from the tkinter main window
        :return:
        """
        target_dir_btn = self.main_window.get_target_dir_browse_button()
        target_dir_btn.configure(command=self.target_dir_btn_fxn)

        export_dir_btn = self.main_window.get_export_path_browse_button()
        export_dir_btn.configure(command = self.export_dir_btn_fxn)

        run_btn = self.main_window.get_main_window_run_btn()
        run_btn.configure(command=self.run_btn_fxn)

# Designed, Written, and Tested By Ramzi Reilly Adil