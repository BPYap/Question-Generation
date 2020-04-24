# Question Generation for Text Augmentation

## Table of Contents  
- [Introduction](#introduction)  
- [Installation](#installation)  
- [Usage](#usage) 

## Introduction
This repository provides a command-line application written in Python for generating multiple variations of questions (both syntactically or/and lexically) from an input question using a combination of rule-based and statistical methods. The generated questions can then be used as additional training data for training question answering models, which can be very useful when training data is small and limited.

The question generation engine includes 3 question generation modes:
- **Rule-based Pattern Matching**. Generate questions with different syntactic structures using hand-crafted question templates.
- **Sense-disambiguated synonyms substitution**. Generates questions with different lexical structures using sense-disambiguated synonoyms.
- **Hybrid Mode**. Combination of the previous 2 methods to generate questions with different syntactic and lexical structures.

For comparison sake, we also implement an interface to the following text generation methods from other researches:
- **Zero-shot Neural Machine Translation** ([Buck et al., 2017](https://arxiv.org/abs/1705.07830)). Questions reformulator based on zero-shot neural machine translation. (GitHub link: https://github.com/google/active-qa)
- **Easy Data Augmentation (EDA)** ([Wei et al., 2019](https://arxiv.org/abs/1901.11196)). Text augmentation technique based on 4 text manipulation operations: synonym replacement, random insertion, random swap, and random deletion. (GitHub link: https://github.com/jasonwei20/eda_nlp) 

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
##### Universal Sentence Encoder
1. Download [the transformer variant of Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder-large/3) ([direct link](https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed))
2. Decompress and put `assets`, `variables`, `saved_model.pb` and `tfhub_module.pb` under `model/pretrained/universal_sentence_encoder` directory
##### ActiveQA Question Reformulator (pretrained on UN+Paralex datasets)
Checkpoint without reinforcement learning:
1. Download the pretrained model from this [direct link](https://storage.googleapis.com/pretrained_models/translate.ckpt-1460356.zip)
2. Decompress and put `translate.ckpt-1460356.data-00000-of-00001`, `translate.ckpt-1460356.index` and `translate.ckpt-1460356.meta` under `model/pretrained/active-qa/translate.ckpt-1460356` directory

Checkpoint with reinforcement learning:
1. Download the pretrained model from this [direct link](https://storage.cloud.google.com/pretrained_models/translate.ckpt-6156696.zip)
2. Decompress and put `translate.ckpt-6156696.data-00000-of-00001`, `translate.ckpt-6156696.index` and `translate.ckpt-6156696.meta` under `model/pretrained/active-qa/translate.ckpt-6156696` directory

## Usage
### Question Generation
```
python script/generate.py [--method METHOD] [--input_path INPUT_PATH] [--output_path OUTPUT_PATH]

arguments:
  --method       METHOD       Question generation method. Available option: [fpm, symsub, hybrid, zeroshot, zeroshot-rl, eda]
                            
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
- Buck, Christian, et al. "Ask the right questions: Active question reformulation with reinforcement learning." arXiv preprint arXiv:1705.07830 (2017).
- Wei, Jason, and Kai Zou. "EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks." Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP). 2019.
- Cer, Daniel, et al. "Universal sentence encoder." arXiv preprint arXiv:1803.11175 (2018).
- Miller, George A. WordNet: An electronic lexical database. MIT press, 1998.
- Basile, Pierpaolo, Annalina Caputo, and Giovanni Semeraro. "An enhanced lesk word sense disambiguation algorithm through a distributional semantic model." Proceedings of COLING 2014, the 25th International Conference on Computational Linguistics: Technical Papers. 2014.
