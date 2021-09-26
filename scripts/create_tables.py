#! /bin/python3

from pathlib import Path
from argparse import ArgumentParser

def create_table_statement(name, cols):
    """
    Method to take 3 SQL table characteristics
    and turn them into a create table statement
    column info should be passed as a list of dicts 
    """
    
    s = f'CREATE TABLE {name}'

    col_list = []
    for col in cols:
        col_list.append(f'\t{col["name"]} {col["dtype"]} {col["null"]}')

    col_list.append("\tYEAR INTEGER NOT NULL")

    return s + '(\n' + ',\n'.join(col_list) + ');\n'

def get_table_data(filename):
    """
    Method to take column information from DOL Meta-files
    and return a list of dicts containing field information.
    """

    table = []
    try:
        with open(filename, "r") as f:
            f_lines = f.readlines()
            for line in f_lines[2:]:
                data = line.split()
                table.append({
                    'name': data.pop(0),
                    'dtype': data.pop(-1),
                    'null':' '.join(data)
                    })
    except:
        print (f'error with loading file {filename}')
        return
    return table

def get_meta_files(meta_path):
    meta_files = Path(meta_path).glob('*_meta.txt')
    
    out = ""    
    for file in meta_files:
        name = '_'.join(file.stem.split('_')[1:-1])
        out += create_table_statement(name,
                    get_table_data(file)) + "\n"
    return out


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("meta", help="Location of meta data files")
    print(get_meta_files(parser.parse_args().meta))