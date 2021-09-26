#! /bin/bash

egrep "(^[^0-9]|[^0-9]$)" $1 | sed -e '1n;N;s/\n/ /g;'
egrep -v "(^[^0-9]|[^0-9]$)" $1

