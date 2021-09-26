#! /bin/bash

FC="$(gawk -F'|' ' NR==1 { print NF } ' $1)"
filename="$(echo $1 | gawk -F'/' ' { print $NF } ' "
echo "Fields Found: "${FC}
echo "Filename: "${filename}
mkdir errors
mkdir clean
gawk -F'|' -v FC=$FC ' NR!=FC { print $0 } ' $1 > errors/$1
gawk -F'|' -v FC=$FC ' NR==FC { print $0 } ' $1 > clean/$1
echo "completed"
