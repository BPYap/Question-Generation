# Pretrained Models Download Instructions

### fastText
1. Download [fastText English vectors](https://fasttext.cc/docs/en/crawl-vectors.html) [[direct link](https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.bin.gz)]
2. Decompress and put `cc.en.300.bin` under `pretrained/fastText`directory

### GloVe
1. Download [spaCy pretrained GloVe model](https://spacy.io/models/en#en_vectors_web_lg) [[direct link](https://github.com/explosion/spacy-models/releases/download/en_vectors_web_lg-2.1.0/en_vectors_web_lg-2.1.0.tar.gz)]
2. Decompress and put `en_vectors_web_lg-2.1.0` (the most nested folder) under `pretrained/spacy_glove` directory

### Universal Sentence Encoder
1. Download the [transformer variant of Universal Sentence Encoder](https://tfhub.dev/google/universal-sentence-encoder-large/3) [[direct link](https://tfhub.dev/google/universal-sentence-encoder-large/3?tf-hub-format=compressed)]
2. Decompress and put `assets`, `variables`, `saved_model.pb` and `tfhub_module.pb` under `pretrained/universal_sentence_encoder` directory

### ActiveQA Question Reformulator (pretrained on UN+Paralex datasets)
1. Download the pretrained model from this [link](https://storage.googleapis.com/pretrained_models/translate.ckpt-1460356.zip)
2. Decompress and put `translate.ckpt-1460356.data-00000-of-00001`, `translate.ckpt-1460356.index` and `translate.ckpt-1460356.meta` under `pretrained/active-qa/translate.ckpt-1460356` directory
