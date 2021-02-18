import string
import json
from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='github', choices=['github', 'arxiv', 'amazon'])
parser.add_argument('--json_name', default='GitHub.json')

args = parser.parse_args()
dataset = args.dataset
json_name = args.json_name

folder = '../' + dataset + '/'
lengths = {'github': 1000, 'arxiv': 300, 'amazon': 300}
if dataset in lengths:
	length = lengths[dataset]
else:
	length = 300

thrs = 10
cnt = defaultdict(int)
with open(folder+json_name) as fin:
	for line in fin:
		js = json.loads(line)
		text = js['text'].split()
		for token in text[:length]:
			cnt[token] += 1

parent_label = dict()
with open(folder+'label_hier.txt') as fin:
	for line in fin:
		data = line.strip().split()
		for label in data[1:]:
			parent_label[label] = data[0]

with open(folder+'/meta_dict.json') as fin:
	meta_dict = json.load(fin)
	meta_set = set(meta_dict['metadata'])

with open('link.dat', 'w') as fout, open('left.dat', 'w') as fou1, open('right.dat', 'w') as fou2:
	left = set()
	right = set()

	# Lc-Lp
	for label in parent_label:
		Lc = '$LABL_'+label
		Lp = '$LABL_'+parent_label[label]

		fout.write(Lc+' '+Lp+' 0 1 \n')
		left.add(Lc)
		right.add(Lp)

	# Lc-D
	with open(folder+'doc_id.txt') as fin:
		for line in fin:
			data = line.strip().split()
			L = '$LABL_'+data[0]
			for doc in data[1:]:
				D = '$DOCU_'+doc
				fout.write(L+' '+D+' 1 1 \n')
				left.add(L)
				right.add(D)

	with open(folder+json_name) as fin:
		for idx, line in enumerate(fin):
			js = json.loads(line)
			D = '$DOCU_'+str(idx)
			right.add(D)

			# M-D
			for meta in meta_set:
				for x in js[meta]:
					M = '$'+meta.upper()+'_'+x.replace(' ', '_')
					fout.write(M+' '+D+' 2 1 \n')
					left.add(M)

			# W-D
			wd = defaultdict(int)
			text = []
			for token in js['text'].split()[:length]:
				if cnt[token] >= thrs:
					text.append(token)
					left.add(token)	

			for W in text:
				wd[W+' '+D] += 1
			for tup in wd:
				fout.write(tup+' 3 '+str(wd[tup])+'\n')

	for x in left:
		fou1.write(x+'\n')
	for x in right:
		fou2.write(x+'\n')
