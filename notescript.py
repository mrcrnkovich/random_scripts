#!/usr/bin/python3

import re
from datetime import date, timedelta
from os import chdir, listdir, makedirs, getenv
from os.path import exists, expanduser
from subprocess import run

HOME = expanduser("~")
EDITOR = getenv("EDITOR") or "nvim"
NOTES_DIR = getenv("NOTES_DIR") or expanduser("~/notes")


def new_week(file_path: str, date_stamp: str, last_filepath: str):
    template_path = "/home/mike/notes/tasks/template.md"
    

    with open(file_path, 'w') as file:
        file.write(f"# {date_stamp}\n\n")

        if last_filepath:
            # Need to handle carrying prior week tasks forward
            file.write("## TODO from last week:\n\n")
            with open(last_filepath, 'r') as last_week:
                todo = re.compile('^\s+\[\s\]')
                line =  last_week.readline()
                while line:
                    if todo.match(line):
                        file.write(line)
                    line = last_week.readline()

            file.write("\n")    # line padding between sections    

        with open(template_path, 'r') as template:
            line = template.readline()
            while line:
                file.write(line)
                line = template.readline()


def get_last_file(start_workweek: date)->str:
    last_week = start_workweek - timedelta(7)
    last_week_dir = f"{NOTES_DIR}/tasks/{last_week.year}/{last_week.month}"
    last_timestamp = f"{last_week.year}-{last_week.month}-{last_week.day}"
    last_filepath = f"{last_week_dir}/{last_timestamp}.md"

    if not exists(last_filepath):
        print("failed to find last weeks notes")
        last_filepath = None

    return last_filepath


def main():
    today = date.today()
    start_workweek = today - timedelta( today.isoweekday() - 1 )

    month_dir = f"{NOTES_DIR}/tasks/{start_workweek.year}/{start_workweek.month}"
    date_stamp = f"{start_workweek.year}-{start_workweek.month}-{start_workweek.day}"
    note_file = f"{month_dir}/{date_stamp}.md"

    chdir(NOTES_DIR)
    makedirs(month_dir, exist_ok=True)

    if not exists(note_file):
        last_filepath = get_last_file(start_workweek)
        new_week(note_file, date_stamp, last_filepath)

    run([f"/usr/bin/{EDITOR}", note_file])


if __name__ == '__main__':
    main()
