#! /bin/bash

sed "s/[\'\"]//g" $2 | gawk -v year=$1 -F"|" ' NR>1 { print $0 "|" year }' >> $3