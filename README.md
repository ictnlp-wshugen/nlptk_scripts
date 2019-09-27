A collection of Natural Language Processing Toolkit scripts for simplifying development.

- BPE: [subword-nmt](https://github.com/rsennrich/subword-nmt)
- Standford Tokenizer: [Standford Tagger](https://nlp.stanford.edu/software/stanford-postagger-full-2018-10-16.zip)
- Moses: [mosesdecoder](https://github.com/moses-smt/mosesdecoder)

#### Setup
```bash
$ git clone REPOSITORY_URL
$ cd nlptk_scripts
$ python setup.py develop

# install extra dependencies to activate bpe/debpe/tok functions
cd vendor
git clone https://github.com/rsennrich/subword-nmt
```

#### Scripts and Descriptions
> Note: you can use the following functions after setup by running 'nlptk-xxx' anywhere
- a2b.py Convert file's contents from Full Angle to Half Angle 
- bleu.py Using Moses to compute BLEU score
- bpe.py Quickly apply BPE
- debpe.py Remove BPE
- detok.py De-Tokenize a tokenized file using Standford Tokenizer
- fdup.py Filter duplicated sequence
- filter.py Filter sequences according to length constraint
- mapping.py Find the mapping between two shuffled files
- flen.py Obtain length statistics of sequence (tokens or characters) with max length
- shuffle.py Quick shuffle file (randomize lines order)
- stat.py Count sequence (tokens) number from corpus
- tok.py Tokenize file using Standford Tokenizer
