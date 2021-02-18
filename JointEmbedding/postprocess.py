import string
import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='github', choices=['github', 'arxiv', 'amazon'])

args = parser.parse_args()
dataset = args.dataset
folder = '../' + dataset + '/'

output = []
with open('vec.dat') as fin, open(folder+'embedding_sph', 'w') as fout:
	for line in fin:
		tmp = line.strip().split()
		if len(tmp) != 101:
			continue
		if tmp[0].startswith('$LABL_') or not tmp[0].startswith('$'):
			output.append(' '.join(tmp)+'\n')

	fout.write(str(len(output))+'\t100\n')
	for line in output:
		fout.write(line)