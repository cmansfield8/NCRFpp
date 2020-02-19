#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: coman8@uw.edu

This script takes the NCRFpp output and postprocesses.
1. Removes contractions
2. Adds function/content/other categories along with POS tags
3. Outputs 1 sentence per line
"""

import argparse
import csv


def get_shape(token, tag, tok_map, tag_map):
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


def main(args):
	tok_map = read_mapper("tokenshapes.tsv")
	tag_map = read_mapper("tagshapes.tsv")
	
	sentences = list()
	temp = list()

	reader = csv.reader(open(args.file, 'r'), delimiter=' ')
	for row in reader:
		if not row: # start a new sentence
			sentences.append(list(map(list, zip(*temp))))
			temp = list()
		elif row[0].startswith("\'"): # skip contractions
			continue
		elif row[1].startswith("1.0000"): # SOS
			continue
		else:
			shape = get_shape(row[0], row[1], tok_map, tag_map)
			temp.append((row[1], shape))
	
	writer = csv.writer(open(args.output, 'w'), delimiter='\t')
	writer.writerow([args.prefix+'_tags', args.prefix+'_shapes'])
	for tags, shapes in sentences:
		writer.writerow([tags, shapes])


if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="File decoded from NCRFpp")
	parser.add_argument("output", help="Output file name")
	parser.add_argument("prefix", help="Prefix of the header")
	args = parser.parse_args()
	main(args)
