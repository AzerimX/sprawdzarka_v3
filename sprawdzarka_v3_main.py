import os
import pathlib
#import pandas as pd
import numpy as np

#Hi github!
#doing stuff
foo = "1232"
password="123"

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

        # Search the directory and find all files with given extension
        file_list = list_files(path, extension)
        file_list = split_and_strip(file_list)


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


def split_and_strip(file_list, extension): # TODO make it full path, then rest of fields , end of file?
    """Split the list, strip elements and add a full path at the end"""
    split_list = [x.split(',') for x in file_list[0]]  # split file names into columns
    for i in range(len(split_list)):
        split_list[i] = [x.strip() for x in split_list[i]]  # strip all fields from leading/trailing spaces
        split_list[i][-1] = split_list[i][-1][0: -1 * len(extension)]  # remove .jpg or .tif

        # add full file name, number and move file name (IDZI-IWAN_2034) closer to beginning
        temp_list = [str(i + 1), file_list[2][i], split_list[i][-1]]
        split_list[i] = temp_list + split_list[i]
        split_list[i] = split_list[i][0:-1]
    return split_list


main()