import os
import pathlib
#import pandas as pd
import numpy as np

# Hi Github!


def main():
    input_file_type = input('Podaj typ plików:\n'
                            '1: KPO (Szufladki)\n'
                            '2: POW\n'
                            '3: PSZ\n'
                            '0: Zamknij program\n')
    if input_file_type in ["1", "2", "3"]:
        input_file_type = int(input_file_type)
        path = path_validation()
        filled_table = process_inputs(path, input_file_type)
        filled_table = check_errors(filled_table, input_file_type)
        save_to_file(filled_table, input_file_type)
    elif input_file_type in ["", "0"]:
        quit()
    else:
        print("Nie wybrano poprawnej opcji.")
        main()


def path_validation():
    """Check if path exists, if not ask user for correct one"""
    input_path = input("Podaj ścieżkę: \n")
    if input_path != "":
        if os.path.exists(input_path.strip()):
            return pathlib.PureWindowsPath(input_path)
        else:
            print("Podana ścieżka nie istnieje.")
            return path_validation()
    else:
        print("Nie podano ścieżki")
        return path_validation()


def process_inputs(path, input_file_type):
    """Driver function for processing the files"""
    file_list = list_files(path, input_file_type)
    file_list = split_and_strip(file_list, input_file_type)
    filled_table = populate_table(file_list, input_file_type)
    return filled_table


def list_files(path, input_file_type):
    """Make a list of full file names with correct extension"""
    # Search directory, add full directories to
    extension = input_file_type_to_extension(input_file_type)
    full_paths = []
    for root, dirs, files in os.walk(os.path.abspath(path), topdown=False):  # walk down the tree from givenPath
        for name in files:  # for each filename that is a file (not a dir)
            if name == "thumbs.db" or name == "Thumbs.db":  # ignore temporary thumbnail files
                continue
            if name.endswith(extension):
                full_paths.append(os.path.join(root, name))

    # Make them into Linux/universal paths
    full_paths = [x.replace("\\", "/") for x in full_paths]
    return full_paths


def split_and_strip(file_list, input_file_type):
    """Split the list, strip elements and add a full path at the end"""

    extension = input_file_type_to_extension(input_file_type)

    # Extract file names
    file_names = []
    for file_path in file_list:
        file_path = file_path[:-1 * len(extension)]
        file_names.append(os.path.basename(file_path))

    # Strip, split and add full path as first position
    split_list = [x.split(',') for x in file_names]  # split file names into columns

    for i in range(len(split_list)):
        for j in range(len(split_list[i])):
            split_list[i][j] = split_list[i][j].strip()

    for i in range(len(file_names)):
        split_list[i].insert(0, file_list[i])
    # for row in split_list:
    #     print(row)  # todo remove
    return split_list


def populate_table(file_list, input_file_type):
    filled_table = []
    # How the table should look like:
    # [0] Full Path
    # [1] Surname
    # [2] Name
    # [3] Year of birth
    # [4] Father's name
    # [5] Signatures
    # [6] Name of file
    # [7] Errors

    # Create empty table to be filled
    for i in range(len(file_list)):
        filled_table.append([])
        for j in range(0, 8):
            filled_table[i].append("")

    # Fill fields that are the same for all tables
    for i in range(len(file_list)):
        filled_table[i][0] = file_list[i][0]
        row_length = len(file_list[i])
        if row_length < 6:
            filled_table[i][7] += "za mało przecinków; "
        elif row_length > 6 and (input_file_type == 2 or input_file_type == 3):
            filled_table[i][7] += "za dużo przecinków; "
        else:
            # Correct number of fields, fill table:
            filled_table[i][1] = file_list[i][1]  # Surname
            filled_table[i][2] = file_list[i][2]  # Name
            filled_table[i][3] = file_list[i][3]  # Year of birth
            filled_table[i][4] = file_list[i][4]  # Father's name

            # Fill signatures and end of file

            # KPO
            if input_file_type == 1:
                signature_fields = file_list[i][5:-1]
                for signature in signature_fields:
                    filled_table[i][5] += signature + "; "
                filled_table[i][6] = file_list[i][-1]

            # POW
            elif input_file_type == 2:
                start_of_file_name = file_list[i][5].find("_")
                filled_table[i][5] = file_list[i][5][:start_of_file_name]  # fix me variable numbers
                filled_table[i][6] = file_list[i][5][start_of_file_name:]

            # PSZ - signature field should be empty
            elif input_file_type == 3:
                filled_table[i][6] = file_list[i][5]

    # testing todo remove
    print(filled_table)
    for row in filled_table:
        print(row)
    # testing todo remove

    return filled_table


def input_file_type_to_extension(input_file_type):
    if input_file_type == 1:
        return ".jpg"
    elif input_file_type == 2:
        return ".jpg"
    elif input_file_type == 3:
        return ".tif"


def check_errors(filled_table, input_file_type):
    """Return the table with errors checked"""
    ...
    return filled_table
    #todo

def save_to_file(filled_table, input_file_type):
    ...
    #todo

main()
