Program: Ramzi's Delimited File SQL Writing Tool 

Program Version: 1.2

Written in Python Version: 3.10.7

Author: Ramzi Reilly Adil

Fork Name: EERP

## Table of Contents
- [Background](#background)
- [Install Requirements](#Install-Requirements)
- [How To Use](#How-To-Use)
- [GUI](#Graphical-User-Interface)
- [Features](#Features)
- [Author Notes](#Author-Notes)
- [Contributors](#Contributors)
- [Maintainers](#Maintainers)
- [Submitting Issues](#Submitting-Issues)
- [Future Goals](#Future-Goals)


## Background
In SQL, one of the tedious and potentially time consuming tasks is to create tables and import data from delimited files
like .csv's, .txt's, ... etc. You need to match the table names and field names and if you have a large amount of files
it can take up a lot of time. I wrote this tool as a way to take a look at all the headers of those files
and generate the scripts for me. This program will generate 2 files, the first is a CreateSourceTables.sql
which contains create tables commands and an ImportData.sql which contains the bulk insert commands.
You can then run the generated scripts in SQL. The scripts generated are made for SQL server or T-SQL.

## Install Requirements
- Python version 3.10.7 and above

## How To Use
- Install python
- Make sure python is added to the path in your system
- Clone/download this repo to your local
- Double click "program_run.py" file or run the command: "python program_run.py" from the terminal.
If using the terminal, make sure the terminal is navigated to your clone of this repo.

## Graphical User Interface
The GUI requires some entries be filled before running.
You will need to input the directory the delimited files are located in, the directory 
where you want the generated sql scripts to be made, the delimiter used in the files
(in the case of .csv, it's a comma, if it's tab delimited you have to use the 
string "tab"), as well as the row terminator. Then you can click the "run" button
at the bottom right corner of the GUI.

## Features
- Automatically replaces the space character 
with an underscore in both the table names and field names
for the CreateSourceData.sql. 
    - For example: if a delimited source file called "Data Set 1" has field called "First Name" then the scripts generated
will have a create statement for the table "Data_Set_1" with a field "First_Name"



- Automatically assigns field names if the source file
does not list them.
  - For example: If a file has 4 columns and two are listed as empty like "First Name,,Last Name," then the table created will have the fields: "First_Name, NO_FIELD_NAME_1,Last_Name,NO_FIELD_NAME_2".


- Skips any files that it cannot read such as .zip files. More info will show up in the summary window that pops up after hitting the run button. This will say the "program completed with errors" meaning, it will work on the valid files but list out the ones that were invalid.


- There is a variable that will be generated in the ImportData.SQL script called: @data_src
  - By default it is set to '<\<SourceDataLoadPath\>>'
  - You will want to replace '<\<SourceDataLoadPath\>>' with the actual path to the directory
  containing the delimited files 

- Adds a flag to the ImportData.sql and CreateSourceTables.sql that you will need to change
in order for the actual script to run on sql.


- Browse button on GUI to select folders in your native OS so you do not
need to manually type out the path to the directory.


- Generated ImportData.sql script will identify failed file imports by printing them
failed files to the SQL terminal in most cases. 

## Author Notes
Written in model-view-controller architectural design pattern.

If you create a fork of this repo or clone it with your own edits, all I ask is that you leave a link
to this original repo and credit me so that I can see what changes others will make. It may help
me improve this master fork in the future. Thank you!

Included in this repo is a directory called ExampleDataFile. You can 
use this as a way to test the program yourself. Select it as the "Target Directory"
in the GUI and set the delimiter to "," (comma only no quotes).

## Contributors
- Ramzi Reilly Adil: Designer, Developer, and Tester

## Maintainers
- [@radil708](https://github.com/radil708)

## Submitting Issues
If you have any comments on how to improve the program or any features you think may be useful, feel free to submit an issue.

You can submit issues here -> [Open an issue](https://github.com/radil708/RamziDataSourceTool/issues/new).

## Future Goals
- Add a flag to ask if the user wants to replace the space character in table names with an underscore
- Add a flag to ask if the user wants to replace the space character in field names with an underscore




