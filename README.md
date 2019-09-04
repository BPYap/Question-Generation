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
### Question Generation
```
python script/generate.py [--method METHOD] [--input_path INPUT_PATH] [--output_path OUTPUT_PATH]

arguments:
  --method       METHOD       Question generation method. Available option: [fpm,
                              symsub, imt, zeroshot, eda]
                            
  --input_path   INPUT_PATH   Path to input file in plain text, each question is
                              separated by newline
                            
  --output_path  OUTPUT_PATH  Path to output file in json format, each question maps 
                              to a list of generated questions
```

### Interactive Demo
```
python script/generation_demo.py
```

Example output:
```
Initializing...
...
...
...
Enter a sentence/question: menu
Choose a generation method:
        1. Rule-based Pattern Matching
        2. Sense-disambiguated Synonym Substitution
        3. IMT Style Transfer Model
        4. Zero-shot Machine Translation Model
        5. Easy Data Augmentation (EDA)
> 2
Enter a sentence/question: Is it compulsory to attend lecture?

Generated questions:
1. Is it compulsory to attend lecture ?
2. Is it compulsory to attend public lecture ?
3. Is it compulsory to attend talk ?
4. Is it compulsory to go to lecture ?
5. Is it compulsory to go to public lecture ?
6. Is it compulsory to go to talk ?
7. Is it mandatory to attend lecture ?
8. Is it mandatory to attend public lecture ?
9. Is it mandatory to attend talk ?
10. Is it mandatory to go to lecture ?
11. Is it mandatory to go to public lecture ?
12. Is it mandatory to go to talk ?
13. Is it required to attend lecture ?
14. Is it required to attend public lecture ?
15. Is it required to attend talk ?
16. Is it required to go to lecture ?
17. Is it required to go to public lecture ?
18. Is it required to go to talk ?
====================================================================================================
```

### Training text style transfer model via Iterative Matching and Translation (IMT)
```
python script/imt_train.py CONFIG

argument:
  CONFIG path to config file (e.g.: config/experiments/sample.yml)
```

#### Configuration file
This script reads all configuration settings from a single yaml file. To get started, copy the provided `sample.yml` file in `config/experiments/` folder and modify the value of each parameter accordingly. Each parameter (other than the general configurations) is prefixed by the name of pipeline component that utilizes it. For example, `bootstrap_corpus-sentence_encoder` indicates parameter `sentence_encoder` is used by the `bootstrap_corpus` pipeline.

There are in total 6 types of configuration parameter:
##### general
 - `src_corpus`: Path to unaligned source corpus.
 - `tgt_corpus`: Path to unaligned target corpus.
 - `min_update_rate`: Convergence criteria. The iterative process stops when the overall update rate of the newly generated pseudo-parallel corpus is lower than this value.
 
##### bootstrap_corpus
 - `sentence_encoder`: Type of sentence encoder. Choose between "fasttext" (Average fastText embedding), "glove" (Average GloVe embedding) or "use" (Universal Sentence Encoder).
 - `similarity_threshold`: Threshold for cosine similarity score when matching source sentence and target sentence. Source-target pair whose cosine similarity score is lower than this threshold value is discarded.

##### prepare_dataset
 - `validation_ratio`: Ratio to split for validation set.
 - `test_ratio`: Ratio to split for test set.
 
##### preprocess
 - Refer to http://opennmt.net/OpenNMT-py/options/preprocess.html
 
##### train
 - Refer to http://opennmt.net/OpenNMT-py/options/train.html
 
##### translate
 - Refer to http://opennmt.net/OpenNMT-py/options/translate.html

## References
- Mikolov, Tomas, et al. "Advances in pre-training distributed word representations." arXiv preprint arXiv:1712.09405 (2017).
- Pennington, Jeffrey, Richard Socher, and Christopher Manning. "Glove: Global vectors for word representation." Proceedings of the 2014 conference on empirical methods in natural language processing (EMNLP). 2014.
- Cer, Daniel, et al. "Universal sentence encoder." arXiv preprint arXiv:1803.11175 (2018).
- Buck, Christian, et al. "Ask the right questions: Active question reformulation with reinforcement learning." arXiv preprint arXiv:1705.07830 (2017).
- Jin, Zhijing, et al. "Unsupervised Text Style Transfer via Iterative Matching and Translation." arXiv preprint arXiv:1901.11333 (2019).
- Wei, Jason W., and Kai Zou. "Eda: Easy data augmentation techniques for boosting performance on text classification tasks." arXiv preprint arXiv:1901.11196 (2019).
- Klein, Guillaume, et al. "OpenNMT: Neural Machine Translation Toolkit." arXiv preprint arXiv:1805.11462 (2018).
- Miller, George A. WordNet: An electronic lexical database. MIT press, 1998.