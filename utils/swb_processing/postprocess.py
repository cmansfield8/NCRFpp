#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: coman8@uw.edu

This script takes the NCRFpp output and postprocesses for error analysis.

- Ignores certain token/POS to match LM scores
- Adds function/content/other categories to POS tags
- Outputs 1 sentence per line
- Empty lines have empty tags
"""

import argparse
import csv


def get_shape(token, tag, tok_map, tag_map):
	if token == '#':
		return None
	if token in tok_map.keys():
		return tok_map[token]
	else:
		try:
			return tag_map[tag]
		except KeyError:
			print("Shape not found for tag: {}".format(tag))
	return 'UNK'
	
def read_mapper(file):
	reader = csv.reader(open(file, 'r'), delimiter='\t')
	result = dict()
	for row in reader:
		result[row[0]] = row[1]
	return result
	
	
def special_token(current, previous):
	"""checks for conditions for ignoring token and pos"""
	if current[0].startswith("\'") or current[0].startswith("n\'t"): 
		# skip contractions
		return True
	# elif current[0] == "not" and previous and previous[0] == "can":
		# can not is treated as 1 word
		# return True
	# elif current[0] == "to" and previous and previous[0] in ["going", "want"]:
		# gonna and wanna
		# return True
	elif current[1].startswith("1.0000"): 
		# SOS
		return True
	return False


def main(args):
	try:
		tok_map = read_mapper("tokenshapes.tsv")
		tag_map = read_mapper("tagshapes.tsv")
	except FileNotFoundError as e:
		print("tokenshapes.tsv and tagshapes.tsv file expected")
	
	sentences = list()
	temp = list()
	previous = None

	reader = csv.reader(open(args.file, 'r'), delimiter=' ')
	for current in reader:
		if not current: # start a new sentence
			sentences.append(list(map(list, zip(*temp))))
			temp = list()
			previous = None
		elif special_token(current, previous): # skip these tokens
			continue
		else:
			if current[0] == '#':  # empty sentence case
				temp.append((None, None))
			else:
				shape = get_shape(current[0], current[1], tok_map, tag_map)
				temp.append((current[1], shape))
		previous = current

	writer = csv.writer(open(args.output, 'w'), delimiter='\t')
	writer.writerow([args.prefix+'_tags', args.prefix+'_shapes'])
	for tags, shapes in sentences:
		if tags == [None]:  # empty sentence case
			writer.writerow([list(), list()])
		else:
			writer.writerow([tags, shapes])


if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="File decoded from NCRFpp")
	parser.add_argument("output", help="Output file name")
	parser.add_argument("prefix", help="Prefix of the header")
	args = parser.parse_args()
	main(args)
