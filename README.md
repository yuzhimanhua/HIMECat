# Hierarchical Metadata-Aware Document Categorization under Weak Supervision
This project provides a weakly supervised framework for hierarchical metadata-aware document categorization.

## Installation
For training, a GPU is strongly recommended.

### Keras
The code is based on Keras. You can find installation instructions [**here**](https://keras.io/#installation).

### Dependency
The code is written in Python 3.6. The dependencies are summarized in the file ```requirements.txt```. You can install them like this:

```
pip3 install -r requirements.txt
```

## Quick Start
To reproduce the results in our paper, you need to first download the [**datasets**](https://drive.google.com/file/d/170Vm8LywO0jDpwjNnPIzIj2kuCClZ21k/view?usp=sharing). Three datasets are used in our paper: **GitHub** ([Zhang et al., 2019](https://arxiv.org/abs/1910.07115)), **ArXiv**, and **Amazon** ([McAuley and Leskovec, 2013](https://dl.acm.org/doi/10.1145/2507157.2507163)). Once you unzip the downloaded file (i.e., ```data.zip```), you can see three folders related to these three datasets, respectively. 

| Dataset | #Documents | #Layers | #Classes (including ROOT) | #Leaves | Sample Classes |
| ------- |------------| ------- | ------------------------- | ------- | -------------- |
| GitHub  | 1,596      | 2       | 18                        | 14      | Computer Vision (Layer-1), Image Generation (Layer-2)|
| ArXiv   | 26,400     | 2       | 94                        | 88      | cs (Layer-1), cs.AI (Layer-2)|
| Amazon  | 147,000    | 2       | 166                       | 147     | Automotive (Layer-1), Car Care (Layer-2)|

You need to put these 3 folders under the main folder ```./```. Then the following running script can be used to run the model.

```
./test.sh
```

Level-1/Level-2/Overall Micro-F1/Macro-F1 scores will be shown in the last several lines of the output. The classification result can be found under your dataset folder. For example, if you are using the GitHub dataset, the output will be ```./github/out.txt```.

## Data
In each of the three folders (i.e., ```github/```, ```arxiv```, and ```amazon```), there is a json file, where each line represents one document with text and metadata information.

For GitHub, the json format is
```
{
  "user": "Natsu6767",
  "text": "PyTorch Implementation of DCGAN trained on the CelebA dataset . # Deep Convolutional GAN ...",
  "tags": [
    "pytorch",
    "dcgan",
    "gan",
    "implementation",
    "deeplearning",
    "computer-vision",
    "generative-model"
  ],
  "super_label": "$Computer-Vision",
  "sub_label": "$Image-Generation",
  "repo_name": "Natsu6767/DCGAN-PyTorch"
}
```
The "repo_name" field is not used by our algorithm.

For ArXiv, the json format is
```
{
  "url": "http://arxiv.org/abs/1001.0063",
  "authors": [
    "Alessandro Epasto",
    "Enrico Nardelli"
  ],
  "text": "on a model for integrated information in this paper we give a thorough presentation of a model proposed by tononi et al . ...",
  "sub_label": "cs.AI",
  "super_label": "cs"
}
```
The "url" field is not used by our algorithm.

For Amazon, the json format is
```
{
  "overall": 5.0,
  "text": "works really great . only had a problem when it was updated , but they fixed it right away.just love it!very user friendly .",
  "super_label": "Apps-for-Android",
  "sub_label": "Books-&-Comics",
  "user": "A39IXH6I0WT6TK",
  "product": "B004DLPXAO"
}
```
The "overall" field is not used by our algorithm.

## Running on New Datasets
TODO.

WARNING: Currently, the code only works for 2-layer hierarchies.

## Citation
If you find the implementation useful, please cite the following paper:
```
@inproceedings{zhang2021hierarchical,
  title={Hierarchical Metadata-Aware Document Categorization under Weak Supervision},
  author={Zhang, Yu and Chen, Xiusi and Meng, Yu and Han, Jiawei},
  booktitle={WSDM'21},
  year={2021},
  organization={ACM}
}
```
