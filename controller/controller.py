from model.model import *
from view.tkinter_view import *
from tkinter import filedialog
from view.pop_up import *

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

    def __new__(cls):
        '''
        Enforce singleton pattern
        '''
        if not hasattr(cls, 'instance'):
            cls.instance = super(script_writer_controller, cls).__new__(cls)
        return cls.instance

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

    def set_model_data(self) -> None:
        '''
        Sets the attributes of the model. This must be run before
        model.set_target_files fxn
        :return: @None
        '''
        # reset if using more than once in one instantiation
        self.model.reset_file_model_parameters()

        delimiter_entry_string_var = self.main_window.get_delimiter_entry_stringvar()
        target_dir_entry_string_var = self.main_window.get_target_dir_entry_stringvar()
        target_export_entry_string_var = self.main_window.get_export_path_entry_stringvar()
        row_term_entry_string_var = self.main_window.get_row_terminator_dropdown_stringvar()

        self.model.delimiter = delimiter_entry_string_var.get()
        self.model.target_dir_path = target_dir_entry_string_var.get()
        self.model.export_directory_path = target_export_entry_string_var.get()
        self.model.row_terminator = row_term_entry_string_var.get()

    def generate_error_summary(self,error_tracker: list) -> str:
        '''
        Generates the error summary that is displayed by the status window
        :param error_tracker:  @list a list of errors encountered when running the program
        :return: @str The error summary displayed by the status window
        '''
        total_errors = len(error_tracker)
        error_string_list = []

        for i in range(total_errors):
            file_name = error_tracker[i][0]
            error_message = error_tracker[i][1]
            error_string_list.append(f"Error {i+1} of {total_errors}")
            error_string_list.append(f"File Name: {file_name}")
            error_string_list.append(f"Error: {error_message}")
            error_string_list.append("-" * 70)

        error_string_list.pop()

        return '\n'.join(error_string_list)

    def run_btn_fxn(self):
        '''
        The function to activate when the run button is clicked.
        :return:
        '''
        self.set_model_data()
        self.model.set_target_files()
        error_tracker = []

        pop_up = pop_up_window(pop_up_message='Running Program',pop_up_title='Status Window',
                               master=self.main_window)
        pop_up.update()

        file_counter = 0
        total_files = len(self.model.target_files)

        for each_file in self.model.target_files:
            file_counter += 1
            try:
                pop_up.set_message_title('Program Running...')
                pop_up.set_message(f"Processing file {file_counter} of {total_files}\nFilename: {each_file}")
                pop_up.update()
                self.model.read_one_file(target_file=each_file)
            except Exception as e:
                error_tracker.append([each_file,e.__str__()])
                continue

            self.model.add_script_section()

        self.model.add_variables_and_flags_to_create_tables_script()
        self.model.add_variables_and_flags_to_import_tables_script()
        self.model.generate_create_tables_file()
        self.model.generate_import_tables_file()

        if len(error_tracker) == 0:
            amount_of_files_processed = len(self.model.target_files)
            status_message_title = f"Program Completed\n "
            status_message = f"Succesfully Processed {amount_of_files_processed} of {len(self.model.target_files)} files\n" \
                               f"Scripts generated in directory: {self.model.export_directory_path}"
        else:
            amount_of_files_processed = len(self.model.target_files) - len(error_tracker)
            status_message_title = f"Program Completed With Errors\n "
            status_message = f"Sucessfully Processed {amount_of_files_processed} of {len(self.model.target_files)} files\n" \
                             f"Scripts generated in directory: {self.model.export_directory_path}\n"
            status_message += '\n' + self.generate_error_summary(error_tracker)

        pop_up.set_message_title(status_message_title)
        pop_up.set_message(status_message)
        pop_up.update()

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