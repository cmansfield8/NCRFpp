"""Given switchboard pickle file, prints sentences in correct format for NCRFpp training."""

import pickle
from .. import util

def swb_to_ncrfpp(source, output):
	sents = pickle.load(open(source, 'rb'))
	with open(output, 'w+') as out:
		for sent in sents:
			for tok, pos in sent:
				out.write("{}\t{}\n".format(tok.lower(), pos))
			out.write('\n')
