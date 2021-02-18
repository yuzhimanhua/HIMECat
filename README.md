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
To reproduce the results in our paper, you need to first download the [**datasets**](https://drive.google.com/file/d/170Vm8LywO0jDpwjNnPIzIj2kuCClZ21k/view?usp=sharing). Three datasets are used in our paper: **GitHub**, **ArXiv**, and **Amazon**. Once you unzip the downloaded file (i.e., ```data.zip```), you can see three folders related to these three datasets, respectively. 

| Dataset | #Documents | #Layers | #Classes (including ROOT) | #Leaves | Sample Classes |
| ------- |------------| ------- | ------------------------- | ------- | -------------- |
| [GitHub](https://github.com/yuzhimanhua/HiGitClass)        | 1,596      | 2       | 18                        | 14      | Computer Vision (Layer-1), Image Generation (Layer-2)|
| ArXiv                                                      | 26,400     | 2       | 94                        | 88      | cs (Layer-1), cs.AI (Layer-2)|
| [Amazon](http://jmcauley.ucsd.edu/data/amazon/index.html)  | 147,000    | 2       | 166                       | 147     | Automotive (Layer-1), Car Care (Layer-2)|

You need to put these 3 folders under the main folder ```./```. Then the following running script can be used to run the model.

```
./test.sh
```

Level-1/Level-2/Overall Micro-F1/Macro-F1 scores will be shown in the last several lines of the output. The classification result can be found under your dataset folder. For example, if you are using the GitHub dataset, the output will be ```./github/out.txt```.

## Data
In each of the three folders (i.e., ```github/```, ```arxiv/```, and ```amazon/```), there is a json file, where each line represents one document with text and metadata information.

For GitHub, the json format is
```
{
  "id": "Natsu6767/DCGAN-PyTorch",  
  "user": [
    "Natsu6767"
  ],
  "text": "pytorch implementation of dcgan trained on the celeba dataset deep convolutional gan ...",
  "tags": [
    "pytorch",
    "dcgan",
    "gan",
    "implementation",
    "deeplearning",
    "computer-vision",
    "generative-model"
  ],
  "labels": [
    "$Computer-Vision",
    "$Image-Generation"
  ]
}
```
The "user" and "tags" fields are metadata.

For ArXiv, the json format is
```
{
  "id": "1001.0063",
  "authors": [
    "Alessandro Epasto",
    "Enrico Nardelli"
  ],
  "text": "on a model for integrated information in this paper we give a thorough presentation of a model ...",
  "labels": [
    "cs",
    "cs.AI"
  ]
}
```
The "authors" field is metadata.

For Amazon, the json format is
```
{
  "user": [
    "A39IXH6I0WT6TK"
  ],
  "product": [
    "B004DLPXAO"
  ],
  "text": "works really great only had a problem when it was updated but they fixed it right away ...",
  "labels": [
    "Apps-for-Android",
    "Books-&-Comics"
  ]
}
```
The "user" and "product" fields are metadata.

**NOTE 1: If you would like to run our code on your own dataset, when you prepare this json file, make sure that: (1) You list the labels in the top-down order. For example, if the label path of your repository is ROOT-A-B-C, then the "labels" field should be \["A", "B", "C"\]. (2) For each document, its metadata field is always represented by a list. For example, the "user" field should be \["A39IXH6I0WT6TK"\] instead of "A39IXH6I0WT6TK".**

## Running New Datasets
In the Quick Start section, we include a pretrained embedding file in the downloaded folders. If you would like to re-train the embedding (or **you have a new dataset**), please follow the steps below.

1. Create a directory named ```${dataset}``` under the main folder (e.g., ```./github```).

2. Prepare four files:             
(1) ```./${dataset}/label_hier.txt``` indicating the parent children relationships between classes. The first class of each line is the parent class, followed by all its children classes. Whitespace is used as the delimiter. **The root class must be named as ROOT. Make sure your class names do not contain whitespace.**           
(2) ```./${dataset}/doc_id.txt``` containing labeled document ids for each class. Each line begins with the class name, and then document ids in the corpus (starting from ```0```) of the corresponding class separated by whitespace.           
(3) ```./${dataset}/${json-name}.json```. **You can refer to the provided json format above. Make sure it has two fields "text" and "labels". You can add your own metadata fields in the json.**             
(4) ```./${dataset}/meta_dict.json``` indicating the names of your metadata fields. For example, for GitHub, it should be
```
{"metadata": ["user", "tags"]}
```
For ArXiv, it should be
```
{"metadata": ["authors"]}
```

3. Install the dependencies [GSL](https://www.gnu.org/software/gsl/) and [Eigen](http://eigen.tuxfamily.org/index.php?title=Main_Page). For Eigen, we already provide a zip file ```JointEmbedding/eigen-3.3.3.zip```. You can directly unzip it in ```JointEmbedding/```.

4. ```./prep_emb.sh```. Make sure you change the dataset/json names. The embedding file will be saved to ```./${dataset}/embedding_sph```.

After that, you can train the classifier as mentioned in Quick Start (i.e., ```./test.sh```).
Please always refer to the example datasets when adapting the code for a new dataset.

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
