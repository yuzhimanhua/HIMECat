from collections import defaultdict
import json

dataset = 'github'
length = 1500
thrs = 5

cnt = dict()
parent_label = dict()
with open('../'+dataset+'/GitHub.json') as fin:
	for idx, line in enumerate(fin):
		js = json.loads(line)

		text = js['text'].lower().split()
		for token in text[:length]:
			if token not in cnt or len(token) >= 50:
				cnt[token] = 0
			cnt[token] += 1

		if js['super_label'] not in parent_label:
			parent_label[js['super_label']] = 'ROOT'
		if js['sub_label'] not in parent_label:
			parent_label[js['sub_label']] = js['super_label']

with open(dataset+'/link.dat', 'w') as fout, open(dataset+'/left.dat', 'w') as fou1, open(dataset+'/right.dat', 'w') as fou2:
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
	with open('../'+dataset+'/doc_id.txt') as fin:
		for line in fin:
			data = line.strip().split()
			L = '$LABL_'+data[0]
			for doc in data[1:]:
				D = '$DOCU_'+doc
				fout.write(L+' '+D+' 1 1 \n')
				left.add(L)
				right.add(D)

	with open('../'+dataset+'/GitHub.json') as fin:
		for idx, line in enumerate(fin):
			js = json.loads(line)
			D = '$DOCU_'+str(idx)
			right.add(D)

			# U-D
			U = '$USER_'+js['user']
			fout.write(U+' '+D+' 2 1 \n')
			left.add(U)

			# T-D
			for tag in js['tags']:
				T = '$TAGS_'+tag
				fout.write(T+' '+D+' 3 1 \n')
				left.add(T)
			
			wd = defaultdict(int)
			text = []
			for token in js['text'].lower().split()[:length]:
				if cnt[token] >= thrs:
					text.append(token)
					left.add(token)
			
			# W-D
			for W in text:
				wd[W+' '+D] += 1
			for tup in wd:
				fout.write(tup+' 4 '+str(wd[tup])+'\n')

	for x in left:
		fou1.write(x+'\n')
	for x in right:
		fou2.write(x+'\n')
