#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
This script takes the NCRFpp output and postprocesses.
1. Removes contractions
2. Adds broad lexical categories along with POS tags
3. Outputs 1 sentence per line
"""

import argparse
import csv


def get_shape(token, tag, tok_map, tag_map):
    if token in tok_map.keys():
        return tok_map[token]
    else:
        try:
            tag_map[tag]
        except KeyError:
            print("Tag not found in tag mapper: {}".format(tag))
            result.append('UNK')
    return result
	
def read_mapper(file):
    reader = csv.reader(open(file, 'r'), delimiter='\t')
    result = dict()
    for row in reader:
        result[row[0]] = row[1]
    return result


def main(file, tagshapes, tokenshapes, output):
	tok_map = read_mapper(tokenshapes)
	tag_map = read_mapper(tagshapes)
	
	sentences = list()
	temp = list()

	reader = csv.reader(open(file, 'r', delimiter='\t')
	for row in reader:
		if row[0].startswith("#"):
			# skip scores from the model
			continue
		elif row[0].startswith("\'"):
			#skip contractions 
			continue
		elif len(row) == 0: # empty line?
			sentences.append(list(zip(*temp)))
			temp = list()
		else:
			shape = get_shape(row[0], row[1])
			temp.append((row[1], shape))
	
	output = file[:-4] + "_post" + file[-4:]
	writer = csv.writer(open(output, 'w', delimiter='\t')
	for line in sentences:
		writer.writerow(line)


if __name__=="__main__":
    parser = argparse.ArgumentParser()
	parser.add_argument("file", help="Output file from NCRFpp")
    parser.add_argument("tagshapes", help="List of tags with lexical class labels")
	parser.add_argument("tokenshapes", help="List of words with lexical class labels")
    args = parser.parse_args()
    main(args.file, args.tagshapes, args.wordshapes)
