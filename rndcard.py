#! /usr/bin/python

# parse input list from terminal
# random num generator for the len of the list
# will slice which cards from list using random num generator
# will pop(i) from the list, which will decrease the list size and rndnumber each time

import sys
import random

def shuffle(input):	

	shuffled = []

	while (len(input) > 0 ):
		x = random.randrange(0,len(input), 1)
		shuffled.append(input.pop(x))
	
	return shuffled

def parse_input(input):
	
	w = ""
	ls_input = []

	for c in input:
		if (c==' ' or c==',' or c==';' or c=='\t' or c=='\n'):
			ls_input.append(w)
			w = ""
		else:
			w += c

	return ls_input

def main():
	
	#parse stream input into a list
	input = parse_input(sys.stdin.read())	
	
	#print shuffled input
	print(shuffle(input))


if __name__ == "__main__":
	main()
	

