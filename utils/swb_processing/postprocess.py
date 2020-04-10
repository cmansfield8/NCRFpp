#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: coman8@uw.edu

This script takes the NCRFpp output and incorporates into alignment file.

-includes 'shapes' or general lexical categories
-detokenizes 

"""

import argparse
import csv
from ast import literal_eval
import pandas as pd


def read_tsv(tsv_file, header=0):
        """Given a tsv file reads and returns as pandas dataframe."""
        df = pd.read_csv(tsv_file, sep='\t', header=header, quotechar="\"")

        # convert strings of lists to lists
        for col_name in df.columns:
                if str(df.iloc[0][col_name]).startswith('[') and \
                   str(df.iloc[0][col_name]).endswith(']'):
                        df[col_name] = df[col_name].apply(lambda x: literal_eval(x))

        return df


def get_shapes(row, prefix, tok_map, tag_map):
	tags = row[prefix + 'tags']
	tokens = row[prefix + 'sentence_dtok']
			
	shapes = list()
	for i in range(len(tags)):
		if tags[i] == None:
			shapes.append(None)
		elif tokens[i] in tok_map.keys():
			shapes.append(tok_map[tokens[i]])
		else:
			try: 
				shapes.append(tag_map[tags[i]])
			except NameError:
				print("Shape not found for tag: {}".format(tags[i]))
				shapes.append('UNK')
	return shapes
	

def read_mapper(file):
	reader = csv.reader(open(file, 'r'), delimiter='\t')
	result = dict()
	for row in reader:
		result[row[0]] = row[1]
	return result

	
def is_sos(current):
	return current[1].startswith("1.0000")


def detokenize(row, prefix):
	tags = row['temp']
	sent_col = prefix + 'sentence'
	tok_ids_col = prefix + 'names'
	
	temp = list()
	tag_ix = 0
	tok_ix = 0
	while tok_ix < len(row[tok_ids_col]):
		label = row[tok_ids_col][tok_ix]
		if label.endswith('_a'):
			# join 'you' 'know' tokens with an underscore
			if row[sent_col][tok_ix] == 'you' and row[sent_col][tok_ix+1] == 'know':
				temp.append('UH')
			# join contractions
			else:
				temp.append(tags[tag_ix])
			tag_ix += 2
			tok_ix += 2
		elif label == 'None':
			tok_ix += 1
		else:
			try:
				temp.append(tags[tag_ix])
			except IndexError as e:
				print('WARNING: list index error!')
				print('tags: {}\ntokens: {}\nnames: {}'.format(temp, row[sent_col], row[tok_ids_col]))
			tag_ix += 1
			tok_ix += 1
	return temp


def read_tags(file):
	reader = csv.reader(open(file, 'r'), delimiter=' ')
	tags = list()
	temp = list()
	for current in reader:
		if not current: # start a new sentence
			tags.append(temp)
			temp = list()
		elif is_sos(current): # skip SOS
			continue
		elif current[0] == '#':	 # empty sentence
			temp.append(None)
		else:
			temp.append(current[1])
	return tags


def main(args):
	try:
		tok_map = read_mapper("tokenshapes.tsv")
		tag_map = read_mapper("tagshapes.tsv")
	except FileNotFoundError as e:
		print("tokenshapes.tsv and tagshapes.tsv file expected in base dir")
		
	if args.ftype == 'ptb':
		prefix = ''
	else:
		prefix = 'ms_'
	
	print('Reading alignments...')
	tags = read_tags(args.file)
	tag_name = prefix + 'tags'
	df = read_tsv(args.alignment)
	
	tags_series = pd.Series(tags)
	tags_series.name = 'temp'
	df = df.join(tags_series)

	print('Detokenizing...')
	df[tag_name] = df.apply(lambda x: detokenize(x, prefix), axis=1)
	
	print('Adding shapes...')
	shape_name = prefix + 'shapes'
	df[shape_name] = df.apply(lambda x: get_shapes(x, prefix, tok_map, tag_map), axis=1)
	
	print('Writing file {}'.format(args.output))
	df = df[['file', 'speaker', 'turn', 'sent_num', tag_name, shape_name]]
	df.to_csv(args.output, sep='\t', index=False)


if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="Out file decoded from NCRFpp")
	parser.add_argument("alignment", help="File with original alignments")
	parser.add_argument("output", help="Output file name")
	parser.add_argument("ftype", help="ptb or ms")
	args = parser.parse_args()
	main(args)