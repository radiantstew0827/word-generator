# Word generator

## Overview

This project contains a set of tools to generate realistic words based on training data. It uses the N-Gram model to generate words which are statistically likely according to the training data used to create it. 

This project uses wiktionary dumps, found on [kaikki](kaikki.org/dictionary/rawdata.html), to create training data. These are called wordlists and are stored on `data/wordlists/`. Another tool creates N-Gram files, stored in `data/ngrams/`. This N-Gram file is used to generate the words.

The English wiktionary data dump contains entry from all languages, meaning words of other languages can be extracted. However, translation data is only available for English.. The number of translation under a word decently reflects usage of a word, which can be used to filter out words too niche or sophisticated from the training data. Therefore, you might wish to download wiktionary of datadumps of another languages if you wish filter based on translation count. Data dumps must be stored in `data/raw/`.

Examples of some generated words:
![Example](/Examples.png)

The original purpose of this project was to create N-Gram models to generate names for procedurally generated island names for a game project. The game is set in the pacific, therefore a lot of examples in `data/ngrams/` and `data/wordlists/` are of pacific languages.

## Setup and Installation

### Requirements

- Python 3.12 or newer
- pip

### Installation

Assuming the repo has been cloned and cd'ed into:

Create and activate venv
```bash
python -m venv .venv
```

then
#### Windows
```bash
.venv\Scripts\activate
```
#### Linux/MacOS
```bash
source .venv/bin/activate
```

Install:
```bash
pip install .
```

### Config

Copy `.env.example` file
```bash
cp .env.example .env
```

for PowerShell:
```bash
Copy-Item .env.example .env
```

Configure `.env` accordingly

## Usage

All of the tools in this project are command-line. They are as follows:
- ngram-generator
- word-generator
- wikt-json-parser

For all of these commands, detailed usage, including optional parameters, can be viewed with `-h` argument.

### Wiktionary parser

The repo does not contain wiktionary files by default due to their size. They have to be downloaded from [kaikki](kaikki.org/dictionary/rawdata.html) and placed in `data/raw/`.

The wiktionary parser `wikt-json-parser` takes the dump and creates the training data.
```bash
wikt-json-parser <input_file> <lang_codes>

# Example, extract english and French from the datadump 
wikt-json-parser raw-wiktextract-data.jsonl "en fr"
```

This command will creare a _wordlist.txt file in `data/wordlists/` for each language given.

### N-Gram generator

The ngram tool `ngram-generator` takes the wordlist file and creates an ngram file in `data/ngrams/`

```bash
ngram-generator <input_file> <n>

# Example
ngram-generator en_wordlist.txt 4
```

The `n` argument determines the context window the script will take when generating N-Grams. Higher n means words more similar to the training data, albeit with less variation, often creating less original words. Lower n means opposite, words less similar to training data but with more variance. n = 4 seems best for most languages such as English.

### Word generator

The word generator takes the ngram file and outputs generated words. 
```bash
word-generator <input_file> <word_count>

# Example
word-generator en_ngrams.json 50
```