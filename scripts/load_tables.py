#! /bin/python3

import os
from pathlib import Path
from argparse import ArgumentParser

def write_copy_data_statement(path):
    """
    method to write upload data statement
    """
    p = Path(path).glob('*.csv')
    stmts = []
    for file in p:
        # drop year at the end of the filename to get
        #table name
        tb_name = file.stem
        stmts.append(f"\COPY {tb_name} FROM {file} "
            + "WITH DELIMITER '|' CSV HEADER;")

    return stmts

def pp_add_year_column(location):
    # pre-process files to add year column 

    p = Path(location).glob('*.txt')
    for file in p:
        year = file.stem.split('_')[-1]
        output = '_'.join(file.stem.split('_')[1:-2])
        os.system(f'./add_year.sh {year} {file} {location}/tmp/{output}.csv')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("location", help="Location of meta data files")
    location = parser.parse_args().location

    pp_add_year_column(location)
    print('\n'.join(write_copy_data_statement(location+"/tmp")))