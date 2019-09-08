""" open General Ledger from Excel, reformat into a database. """
import pandas as pd
import numpy as np
import argparse

col_name = ["Account Description", "Type", "Date", "Num", "Name",
            "Memo", "Split", "Amount", "Balance"]


def format_file(df, col_name=col_name):

    df['Account Description'] = merge_columns(df[[1, 2, 3]])

    # clean up empty columns/rows
    df = df.drop(0)
    df = df.drop([0, 1, 2, 3, 4], axis=1)
    df = df.dropna(axis=0, thresh=6)
    df = df.dropna(axis=1, how='all')

    # Reindex Columns
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df.columns = col_name

    return df


def merge_columns(df):

    # Create single column from DataFrame argument. Value in the merged column
    # will be the first non-NaN value encountered in the row. If the entire row
    # is NaN, it will fill using the previous value in the merged column.

    temp_df = df.copy()
    temp_df = temp_df.replace(' ', np.nan)
    temp_df["mergeColumn"] = [np.nan for _ in df.index]

    for column in temp_df.columns:
        temp_df["mergeColumn"] = temp_df["mergeColumn"].fillna(temp_df[column])

    return temp_df["mergeColumn"].fillna(method='ffill')


def open_file(filename):

    # try to open filename as Pandas DataFrame, if error, quit.
    try:
        df = pd.read_excel(filename, index_col=None, header=None)
        return df
    except:
        print("Error with filename")
        quit()


def main():

    parser = argparse.ArgumentParser(
                description='Location of Excel File to be formatted.')
    parser.add_argument('file_location', type=str, help='file location')
    args = parser.parse_args()

    file = format_file(open_file(args.file_location))
    # consider using Path object for file location, to allow for
    # more accurate location saving.
    file.to_csv("modified_GL.csv")
    print(file)


if __name__ == "__main__":
    main()
