import os
from model.exceptions_and_constants import *

'''
This class acts as the model for Ramzi's Delimited File SQL Writing Tool program.
'''
class script_writer_model():
    def __init__(self):
        self.file_number_counter = 1
        self.target_dir_path = ''
        self.export_directory_path = ''
        self.delimiter = ''
        self.whole_create_script_content_list = []
        self.whole_bulk_insert_content_list = []
        self.error_tracker = []
        self.skip_file = []
        self.row_terminator = None
        self.target_files = []

        #used in loop to catch errors
        self.current_create_script_section = None
        self.current_import_script_section = None

    def __new__(cls):
        '''
        Enforce singleton pattern
        '''
        if not hasattr(cls, 'instance'):
            cls.instance = super(script_writer_model, cls).__new__(cls)
        return cls.instance


    def reset_file_model_parameters(self):
        '''
        Clears out model data
        :return: @None
        '''
        self.file_number_counter = 1
        self.target_dir_path = ''
        self.export_directory_path = ''
        self.delimiter = ''
        self.whole_create_script_content_list = []
        self.whole_bulk_insert_content_list = []
        self.error_tracker = []
        self.skip_file = []
        self.row_terminator = None
        self.target_files = []
        self.current_create_script_section = None
        self.current_import_script_section = None

    def is_delimiter_empty(self) -> None:
        '''
		Used to check if user entry for delimiter has been set.
		raises an error if not.
		:return: @None
		'''
        if self.delimiter == '':
            raise CustomExceptionMissingEntry('DELIMITER')
        else:
            return

    def is_target_dir_empty(self) -> None:
        '''
		Used to check if user entry for target directory has been set.
		raises an error if not.
		:return: @None
		'''
        if self.target_dir_path == '':
            raise CustomExceptionMissingEntry('Target Directory')
        else:
            return

    def is_export_dir_empty(self) -> None:
        '''
		Used to check if user entry for export directory has been set.
		raises an error if not.
		:return: @None
		'''
        if self.export_directory_path == '':
            raise CustomExceptionMissingEntry('File Export Directory')
        else:
            return

    def does_target_dir_have_files(self) -> None:
        '''
        Used to check if there are files in target directory
        :return: @None
        '''
        if len(self.target_files) == 0:
            raise CustomExceptionNoFilesFound(self.target_dir_path)
        else:
            return

    def is_valid_target_dir_path(self) -> None:
        '''
        Used to check if target directory path is valid
        :return: @None
        '''
        if not os.path.exists(self.target_dir_path):
            raise CustomExceptionInvalidDirectoryPath(self.target_dir_path,'target directory')
        else:
            return

    def is_valid_target_export_path(self) -> None:
        '''
        Used to check if export directory path is valid
        :return: @None
        '''
        if not os.path.exists(self.export_directory_path):
            raise CustomExceptionInvalidDirectoryPath(self.export_directory_path,'export directory')
        else:
            return

    def check_for_valid_paths(self) -> None:
        '''
        Checks if user defined paths are valid
        :return: @none
        '''
        self.is_valid_target_dir_path()
        self.is_valid_target_export_path()

    def check_user_defined_attributes(self) -> None:
        '''
		Checks all user defined entries. Raises an error if any are
		encountered.
		:return: @None
		'''
        self.is_delimiter_empty()
        self.is_target_dir_empty()
        self.is_export_dir_empty()

    def get_all_filenames(self,target_directory: str) -> list:
        '''
        Get all filenames from a specific directory
        :param target_directory: @str filepath to target directory
        :return: @list list of files from the target directory
        '''
        return os.listdir(target_directory)
    
    def make_create_tables_fields(self,filepath_in: str, delimiter_in: str) -> str:
        '''
        Helper func to make_create_tables_scripts
        :param filepath_in: @str path to the file to look at
        :param delimiter_in: @str delimiter the splits the fields from target files
        :return: @str the fields section of a create table specific to the filepath_in
        '''
        temp = []
        empty_field_counter = 1 #used to keep count of how many empty fields there are if any
        file_name = filepath_in.split('\\').pop()

        try:
            #read the header from the file and store the fields
            with open(filepath_in, 'r') as filereader:
                headers_line = filereader.readline()
                all_fields_unformatted = headers_line.split(delimiter_in)

                for i in range(len(all_fields_unformatted)):
                    field = all_fields_unformatted[i].replace(' ', '_') #replacing space char with underscore
                    field = field.replace('\n','') #for last field remove newline char
                    field = field.replace('\"','') #remove quotes in field names

                    for char in NON_VALID_CHARS_FIELD_NAME:
                        field = field.replace(char,'') #replace any non_valid field chars

                    if field in WHITE_SPACE_CHAR_LIST or field == '': #column'fields with no name
                        field = f'NO_FIELD_NAME_{str(empty_field_counter)}'
                        empty_field_counter += 1

                    if i == len(all_fields_unformatted) - 1:
                        temp.append(f'\t\t[{field}] varchar(max)\n')
                    else:
                        temp.append(f'\t\t[{field}] varchar(max),\n')
        except UnicodeDecodeError:
            raise CustomExceptionInvalidFile(file_name)
    
        return ''.join(temp)
    
    def make_create_tables_script(self,filepath_in: str,delimiter_in: str) -> str:
        """
        Stores the sections of the create table script that will eventually
        get written into one create table file
        :param filepath_in: @str path to the file to look at
        :return: @None
        """
        insert_list = []
    
        file_name = filepath_in.split('\\').pop()

        # get file name no extension. Did it this way in case extension uses multiple periods
        file_name_list = file_name.split('.')
        file_name_no_extension = file_name_list.pop(0)

        table_name = file_name_no_extension
        table_name = table_name.replace(' ','_') #remove space char in table name so don't have to use brackets when calling table name
    
        for invalid_char in NON_VALID_CHARS_TABLE_NAME:
            table_name = table_name.replace(invalid_char,'')
    
        if table_name.upper() in RESERVED_KEYWORDS: #raise error if table name is a keyword in sql
            raise CustomExceptionInvalidTableName(table_name, file_name)
    
        #generate the create script per file
        ct_drop = f'IF OBJECT_ID (\'{table_name}\', \'U\') IS NOT NULL\n\tDROP TABLE dbo.{table_name};\n\n'
        fields_as_string = self.make_create_tables_fields(filepath_in,delimiter_in)
        ct_create = f'CREATE TABLE {table_name}\n\t(\n' + fields_as_string + '\t)\n\n' + '--' + ('='*50) + '\n'
        insert_list.append(ct_drop)
        insert_list.append(ct_create)

        return ''.join(insert_list)

    
    def wrap_in_try_catch(self,input: str, table_name_in: str,filename: str) -> str:
        """
        Used in the generation of the insert scripts by wrapping them in a try catch
        :param input: @str the insert that goes in between the try catch
        :param table_name_in: @str the tablename
        :param filename: @str the filename we are making the table from
        :return: @str the whole insert script section per table
        """

        zero = f'DECLARE @command{self.file_number_counter} varchar(max) ='
        first = '\'BEGIN TRY\n' + input + '\nEND TRY\n'
        second = f'BEGIN CATCH\n\tPRINT \'\'Failed to insert data from {filename} into [dbo].[{table_name_in}]\'\''
        third = f'\n\tDECLARE @err_msg{self.file_number_counter} AS varchar(MAX)'
        fourth = f'\n\tSET @err_msg{self.file_number_counter} = ERROR_MESSAGE()'
        fifth = f'\n\tPRINT @err_msg{self.file_number_counter} \n' + 'END CATCH\'\n'
        sixth = f'exec(@command{self.file_number_counter})'
        return zero + first + second + third + fourth + fifth + sixth
    
    def make_insert_script(self, filepath_in: str, delimiter_in: str) -> str:
        """
        Generates the insert script sections
        :param filepath_in: @str path to the file to read
        :param delimiter_in: @str the delimiter for the file
        :return: @None
        """
        file_name = filepath_in.split('\\').pop()

        #get file name no extension. Did it this way in case extension uses multiple periods
        file_name_list = file_name.split('.')
        file_name_no_extension = file_name_list.pop(0)

        #get extension
        extension = '.'.join(file_name_no_extension)

        table_name = file_name_no_extension # this is full name including the dot
        table_name = table_name.replace(' ',
                                        '_')  # remove space char in table name so don't have to use brackets
                                                    # when calling table name
    
        for invalid_char in NON_VALID_CHARS_TABLE_NAME: # Remove invalid characters for table names
            table_name = table_name.replace(invalid_char, '')
    
        if table_name.upper() in RESERVED_KEYWORDS: #raise error if table name is a keyword in sql
            raise CustomExceptionInvalidTableName(table_name, file_name)
    
        if delimiter_in in REP_DICT.keys():
            delim = REP_DICT[delimiter_in] #replace delimiter with delimiter to write in script if needed
        else:
            delim = delimiter_in
    
        trunc_cmd = f'\nIF OBJECT_ID (\'{table_name}\', \'U\') IS NOT NULL\n\tTRUNCATE TABLE dbo.{table_name};\n\n'
    
        self.whole_bulk_insert_content_list.append(trunc_cmd)

        file_ins = 'file' + str(self.file_number_counter)
        s0 = f'\nDECLARE @{file_ins} varchar(max) = \'{file_name}\'\n'
        s0 += f'SET @{file_ins} = CONVERT(nvarchar(max), @data_src + \'\\\' + @{file_ins})\n'
        self.whole_bulk_insert_content_list.append(s0)
        s1 = f'BULK INSERT [dbo].[{table_name}] '
        s2 = f'FROM \'\'\' + @{file_ins} + \'\'\' WITH\n'
        s3 = f'\t(\n\tFIELDTERMINATOR = \'\'{delim}\'\',\n\tROWTERMINATOR = \'\'{self.row_terminator}\'\'\n\t)'

    
        # files will always have headers so no need for if statement
        s3 = s3.lstrip('\t(')
        s3 = f'\t(\n\tFIRSTROW = 2,' + s3
    
        temp = [s1,s2,s3]
    
        if extension.lower() == 'csv':
            s3 = temp.pop()
            s3 = s3.rstrip('\n\t)')
            s3 = s3 + ",\n\tFORMAT = ''CSV''\n\t)"
            temp.append(s3)
    
        t_str = ''.join(temp)
        t_str = self.wrap_in_try_catch(t_str,table_name,filepath_in.split('\\').pop())
        t_str += '\n--' + ('=' * 50)

        return t_str

    def set_target_files(self) -> None:
        '''
        Sets the target_files attribute. Also fixes the delimiter attribute
        if "tab" is the user input for delimiter.
        :return: @None
        '''

        self.target_files.extend(self.get_all_filenames(self.target_dir_path))

        if self.delimiter.lower().strip() == "tab": #for tab delimited
            self.delimiter = '\t'

    def read_one_file(self, target_file: str) -> None:
        '''
        Reads a file, and sets the current_create_script_section attribute as well as the
        current_import_script_section_attribute
        :param target_file: @str filepath to the file to read
        :return: @None
        '''
        filepath = self.target_dir_path + '\\' + target_file
        self.current_create_script_section = self.make_create_tables_script(filepath, self.delimiter)
        self.current_import_script_section = self.make_insert_script(target_file, self.delimiter)

    def add_script_section(self) -> None:
        '''
        Adds a section to the create and import sql scripts.
        Only call after the read_one_file fxn has been called.
        :return: @None
        '''
        self.whole_create_script_content_list.append(self.current_create_script_section)
        self.whole_bulk_insert_content_list.append(self.current_import_script_section)

        self.current_create_script_section = None
        self.current_import_script_section = None

    def add_variables_and_flags_to_create_tables_script(self) -> None:
        '''
        Adds extra variables or flags to the generated create tables sql scripts
        :return: @None
        '''
        self.whole_create_script_content_list.insert(0,'IF \'<<LoadSourceDataFlagYN>>\' = \'Y\'\nBEGIN\n\n')
        self.whole_create_script_content_list.insert(0,'use <<ConversionDatabase>>\n\n')
        self.whole_create_script_content_list.append('\nEND')

    def add_variables_and_flags_to_import_tables_script(self) -> None:
        '''
        Adds extra variables or flags to the generated import data tables sql scripts
        :return: @None
        '''
        self.whole_bulk_insert_content_list.insert(0,'IF \'<<LoadSourceDataFlagYN>>\' = \'Y\'\nBEGIN\n\n')
        self.whole_bulk_insert_content_list.insert(0, 'DECLARE @data_src VARCHAR(max) = \'<<SourceDataLoadPath>>\'\n\n')
        self.whole_bulk_insert_content_list.insert(0,'use <<ConversionDatabase>>\n\n')

        self.whole_bulk_insert_content_list.append('\nEND')

    def generate_create_tables_file(self):
        '''
        Export the data into the create tables sql script
        :return:
        '''
        create_table_export_full_path = self.export_directory_path + '\\' + 'CreateSourceTables.sql'

        with open(create_table_export_full_path, 'w') as create_writer:
            create_writer.write(''.join(self.whole_create_script_content_list))

    def generate_import_tables_file(self):
        '''
        Export the data into the import tables sql script
        :return:
        '''
        import_data_export_full_path = self.export_directory_path + '\\' + 'ImportData.sql'

        with open(import_data_export_full_path, 'w') as import_writer:
            import_writer.write(''.join(self.whole_bulk_insert_content_list))

# Designed, Written, and Tested By Ramzi Reilly Adil




