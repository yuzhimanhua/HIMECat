#!/bin/sh

unzip eigen-3.3.3.zip
make

dataset="github"
# sample: number of training samples (Million); sample=1000 for github, sample=2000 for arxiv, sample=5000 for amazon
sample=1000
# type: number of edge types; type=5 for github and amazon, type=4 for arxiv
type=5

threads=4 # number of threads for training
negative=5 # number of negative samples
alpha=0.04 # initial learning rate
dim=100

prep_script="preprocess_${dataset}.py"
word_file="${dataset}/left.dat"
node_file="${dataset}/right.dat"
link_file="${dataset}/link.dat"
emb_file="vec.dat"

echo Preprocessing...
python ${prep_script}

echo Embedding Learning...
./bin/jointemb -words ${word_file} -nodes ${node_file} -hin ${link_file} -output ${emb_file} -binary 0 -type ${type} -size ${dim} -negative ${negative} -samples ${sample} -alpha ${alpha} -threads ${threads}

echo Postprocessing...
python postprocess.py