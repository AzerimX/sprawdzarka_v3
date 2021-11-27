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
        path = path_validation()
        extension = ""
        if input_file_type == "1":
            extension = ".jpg"
        if input_file_type == "2":
            extension = ".jpg"
        if input_file_type == "3":
            extension = ".tif"

        # Process the files
        process_inputs(path, extension)

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


def process_inputs(path, extension):
    """Driver function for processing the files"""
    file_list = list_files(path, extension)
    file_list = split_and_strip(file_list, extension)
    file_list = length_check(file_list)  # todo len check


def list_files(path, extension):
    """Make a list of full file names with correct extension"""
    # Search directory, add full directories to
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


def split_and_strip(file_list, extension):
    """Split the list, strip elements and add a full path at the end"""

    # Extract file names
    file_names = []
    for file_path in file_list:
        file_path = file_path[:-1 * len(extension)]
        file_names.append(os.path.basename(file_path))

    # Strip, split and add full path as first position
    split_list = [x.split(',') for x in file_names]  # split file names into columns
    for i in range(len(file_names)):
        split_list[i].insert(0, file_list[i])
    for row in split_list:
        print(row)
    return split_list



def length_check(file_list):
    ... # TODO


main()