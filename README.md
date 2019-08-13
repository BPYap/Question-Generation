# Question_Generation

##### Table of Contents  
[Introduction](#introduction)  
[Installation](#installation)  
[Usage](#usage) 

## Introduction
[To be added]

## Installation
### Step 1: Clone the repository
```
git clone https://github.com/BPYap/Question-Generation
cd Question-Generation
```
### Step 2 (Optional): Setup virtual environment
Windows:
```
python3 -m virtualenv env
env\scripts\activate
```
Ubuntu:
```
python3 -m virtualenv env
source env/bin/activate
```
### Step 3: Install dependencies
```
pip install -r requirements.txt
python setup.py install
```
### Step 4: Download pretrained models
##### fastText
1. Download [fastText English vectors](https://fasttext.cc/docs/en/crawl-vectors.html) [[direct link](https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz)]
2. Decompress and put `cc.en.300.bin` under `model/pretrained/fastText` directory
##### GloVe
1. Download [spaCy pretrained GloVe model](https://spacy.io/models/en#en_vectors_web_lg) [[direct link](https://github.com/explosion/spacy-models/releases/download/en_vectors_web_lg-2.1.0/en_vectors_web_lg-2.1.0.tar.gz)]
2. Decompress and put `en_vectors_web_lg-2.1.0` (the most nested folder) under `model/pretrained/spacy_glove` directory
##### Universal Sentence Encoder
1. Download the [transformer variant of Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder-large/3) [[direct link](https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed)]
2. Decompress and put `assets`, `variables`, `saved_model.pb` and `tfhub_module.pb` under `model/pretrained/universal_sentence_encoder` directory
##### ActiveQA Question Reformulator (pretrained on UN+Paralex datasets)
1. Download the pretrained model from this [link](https://storage.googleapis.com/pretrained_models/translate.ckpt-1460356.zip)
2. Decompress and put `translate.ckpt-1460356.data-00000-of-00001`, `translate.ckpt-1460356.index` and `translate.ckpt-1460356.meta` under `model/pretrained/active-qa/translate.ckpt-1460356` directory
### Step 5: Download OpenNMT toolkit for PyTorch
Change to the root directory `Question-Generation/` and follow the instructions at this [link](http://opennmt.net/OpenNMT-py/main.html#installation).

## Usage
### Iterative Matching and Translation
To execute the Iterative Matching and Translation (IMT) pipeline:
```
python imt.py config_file_path
```

#### Configuration file
This script reads all configuration settings from a single yaml file. To get started, copy the provided `sample.yml` file in `config/experiments/` folder and modify the value of each parameter accordingly. Each parameter (other than the general configurations) is prefixed by the name of pipeline component that consumes it. For example, `bootstrap_corpus-sentence_encoder` indicates parameter `sentence_encoder` is consumed by the `bootstrap_corpus` pipeline.

There are in total 6 types of configuration parameter:
##### general
 - `src_corpus`: Path to unaligned source corpus.
 - `tgt_corpus`: Path to unaligned target corpus.
 - `min_update_rate`: Convergence criteria. The iterative process stops when the overall update rate of the newly generated pseudo-parallel corpus is lower than this value.
 
##### bootstrap_corpus
 - `sentence_encoder`: Type of sentence encoder. Choose between "fasttext" (Average fastText embedding), "glove" (Average GloVe embedding) or "use" (Universal Sentence Encoder).
 - `similarity_threshold`: Threshold for cosine similarity score when matching source sentence and target sentence. Source-target pair whose cosine similarity score is lower than this threshold value is discarded.

##### prepare_dataset
 - `validation_ratio`: Ratio of validation set when splitting data set for OpenNMT training.
 - `test_ratio`: Ratio of test set when splitting data set for OpenNMT training.
 
##### preprocess
 - Refer to http://opennmt.net/OpenNMT-py/options/preprocess.html
 
##### train
 - Refer to http://opennmt.net/OpenNMT-py/options/train.html
 
##### translate
 - Refer to http://opennmt.net/OpenNMT-py/options/translate.html
 
### Demo Script
[To be added]

## Acknowledgement/References
[To be added]