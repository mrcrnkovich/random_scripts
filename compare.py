#!/usr/bin/env python3

import argparse
import filecmp

def compare ( f1 , f2 ):
	print(filecmp.cmp(f1 , f2))



parser = argparse.ArgumentParser(description = "Compare Files")
parser.add_argument(dest = "filename" , nargs = '*',  type=str , help = "Add filename here")

args = parser.parse_args()
print(args.filename)

compare(args.filename[0],args.filename[1])
