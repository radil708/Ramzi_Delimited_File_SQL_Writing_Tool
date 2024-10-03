'''
The purpose of this program is to look at files in the target directory (TARGET_DIR)
reads the first line of each file and make the create tables script making every field
a varchar(max). The first line must contain the fields in the files
'''
#idea check for invalid field names for tables
import os


CURRENT_DIR = os.getcwd()
TARGET_DIR = "SourceDataDirectory"
DELIMITER = ','
EXCLUDED_FILES = []
NON_VALID_CHARS_TABLE_NAME = ['[',']','#','-']
NON_VALID_CHARS_FIELD_NAME = ['/'] #Non valid chars for table name
WHOLE_CREATE_SCRIPT_LIST = [] #way to hold the data before writing it out
#field names replace space with underscor
WHOLE_IMPORT_SCRIPT_LIST = []
WHOLE_BULK_INSERT_LIST = []

DO_FILES_HAVE_HEADERS = True

#Helper Dictionary
REP_DICT = {' ': r'\s', '\n': '\\n', '\t': '\\t'}

WHITE_SPACE_CHAR_LIST = [' ', '\n', '\t']
FILEPATH_TO_TABLENAME_DICT = {}

FILE_NUMBER_COUNTER = 1

def get_all_filenames(target_directory: str) -> list:
    '''
    Get all filenames from a specific directory
    :param target_directory:
    :return:
    '''
    return os.listdir(target_directory)

def filter_out_exclded_files(list_to_filter: list) -> list:
    filtered = list(filter(lambda x: x not in EXCLUDED_FILES, list_to_filter))
    return filtered

def make_create_tables_fields(filepath: str) -> str:
    '''
    Helper func to make_create_tables_scripts
    :param filepath:
    :return:
    '''
    temp = []
    empty_field_counter = 1
    with open(filepath, 'r') as filereader:
        headers_line = filereader.readline()
        all_fields_unformatted = headers_line.split(DELIMITER)
        for i in range(len(all_fields_unformatted)):
            field = all_fields_unformatted[i].replace(' ', '_') #replacing space char with underscore
            field = field.replace('\n','') #for last field remove newline char

            for char in NON_VALID_CHARS_FIELD_NAME:
                field = field.replace(char,'')

            if field in WHITE_SPACE_CHAR_LIST or field == '': #column'fields with no name
                field = f'NO_FIELD_NAME_{str(empty_field_counter)}'
                empty_field_counter+= 1

            if field == 'file':
                field = 'file_'

            if i == len(all_fields_unformatted) - 1:
                temp.append(f'\t\t{field} varchar(max)\n')
            else:
                temp.append(f'\t\t{field} varchar(max),\n')
    return ''.join(temp)


def make_create_tables_scripts(filepath: str) -> None:
    '''
    :param filepath:
    :return:
    '''
    insert_list = []
    file_name = filepath.split('\\').pop()
    table_name = file_name
    #remove file suffix if it exist
    if '.' in file_name:
        table_list = file_name.split('.')
        table_name = table_list[0]

    table_name = table_name.replace(' ','_') #remove space char in table name so don't have to use brackets when calling table name


    #TODO temp for this proj replace - with @ symbol
    table_name = table_name.replace('-','@')

    #table name cannot end in word called file
    full_table_name_len = len(table_name)
    if table_name[full_table_name_len - 4: full_table_name_len] == 'file':
        table_name += '_'


    for invalid_char in NON_VALID_CHARS_TABLE_NAME:
        table_name = table_name.replace(invalid_char,'')


    ct_drop = f'IF OBJECT_ID (\'{table_name}\', \'U\') IS NOT NULL\n\tDROP TABLE dbo.{table_name};\n\n'
    fields_as_string = make_create_tables_fields(filepath)
    ct_create = f'CREATE TABLE {table_name}\n\t(\n' + fields_as_string + '\t)\n\n' + '--' + ('='*50) + '\n'
    insert_list.append(ct_drop)
    insert_list.append(ct_create)
    WHOLE_CREATE_SCRIPT_LIST.append(''.join(insert_list))

def make_source_import_script(filepath: str):
    file_name = filepath.split('\\').pop()
    table_name=file_name

    if '.' in file_name:
        table_list = file_name.split('.')
        table_name = table_list[0]
    table_name = table_name.replace(' ','_')  # remove space char in table name so don't have to use brackets when calling table name
    # TODO temp for this proj replace - with @ symbol
    table_name = table_name.replace('-', '@')

    # table name cannot end in word called file
    full_table_name_len = len(table_name)
    if table_name[full_table_name_len - 4: full_table_name_len] == 'file':
        table_name += '_'

    for invalid_char in NON_VALID_CHARS_TABLE_NAME:
        table_name = table_name.replace(invalid_char, '')

    WHOLE_IMPORT_SCRIPT_LIST.append(f'\texec sp_LoadData \'{filepath}\', \'{table_name}\')\n')

