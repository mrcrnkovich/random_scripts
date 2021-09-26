#! /bin/bash

echo "Reformatting Test database"
psql -h localhost -U postgres -c "DROP DATABASE $1" -c "CREATE DATABASE $1"
echo "$1 reformatting complete"

echo "Starting process to create tables from dir"
./create_tables.py "$2/meta"> ../tmp/create_tables.txt
psql -h localhost -U postgres $1 -f "../tmp/create_tables.txt"
echo "table statements created"

echo "Starting process to create load statements for tables"
rm -rf "$2/tmp"
mkdir "$2/tmp"
./load_tables.py "$2" > ../tmp/load_tables.txt
psql -h localhost -U postgres $1 -f "../tmp/load_tables.txt"
echo "process complete"