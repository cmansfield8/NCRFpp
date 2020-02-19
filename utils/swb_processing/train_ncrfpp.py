"""Given switchboard pickle file, prints sentences in correct format for NCRFpp training."""

import pickle
from .. import util

def main(args):
	sents = pickle.load(open(args.file, 'rb'))
	with open(args.output, 'w+') as out:
		for sent in sents:
			for tok, pos in sent:
				out.write("{}\t{}\n".format(tok.lower(), pos))
			out.write('\n')
			
if __name__=="__main__":
    parser = argparse.ArgumentParser()
	parser.add_argument("file", help="Switchboard pickle training file")
	parser.add_argument("output", help="Output file name")
    args = parser.parse_args()
    main(args)
