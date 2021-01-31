# The code structure is adapted from the WeSHClass implementation
# https://github.com/yumeng5/WeSHClass

import numpy as np
np.random.seed(1234)
from time import time
from models import WSTC
from load_data import load_dataset
from utils import proceed_level, write_output

import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ['CUDA_VISIBLE_DEVICES'] = '0'

if __name__ == "__main__":

	import argparse

	parser = argparse.ArgumentParser(description='main',
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	
	### Basic settings ###
	
	# dataset selection: github (default), arxiv, or amazon
	parser.add_argument('--dataset', default='github', choices=['github', 'arxiv', 'amazon'])
	# weak supervision selection: labeled documents
	parser.add_argument('--sup_source', default='docs', choices=['docs'])
	# the class tree level to proceed until: None (default) = maximum possible level
	parser.add_argument('--max_level', default=None, type=int)
	# the highest class tree level that documents can be assigned to: 1 (default)
	parser.add_argument('--block_level', default=1, type=int)
	# whether ground truth labels are available for evaluation: All (default, all documents have ground truth for evaluation) or None (no ground truth)
	parser.add_argument('--with_eval', default='All', choices=['All', 'None'])
	
	### Training settings ###

	# mini-batch size for both pre-training and self-training: 256 (default)
	parser.add_argument('--batch_size', default=256, type=int)
	# pre-training epochs: None (default)
	parser.add_argument('--pretrain_epochs', default=None, type=int)
	# pseudo document generation method: bow (Bag-of-words, default)
	parser.add_argument('--pseudo', default='bow', choices=['bow'])

	### Hyperparameters settings ###

	# background word distribution weight (alpha): 0 (default)
	parser.add_argument('--alpha', default=0, type=float)
	# number of generated pseudo documents per class (beta): 500 (default)
	parser.add_argument('--beta', default=500, type=int)
	# self-training stopping criterion (delta): 0.1 (default)
	parser.add_argument('--delta', default=0.1, type=float)
	# normalized entropy threshold for blocking: 1.0 (default)
	parser.add_argument('--gamma', default=0.9, type=float)
	# pretrained embedding name: Joint Spherical (default)
	parser.add_argument('--embedding', default='sph')
	
	args = parser.parse_args()
	print(args)

	alpha = args.alpha
	beta = args.beta
	delta = args.delta

	word_embedding_dim = 100
	
	if args.dataset == 'github':
		pretrain_epochs = 30
		max_doc_length = 1500
		max_sent_length = 40
		common_words = 10000
		kappa = 150

	elif args.dataset == 'arxiv':		
		pretrain_epochs = 30
		max_doc_length = 300
		max_sent_length = 40
		common_words = 10000
		kappa = 150

	elif args.dataset == 'amazon':		
		pretrain_epochs = 30
		max_doc_length = 300
		max_sent_length = 40
		common_words = 10000
		kappa = 150

	decay = 1e-6
	update_interval = 2
	self_lr = 0

	if args.sup_source == 'docs':
		expand_num = 0
	else:
		expand_num = None
		
	if args.pretrain_epochs is not None:
		pretrain_epochs = args.pretrain_epochs
	
	x, y, sequences, class_tree, word_counts, vocabulary, vocabulary_inv_list, len_avg, len_std, perm = \
		load_dataset(args.dataset, sup_source=args.sup_source, common_words=common_words, 
					truncate_doc_len=max_doc_length, truncate_sent_len=max_sent_length, with_eval=args.with_eval)
	
	assert max_doc_length > len_avg, f"max_doc_length should be greater than {len_avg}"

	np.random.seed(1234)
	vocabulary_inv = {key: value for key, value in enumerate(vocabulary_inv_list)}
	vocab_sz = len(vocabulary_inv)

	print(f'x shape: {x.shape}')
	
	if args.max_level is None:
		max_level = class_tree.get_height()
	else:
		max_level = args.max_level

	wstc = WSTC(input_shape=x.shape, class_tree=class_tree, max_level=max_level, sup_source=args.sup_source, y=y,
				vocab_sz=vocab_sz, word_embedding_dim=word_embedding_dim, block_thre=args.gamma, block_level=args.block_level)

	total_counts = sum(word_counts[ele] for ele in word_counts)
	total_counts -= word_counts[vocabulary_inv_list[0]]
	background_array = np.zeros(vocab_sz)
	for i in range(1,vocab_sz):
		background_array[i] = word_counts[vocabulary_inv[i]]/total_counts

	for level in range(max_level):
		y_pred = proceed_level(x, sequences, wstc, args, pretrain_epochs, self_lr, decay, update_interval,
								delta, class_tree, level, expand_num, background_array, max_doc_length, max_sent_length,
								len_avg, len_std, beta, alpha, vocabulary_inv, common_words, kappa, word_embedding_dim)
	write_output(y_pred, perm, class_tree, './' + args.dataset)
