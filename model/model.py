'''
The purpose of this program is to generate 2 .sql files based on the contents of delimited files
placed in a specific folder.

The first file is a script related to generating new tables in .sql.

The second is concerned with importing data into those tables. It will look at the first line from
each file to determine what the field names should be.

Any empty fields will have a
field name called "NO_FIELD_NAME_X" where x is a number. So if there are two empty fields
there will be two columns labeled "NO_FIELD_NAME_1" and "NO_FIELD_NAME__2"

This model file contains the functionality needed to run the program
'''

import os
from model.Custom_Errors import *

# CONSTANTS
NON_VALID_CHARS_FIELD_NAME = ['/']
NON_VALID_CHARS_TABLE_NAME = ['[',']','#','-']
WHITE_SPACE_CHAR_LIST = [' ', '\n', '\t']
REP_DICT = {' ': r'\s', '\n': '\\n', '\t': '\\t'}
RESERVED_KEYWORDS = ['ADD', 'EXTERNAL', 'PROCEDURE', 'ALL', 'FETCH', 'PUBLIC',
                     'ALTER', 'FILE', 'RAISERROR', 'AND', 'FILLFACTOR', 'READ',
                     'ANY', 'FOR', 'READTEXT', 'AS', 'FOREIGN', 'RECONFIGURE',
                     'ASC', 'FREETEXT', 'REFERENCES', 'AUTHORIZATION',
                     'FREETEXTTABLE', 'REPLICATION', 'BACKUP', 'FROM',
                     'RESTORE', 'BEGIN', 'FULL', 'RESTRICT', 'BETWEEN', 'FUNCTION',
                     'RETURN', 'BREAK', 'GOTO', 'REVERT', 'BROWSE', 'GRANT', 'REVOKE',
                     'BULK', 'GROUP', 'RIGHT', 'BY', 'HAVING', 'ROLLBACK', 'CASCADE',
                     'HOLDLOCK', 'ROWCOUNT', 'CASE', 'IDENTITY', 'ROWGUIDCOL', 'CHECK',
                     'IDENTITY_INSERT', 'RULE', 'CHECKPOINT', 'IDENTITYCOL', 'SAVE',
                     'CLOSE', 'IF', 'SCHEMA', 'CLUSTERED', 'IN', 'SECURITYAUDIT',
                     'COALESCE', 'INDEX', 'SELECT', 'COLLATE', 'INNER',
                     'SEMANTICKEYPHRASETABLE', 'COLUMN', 'INSERT',
                     'SEMANTICSIMILARITYDETAILSTABLE', 'COMMIT', 'INTERSECT',
                     'SEMANTICSIMILARITYTABLE', 'COMPUTE', 'INTO', 'SESSION_USER',
                     'CONSTRAINT', 'IS', 'SET', 'CONTAINS', 'JOIN', 'SETUSER',
                     'CONTAINSTABLE', 'KEY', 'SHUTDOWN', 'CONTINUE', 'KILL', 'SOME',
                     'CONVERT', 'LEFT', 'STATISTICS', 'CREATE', 'LIKE', 'SYSTEM_USER',
                     'CROSS', 'LINENO', 'TABLE', 'CURRENT', 'LOAD', 'TABLESAMPLE',
                     'CURRENT_DATE', 'MERGE', 'TEXTSIZE', 'CURRENT_TIME', 'NATIONAL',
                     'THEN', 'CURRENT_TIMESTAMP', 'NOCHECK', 'TO', 'CURRENT_USER',
                     'NONCLUSTERED', 'TOP', 'CURSOR', 'NOT', 'TRAN', 'DATABASE',
                     'NULL', 'TRANSACTION', 'DBCC', 'NULLIF', 'TRIGGER', 'DEALLOCATE',
                     'OF', 'TRUNCATE', 'DECLARE', 'OFF', 'TRY_CONVERT', 'DEFAULT',
                     'OFFSETS', 'TSEQUAL', 'DELETE', 'ON', 'UNION', 'DENY', 'OPEN',
                     'UNIQUE', 'DESC', 'OPENDATASOURCE', 'UNPIVOT', 'DISK', 'OPENQUERY',
                     'UPDATE', 'DISTINCT', 'OPENROWSET', 'UPDATETEXT', 'DISTRIBUTED',
                     'OPENXML', 'USE', 'DOUBLE', 'OPTION', 'USER', 'DROP', 'OR',
                     'VALUES', 'DUMP', 'ORDER', 'VARYING', 'ELSE', 'OUTER', 'VIEW',
                     'END', 'OVER', 'WAITFOR', 'ERRLVL', 'PERCENT', 'WHEN', 'ESCAPE',
                     'PIVOT', 'WHERE', 'EXCEPT', 'PLAN', 'WHILE', 'EXEC', 'PRECISION',
                     'WITH', 'EXECUTE', 'PRIMARY', 'WITHIN GROUP', 'EXISTS', 'PRINT',
                     'WRITETEXT', 'EXIT', 'PROC']
