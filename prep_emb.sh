dataset=github
json_name=GitHub.json
sample=1000 # number of training samples in embedding; sample=1000 for github; sample=2000 for arxiv; sample=5000 for amazon

echo Data Preprocessing ...
python data_preprocess.py --dataset ${dataset} --json_name ${json_name}

cd JointEmbedding/

echo Embedding Preprocessing ...
python preprocess.py --dataset ${dataset} --json_name ${json_name}

echo Embedding Learning ...
./run.sh ${sample}

echo Embedding Postprocessing ...
python postprocess.py --dataset ${dataset}

cd ../
