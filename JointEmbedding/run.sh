#!/bin/sh

# unzip eigen-3.3.3.zip
# make

threads=4 # number of threads for training
negative=5 # number of negative samples
alpha=0.04 # initial learning rate
dim=100
type=4
sample=$1

word_file="left.dat"
node_file="right.dat"
link_file="link.dat"
emb_file="vec.dat"

./bin/jointemb -words ${word_file} -nodes ${node_file} -hin ${link_file} -output ${emb_file} -binary 0 -type ${type} -size ${dim} -negative ${negative} -samples ${sample} -alpha ${alpha} -threads ${threads}
