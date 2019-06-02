# Question_Generation

### Installing Dependencies
###### 1. Create virtual environment
```
python3 -m virtualenv env
```
###### 2. Activate virtual environment
###### Windows: 
```
env\scripts\activate
```
###### Ubuntu: 
```
source env/bin/activate
```
###### 3. Install dependencies (from requirements.txt)
```
pip install -r requirements.txt
```
###### 4. Clone fastText repository
```
git clone https://github.com/facebookresearch/fastText.git
```
###### 5. Change directory to `fastText`
```
cd fastText
```
###### 6. Install `fastText` package
```
pip install .
```

### Downloading Pretrained Models
##### fastText
1. Download [fastText English vectors](https://fasttext.cc/docs/en/crawl-vectors.html) [[direct link](https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz)]
2. Decompress and put `cc.en.300.bin` inside `model/pretrained/fastText`directory

##### GloVe
1. Download [spaCy pretrained GloVe model](https://spacy.io/models/en#en_vectors_web_lg) [[direct link](https://github.com/explosion/spacy-models/releases/download/en_vectors_web_lg-2.1.0/en_vectors_web_lg-2.1.0.tar.gz)]
2. Decompress and put `en_vectors_web_lg-2.1.0` (the most inner folder) under `model/pretrained/spacy_glove` directory

##### Universal Sentence Encoder
1. Download the [transformer variant of Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder-large/3) [[direct link](https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed)]
2. Decompress and put `assets`, `variables`, `saved_model.pb` and `tfhub_module.pb` under `model/pretrained/universal_sentence_encoder` directory
