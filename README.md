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
git clone --recursive https://github.com/BPYap/Question-Generation
cd Question-Generation
```
### Step 2: Install dependencies
```
python -m virtualenv env
source env/bin/activate

pip install -r requirements.txt
python setup.py install
```
### Step 3: Download pretrained models
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
Checkpoint without reinforcement learning:
1. Download the pretrained model from this [link](https://storage.googleapis.com/pretrained_models/translate.ckpt-1460356.zip)
2. Decompress and put `translate.ckpt-1460356.data-00000-of-00001`, `translate.ckpt-1460356.index` and `translate.ckpt-1460356.meta` under `model/pretrained/active-qa/translate.ckpt-1460356` directory

Checkpoint with reinforcement learning:
1. Download the pretrained model from this [link](https://storage.cloud.google.com/pretrained_models/translate.ckpt-6156696.zip)
2. Decompress and put `translate.ckpt-6156696.data-00000-of-00001`, `translate.ckpt-6156696.index` and `translate.ckpt-6156696.meta` under `model/pretrained/active-qa/translate.ckpt-6156696` directory

## Usage
### Question Generation
```
python script/generate.py [--method METHOD] [--input_path INPUT_PATH] [--output_path OUTPUT_PATH]

arguments:
  --method       METHOD       Question generation method. Available option: [fpm, symsub, zeroshot, zeroshot-rl, eda]
                            
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
        3. Zero-shot Machine Translation Model
        4. Zero-shot Machine Translation Model (with reinforcement learning)
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

## References
- Mikolov, Tomas, et al. "Advances in pre-training distributed word representations." arXiv preprint arXiv:1712.09405 (2017).
- Pennington, Jeffrey, Richard Socher, and Christopher Manning. "Glove: Global vectors for word representation." Proceedings of the 2014 conference on empirical methods in natural language processing (EMNLP). 2014.
- Cer, Daniel, et al. "Universal sentence encoder." arXiv preprint arXiv:1803.11175 (2018).
- Buck, Christian, et al. "Ask the right questions: Active question reformulation with reinforcement learning." arXiv preprint arXiv:1705.07830 (2017).
- Jin, Zhijing, et al. "Unsupervised Text Style Transfer via Iterative Matching and Translation." arXiv preprint arXiv:1901.11333 (2019).
- Wei, Jason W., and Kai Zou. "Eda: Easy data augmentation techniques for boosting performance on text classification tasks." arXiv preprint arXiv:1901.11196 (2019).
- Klein, Guillaume, et al. "OpenNMT: Neural Machine Translation Toolkit." arXiv preprint arXiv:1805.11462 (2018).
- Miller, George A. WordNet: An electronic lexical database. MIT press, 1998.
