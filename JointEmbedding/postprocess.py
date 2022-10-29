import string
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='github', choices=['github', 'arxiv', 'amazon'])

args = parser.parse_args()
dataset = args.dataset
folder = '../' + dataset + '/'

output = []
with open('vec.dat') as fin, open(folder+'embedding_sph', 'w') as fout:
	for line in tqdm(fin):
		data = line.strip().split()
		if len(data) != 101:
			continue
		if data[0].startswith('$LABL_') or not data[0].startswith('$'):
			output.append(' '.join(data)+'\n')

	fout.write(str(len(output))+'\t100\n')
	for line in output:
		fout.write(line)