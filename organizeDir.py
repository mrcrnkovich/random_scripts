#script to sort files by suffix into folders

import os
import shutil
from sys import exit
import argparse
from pathlib import Path

verbose = False

#function receives Path object ('current_dir') and list of file_types
def temp_function_name(current_dir, file_types):

    for folder in file_types:
        
        #check if directory exists, create directory if it does not exist
        if os.path.exists(folder):
            if verbose:
                print(f'{folder}: already exists')
        else:
            os.mkdir(folder)
            if verbose:
                print(f'{folder}: created')

        move_files(current_dir, folder)


def move_files(current_dir, folder_name):

    for file in current_dir.glob("*."+folder_name):
        shutil.move(file.name, folder_name+"/"+file.name)

    if verbose:
        print(f'{folder_name} successfully moved')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Folder Location")

    parser.add_argument('directory', help="enter complete directory location")
    parser.add_argument('-v', dest='verbose', action='store_const', default=False, 
            const=True, help="Verbose output option")

    args = parser.parse_args()

    verbose = args.verbose

    if os.path.isdir(args.directory):
        os.chdir(args.directory)
    else:
        print(f'{args.directory} does not exist')
        print("Exiting...")
        exit()

    current_dir = Path('.')
    file_types = list(set([x.suffix[1:] for x in current_dir.iterdir() if x.is_file()]))
    file_types.remove('')

    temp_function_name(current_dir, file_types)