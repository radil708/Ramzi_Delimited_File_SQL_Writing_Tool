Program: SQL Data Source Tool 

Program Version: 1.1

Written in Python Version: 3.10.7

Author: Ramzi Reilly Adil

## Table of Contents
- [Background](#background)
- [Install Requirements](#Install-Requirements)
- [How To Use](#How-To-Use)
- [GUI](#Graphical-User-Interface)
- [Features](#Features)
- [Author Notes](#Author-Notes)
- [Contributors](#Contributors)
- [Maintainers](#Maintainers)


## Background
In SQL, one of the tedious more laborious tasks is to create tables and import data from delimited files
like csv. You need to match the table names and field names and if you have a large amount of files
it can take up a lot of time. I wrote this tool as a way to take a look at all the headers of those files
and generate the scripts for me. This program will generate 2 files, the first is a CreateSourceTables.sql
which contains create tables commands and an ImportData.sql which contains the bulk insert commands.
You can then run the generated scripts in SQL. The scripts generated are made for SQL server or T-SQL.

## Install Requirements
- Python version 3.10.7 and above

## How To Use
Simply run the program_run.py program. This will bring up a graphical user interface (GUI)
that a user can interact with.

## Graphical User Interface
The GUI requires some entries be filled before running.
You will need to input the directory the delimited files are located in, the directory 
where you want the generated sql scripts to be made, the delimiter used in the files
(in the case of .csv, it's a comma, if it's tab delimited you have to use the 
string "tab"), as well as the row terminator. Then you can click the "run" button
at the bottom right corner of the GUI.

## Features
- The program will automatically replace the space character 
with an underscore in both the table names and field names
for the CreateSourceData.sql
- The program will skip any files that it cannot read automatically such as .zip files. An error will show up in the summary window that pops up after hitting the run button. This will say the "program completed with errors" meaning, it will work on the valid files but list out the ones that were invalid.

## Author Notes
There are some portions of the script that are specific to my personal needs such as the addition
of variables surrounded by '<<>>'. If you are using this you may remove those variables or modify
them as needed.

If you create a fork of this repo or clone it with your own edits, all I ask is that you leave a link
to this original repo and credit me so that I can see what changes others will make. It may help
me improve this master fork in the future. Thank you!

## Contributors
- Ramzi Reilly Adil: Designer, Developer, and Tester

## Maintainers
- [@radil708](https://github.com/radil708)

## Submitting Requests Or Issues
If you have any comments on how to improve the program or any features you think may be useful, feel free to submit an issue.

You can submit issues here -> [Open an issue](https://github.com/radil708/RamziDataSourceTool/issues/new).




