#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: coman8@uw.edu

This script takes the NCRFpp output and incorporates into alignment file.

- Adds function/content/other categories to POS tags
- Empty lines have [None] tags

"""

import argparse
import csv
import pandas as pd


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
	
	
def skip_token(current, previous):
	if current[1].startswith("1.0000"): 
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
		elif skip_token(current, previous): # skip these tokens
			continue
		else:
			if current[0] == '#':  # empty sentence case
				temp.append((None, None))
			elif current[0] == "know" and previous and previous[0] == "you":  # you_know
				temp.pop()
				temp.append(('UH', '2'))
				temp.append(('UH', '2'))
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
	parser.add_argument("file", help="Out file decoded from NCRFpp")
	parser.add_argument("output", help="Output file name")
	parser.add_argument("prefix", help="Prefix of the header")
	args = parser.parse_args()
	main(args)
