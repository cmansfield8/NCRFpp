#! /usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: coman8@uw.edu

This script takes the switchboard file and does preprocessing so it can be read by NCRFpp.

1. Empty sentences are converted to "#" so we don't lose track when they need to be zipped back in to the alignment file.
2. Sentences are printed word by word with a newline inbetween.
3. Label is added to column 2 (required by NCRFpp decoder).

"""


import argparse
import csv
from ast import literal_eval
import pandas as pd


def write_file(sentences, output, label):
	sentences = [literal_eval(x) for x in sentences]
	writer = csv.writer(open(output, 'w'), delimiter='\t', lineterminator="\n")
	for sent in sentences:
		if not sent:
			writer.writerow(["#", label])
		else:
			for token in sent:
				writer.writerow([token, label])
		writer.writerow("")
		
def main(args):
	LABEL = 'SYM'
	
	df = pd.read_csv(args.file, delimiter='\t')
	
	ptb_out = args.output + "_ptb.txt"
	write_file(df['sentence'].tolist(), ptb_out, LABEL)
	
	ms_out = args.output + "_ms.txt"
	write_file(df['ms_sentence'].tolist(), ms_out, LABEL)


if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("file", help="Switchboard file")
	parser.add_argument("output", help="Output file prefix")
	args = parser.parse_args()
	main(args)
