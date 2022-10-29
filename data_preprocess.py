import json
import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='github', choices=['github', 'arxiv', 'amazon'])
parser.add_argument('--json_name', default='GitHub.json')

args = parser.parse_args()
dataset = args.dataset
json_name = args.json_name

with open(f'{dataset}/{json_name}') as fin, open(f'{dataset}/dataset.txt', 'w') as fou1, open(f'{dataset}/labels.txt', 'w') as fou2:
	for line in fin:
		data = json.loads(line)
		fou1.write(data['text'] + '\n')
		fou2.write(data['labels'][-1] + '\n')