def wrap_in_try_catch(input: str, optional_tablename: str = 'table') -> str:
    global FILE_NUMBER_COUNTER

    if '@' in optional_tablename:
        just_table_name = (optional_tablename.split('@'))[1].replace('[','').replace(']','')
    else:
        just_table_name = optional_tablename
    truncate = f"TRUNCATE TABLE {just_table_name}"
    zero = f'DECLARE @command{FILE_NUMBER_COUNTER} varchar(max) ='
    #TODO have an extension figure outer
    filename = optional_tablename + '.csv'
    first = '\'BEGIN TRY\n' + input + '\nEND TRY\n'
    second = f'BEGIN CATCH\n\tPRINT \'\'Failed to insert data from {filename} into [dbo].[{optional_tablename}]\'\'\n' + 'END CATCH\'\n'
    third = f'exec(@command{FILE_NUMBER_COUNTER})'
    return zero + first + second + third

def add_insert_script(filepath: str, optional_del : str = ' ', file_contains_headers: bool = True) -> None:
    file_name = filepath.split('\\').pop()
    #TODO may be an issue for extensions longer than 3 char
    extension = file_name.split('.').pop()
    table_name = file_name
    if '.' in file_name:
        table_list = file_name.split('.')
        table_name = table_list[0]
    table_name = table_name.replace(' ',
                                    '_')  # remove space char in table name so don't have to use brackets when calling table name
    table_name = table_name.replace('-', '@')
    # table name cannot end in word called file
    full_table_name_len = len(table_name)
    if table_name[full_table_name_len - 4: full_table_name_len] == 'file':
        table_name += '_'

    for invalid_char in NON_VALID_CHARS_TABLE_NAME:
        table_name = table_name.replace(invalid_char, '')

    global FILE_NUMBER_COUNTER

    if optional_del in REP_DICT.keys():
        delim = REP_DICT[optional_del]
    else:
        delim = optional_del

    trunc_cmd = f'\nIF OBJECT_ID (\'{table_name}\', \'U\') IS NOT NULL\n\tTRUNCATE TABLE dbo.{table_name};\n\n'
    WHOLE_BULK_INSERT_LIST.append(trunc_cmd)

    file_ins = 'file' + str(FILE_NUMBER_COUNTER)
    s0 = f'\nDECLARE @{file_ins} varchar(max) = \'{file_name}\'\n'
    s0 += f'SET @{file_ins} = CONVERT(nvarchar(max), @data_src + @{file_ins})\n'
    WHOLE_BULK_INSERT_LIST.append(s0)
    s1 = f'BULK INSERT [dbo].[{table_name}] '
    s2 = f'FROM \'\'\' + @{file_ins} + \'\'\' WITH\n'
    s3 = f'\t(\n\tFIELDTERMINATOR = \'\'{delim}\'\',\n\tROWTERMINATOR = \'\'\\n\'\'\n\t)'
    if file_contains_headers is True:
        s3 = s3.lstrip('\t(')
        s3 = f'\t(\n\tFIRSTROW = 2,' + s3

    temp = [s1,s2,s3]

    if extension == 'csv':
        s3 = temp.pop()
        s3 = s3.rstrip('\n\t)')
        s3 = s3 + ",\n\tFORMAT = ''CSV''\n\t)"
        temp.append(s3)

    t_str = ''.join(temp)
    t_str = wrap_in_try_catch(t_str,table_name)
    WHOLE_BULK_INSERT_LIST.append(t_str)
    WHOLE_BULK_INSERT_LIST.append('\n--' + ('=' * 50))

    FILE_NUMBER_COUNTER += 1

def main():
    all_files = get_all_filenames(TARGET_DIR)
    target_files = filter_out_exclded_files(all_files)

    WHOLE_BULK_INSERT_LIST.append('DECLARE @data_src VARCHAR(max) = \'<<SourceLoadPath>>\'\n')

    for each_file in target_files:
        #filepath = CURRENT_DIR + '\\' + TARGET_DIR + '\\' + each_file
        filepath = TARGET_DIR + '\\' + each_file
        make_create_tables_scripts(filepath)
        #make_source_import_script(filepath)
        add_insert_script(filepath,DELIMITER,DO_FILES_HAVE_HEADERS)

    #write make tables script
    write_tables_script = 1
    if write_tables_script == 1:
        with open('CreateSourceTables.sql','w') as create_writer:
            create_writer.write(''.join(WHOLE_CREATE_SCRIPT_LIST))
        print("COMPLETED WRITING CREATE SOURCE TABLES SCRIPT")

    write_import_script = 1
    if write_import_script == 1:
        with open('ImportData.sql','w') as import_writer:
            import_writer.write(''.join(WHOLE_BULK_INSERT_LIST))
        print("COMPLETED WRITING CREATE DATA IMPORT SCRIPT")

    input("Press enter to exit")

if __name__ == '__main__':

    main()

#'F:\Users\ramzi.adil\temp_nartax\'