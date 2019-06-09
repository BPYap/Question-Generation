# Question_Generation

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
```
### Step 4: Download pretrained models
##### fastText
1. Download [fastText English vectors](https://fasttext.cc/docs/en/crawl-vectors.html) [[direct link](https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz)]
2. Decompress and put `cc.en.300.bin` under `model/pretrained/fastText`directory
##### GloVe
1. Download [spaCy pretrained GloVe model](https://spacy.io/models/en#en_vectors_web_lg) [[direct link](https://github.com/explosion/spacy-models/releases/download/en_vectors_web_lg-2.1.0/en_vectors_web_lg-2.1.0.tar.gz)]
2. Decompress and put `en_vectors_web_lg-2.1.0` (the most inner folder) under `model/pretrained/spacy_glove` directory
##### Universal Sentence Encoder
1. Download the [transformer variant of Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder-large/3) [[direct link](https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed)]
2. Decompress and put `assets`, `variables`, `saved_model.pb` and `tfhub_module.pb` under `model/pretrained/universal_sentence_encoder` directory
### Step 5: Install OpenNMT toolkit for PyTorch
Change to the root directory `Question-Generation/` then follow the instructions at this [link](http://opennmt.net/OpenNMT-py/main.html#installation).
