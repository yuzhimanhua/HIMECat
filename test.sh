dataset=github
embedding=sph

python main.py --dataset ${dataset} --embedding ${embedding}

python eval.py --dataset ${dataset}