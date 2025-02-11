'''
Custom exceptions/errors created for the program as well as constants
'''
class CustomExceptionInvalidTableName(Exception):
    def __init__(self, invalid_tablename,filename_in):
        self.message = f'TableName: \"{invalid_tablename}\" from file: \"{filename_in}\" is not a valid tablename\nA table cannot be the name of a t-sql keyword such as TABLE, ORDER,...etc\n '
        super().__init__(self.message)

    def __str__(self):
        return self.message

class CustomExceptionInvalidFile(Exception):
    def __init__(self, filename_in):
        self.message = f'Unable to decode one or more characters from file: \"{filename_in}\".\nPlease ensure only flat files are used i.e. csv, txt... not xls' \
                        f"\nOtherwise, ensure that the file is encoded in the utf-8 format"
        super().__init__(self.message)

    def __str__(self):
        return self.message

class CustomExceptionMissingEntry(Exception):
    def __init__(self, missing_entry):
        self.message = f'Missing user entry for {missing_entry}'
        super().__init__(self.message)

    def __str__(self):
        return self.message

class CustomExceptionNoFilesFound(Exception):
    def __init__(self, directory_path):
        self.message = f'There are 0 files in target directory: {directory_path}\nNo files could be processed'
        super().__init__()

    def __str__(self):
        return self.message

class CustomExceptionInvalidDirectoryPath(Exception):
    def __init__(self, directory_path, directory_entry):
        self.message = f'Entry for {directory_entry} contains an invalid filepath: {directory_path}'
        super().__init__()

    def __str__(self):
        return self.message

#CONSTANTS
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

# Designed, Written, and Tested By Ramzi Reilly Adil

image_1 = '''
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

image_2 = '''
      |\      _,,,---,,_
ZZZzz /,`.-'`'    -.  ;-;;,_
     |,4-  ) )-,_. ,\ (  `'-'
    '---''(_/--'  `-'\_)  
'''

# Designed, Written, and Tested By Ramzi Reilly Adil