#global self.file_number_counter
#self.file_number_counter = 1 #used for insert script commands
#-----------------------------------------------------------------------------------------

#Store the section of the scripts to write final one in the end (makes things move fast)
#WHOLE_CREATE_SCRIPT_LIST = [] #way to hold the data before writing it out
#WHOLE_BULK_INSERT_LIST = [] #way to hold the data before writing it out

class script_writer_model():
    def __init__(self):
        self.file_number_counter = 1
        self.target_dir_path = ''
        self.export_directory_path = ''
        self.delimiter = ''
        self.WHOLE_CREATE_SCRIPT_LIST = []
        self.WHOLE_BULK_INSERT_LIST = []
        self.error_tracker = []
        self.skip_file = []

    def reset_file_model_parameters(self):
        self.file_number_counter = 1
        self.target_dir_path = ''
        self.export_directory_path = ''
        self.delimiter = ''
        self.WHOLE_CREATE_SCRIPT_LIST = []
        self.WHOLE_BULK_INSERT_LIST = []
        self.error_tracker = []
        self.skip_file = []

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
        :return:
        '''
        temp = []
        empty_field_counter = 1 #used to keep count of how many empty fields there are if any
    
        #read the header from the file and store the fields
        with open(filepath_in, 'r') as filereader:
            headers_line = filereader.readline()
            all_fields_unformatted = headers_line.split(delimiter_in)
    
            for i in range(len(all_fields_unformatted)):
                field = all_fields_unformatted[i].replace(' ', '_') #replacing space char with underscore
                field = field.replace('\n','') #for last field remove newline char
    
                for char in NON_VALID_CHARS_FIELD_NAME:
                    field = field.replace(char,'') #replace any non_valid fielld chars
    
                if field in WHITE_SPACE_CHAR_LIST or field == '': #column'fields with no name
                    field = f'NO_FIELD_NAME_{str(empty_field_counter)}'
                    empty_field_counter += 1
    
                if i == len(all_fields_unformatted) - 1:
                    temp.append(f'\t\t[{field}] varchar(max)\n')
                else:
                    temp.append(f'\t\t[{field}] varchar(max),\n')
    
        return ''.join(temp)
    
    def make_create_tables_scripts(self,filepath_in: str,delimiter_in: str) -> None:
        """
        Stores the sections of the create table script that will eventually
        get written into one create table file
        :param filepath_in: @str path to the file to look at
        :return: @None
        """
        insert_list = []
    
        file_name = filepath_in.split('\\').pop()
        table_name = file_name
    
        #remove file suffix if it exist
        if '.' in file_name:
            table_list = file_name.split('.')
            table_name = table_list[0]
    
        table_name = table_name.replace(' ','_') #remove space char in table name so don't have to use brackets when calling table name
    
        for invalid_char in NON_VALID_CHARS_TABLE_NAME:
            table_name = table_name.replace(invalid_char,'')
    
        if table_name.upper() in RESERVED_KEYWORDS: #raise error if table name is a keyword insql
            raise invalid_table_name(table_name,file_name)
    
        #generate the create script per file
        ct_drop = f'IF OBJECT_ID (\'{table_name}\', \'U\') IS NOT NULL\n\tDROP TABLE dbo.{table_name};\n\n'
        fields_as_string = self.make_create_tables_fields(filepath_in,delimiter_in)
        ct_create = f'CREATE TABLE {table_name}\n\t(\n' + fields_as_string + '\t)\n\n' + '--' + ('='*50) + '\n'
        insert_list.append(ct_drop)
        insert_list.append(ct_create)
    
        self.WHOLE_CREATE_SCRIPT_LIST.append(''.join(insert_list))

        #TODO delete
        #print(''.join(insert_list))
    
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
    
    def add_insert_script(self,filepath_in: str, delimiter_in: str) -> None:
        """
        Generates the insert script sections
        :param filepath_in: @str path to the file to read
        :param delimiter_in: @str the delimiter for the file
        :return: @None
        """
        file_name = filepath_in.split('\\').pop()
    
        #TODO may be an issue for extensions longer than 3 char
        extension = file_name.split('.').pop()
        table_name = file_name
    
        if '.' in file_name:
            table_list = file_name.split('.')
            table_name = table_list[0]
        table_name = table_name.replace(' ',
                                        '_')  # remove space char in table name so don't have to use brackets
                                                    # when calling table name
    
        for invalid_char in NON_VALID_CHARS_TABLE_NAME:
            table_name = table_name.replace(invalid_char, '')
    
        if table_name.upper() in RESERVED_KEYWORDS: #raise error if table name is a keyword insql
            raise invalid_table_name(table_name,file_name)
    
        if delimiter_in in REP_DICT.keys():
            delim = REP_DICT[delimiter_in] #replace delimiter with delimiter to write in script if needed
        else:
            delim = delimiter_in
    
        trunc_cmd = f'\nIF OBJECT_ID (\'{table_name}\', \'U\') IS NOT NULL\n\tTRUNCATE TABLE dbo.{table_name};\n\n'
    
        self.WHOLE_BULK_INSERT_LIST.append(trunc_cmd)

        file_ins = 'file' + str(self.file_number_counter)
        s0 = f'\nDECLARE @{file_ins} varchar(max) = \'{file_name}\'\n'
        s0 += f'SET @{file_ins} = CONVERT(nvarchar(max), @data_src + \'\\\' + @{file_ins})\n'
        self.WHOLE_BULK_INSERT_LIST.append(s0)
        s1 = f'BULK INSERT [dbo].[{table_name}] '
        s2 = f'FROM \'\'\' + @{file_ins} + \'\'\' WITH\n'
        #s3 = f'\t(\n\tFIELDTERMINATOR = \'\'{delim}\'\',\n\tROWTERMINATOR = \'\'\\n\'\'\n\t)'
        s3 = f'\t(\n\tFIELDTERMINATOR = \'\'{delim}\'\',\n\tROWTERMINATOR = \'\'0x0A\'\'\n\t)'
        #if file_contains_headers is True:
    
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
    
        self.WHOLE_BULK_INSERT_LIST.append(t_str)
        self.WHOLE_BULK_INSERT_LIST.append('\n--' + ('=' * 50))
    
        self.file_number_counter += 1

        #TODO delete
        #print(''.join(t_str))

    def run(self):
        DELIMITER = self.delimiter

        if DELIMITER.lower().strip() == "tab": #for tab delimited
            DELIMITER = '\t'

        TARGET_DIR = self.target_dir_path
        EXPORT_PATH = self.export_directory_path

        all_files = self.get_all_filenames(TARGET_DIR)  # want to try catch for files that are not flat files
        target_files = all_files

        self.WHOLE_BULK_INSERT_LIST.append('DECLARE @data_src VARCHAR(max) = \'<<SourceLoadPath>>\'\n')

        for each_file in target_files:
            # filepath = CURRENT_DIR + '\\' + TARGET_DIR + '\\' + each_file
            filepath = TARGET_DIR + '\\' + each_file
            try:
                self.make_create_tables_scripts(filepath, DELIMITER)
            except Exception as e:
                self.error_tracker.append(f'Error: Unable to read file: {each_file}\nPotentially invalid file format like xls, should be csv, txt or other flat/delimited type... See error raised below\nError:{e.__str__()}\n{("-" * 100)}\n\n')
                continue #this will make it so the import section doesn't get hit for the errored out file either

            try:
                self.add_insert_script(filepath, DELIMITER)
            except Exception as e:
                self.error_tracker.append(f'Unable to add import table script for {each_file}\nPotentially invalid file format like xls, should be csv, txt or other flat/delimited type... See error raised below\nError:{e.__str__()}\n{("-" * 100)}\n\n')
                continue

        # write make tables script
        write_tables_script = 1
        create_table_export_full_path = EXPORT_PATH + '\\' +'CreateSourceTables.sql'
        if write_tables_script == 1:
            with open(create_table_export_full_path, 'w') as create_writer:
                create_writer.write(''.join(self.WHOLE_CREATE_SCRIPT_LIST))
            #print("COMPLETED WRITING CREATE SOURCE TABLES SCRIPT")

        write_import_script = 1
        import_data_export_full_path = EXPORT_PATH + '\\' + 'ImportData.sql'
        if write_import_script == 1:
            with open(import_data_export_full_path, 'w') as import_writer:
                import_writer.write(''.join(self.WHOLE_BULK_INSERT_LIST))
            #print("COMPLETED WRITING CREATE DATA IMPORT SCRIPT")

'''
#test works
def main():
    # if 'table'.upper() in RESERVED_KEYWORDS:
    #     raise invalid_table_name('table','filename')
    # need to test target dir
    DELIMITER = ',' #will want this as a vraibalt
    TARGET_DIR = 'D:\\Users\\ramzi.adil\\PycharmProjects\\DataSourceTool\\pythonProject\\SourceDataDirectory' # want this as a variable
    EXPORT_PATH = 'D:\\Users\\ramzi.adil\\PycharmProjects\\DataSourceTool\\pythonProject\\' #probably want  an export path as well
    all_files = get_all_filenames(TARGET_DIR) #want to try catch for files that are not flat files
    target_files = all_files

    WHOLE_BULK_INSERT_LIST.append('DECLARE @data_src VARCHAR(max) = \'<<SourceLoadPath>>\'\n')

    for each_file in target_files:
        # filepath = CURRENT_DIR + '\\' + TARGET_DIR + '\\' + each_file
        filepath = TARGET_DIR + '\\' + each_file
        make_create_tables_scripts(filepath,DELIMITER)
        # make_source_import_script(filepath)
        add_insert_script(filepath, DELIMITER)

    # write make tables script
    write_tables_script = 1
    if write_tables_script == 1:
        with open(EXPORT_PATH + 'CreateSourceTables.sql', 'w') as create_writer:
            create_writer.write(''.join(WHOLE_CREATE_SCRIPT_LIST))
        print("COMPLETED WRITING CREATE SOURCE TABLES SCRIPT")

    write_import_script = 1
    if write_import_script == 1:
        with open(EXPORT_PATH + 'ImportData.sql', 'w') as import_writer:
            import_writer.write(''.join(WHOLE_BULK_INSERT_LIST))
        print("COMPLETED WRITING CREATE DATA IMPORT SCRIPT")

    input("Press enter to exit")
'''





