dataset=github
sup_source=docs
embedding=sph

python main.py --dataset ${dataset} --sup_source ${sup_source} --block_level 2 --embedding ${embedding} --beta 500

python eval.py --dataset ${dataset}