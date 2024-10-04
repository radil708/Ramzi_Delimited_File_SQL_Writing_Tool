
class invalid_table_name(Exception):
    def __init__(self, invalid_tablename,filename_in):
        self.message = f'TableName: \"{invalid_tablename}\" from file: \"{filename_in}\" is not a valid tablename\nA table cannot have the name of a t-sql keyword such as \'table\',\'update\'.. etc\n '
        super().__init__(self.message)

class invalid_file(Exception):
    def __init__(self, filename_in):
        self.message = f'Unable to read file {filename_in}, please ensure only flat files are used i.e. csv, txt... not xls'
        super().__init__(self.message)