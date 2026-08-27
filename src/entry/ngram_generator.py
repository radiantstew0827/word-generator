import json, os, argparse
from dotenv import load_dotenv
from src.modules.ngram import GenerateNGramFile

# arg parse
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="name of the txt file which contains the wordlist used to generate ngrams.")
parser.add_argument("n", help="the size of the n-grams generated.", type=int)
parser.add_argument("-s", "--seperator", help="the seperator used in the wordlist", default=", ")

# constants
SUFFIX = "_ngrams.json"

def Main():
    args = parser.parse_args()

    # dump weights into json file
    # first, get the prefix
    prefixTuple =  args.input_file.split("_")[0:-1] # remove "_wordlist.txt"
    prefix = "_".join(prefixTuple)
    outputFile = f"{prefix}{SUFFIX}"

    GenerateNGramFile(args.input_file, outputFile, n=args.n, seperator=args.seperator)

if __name__ == "__main__":
    load_dotenv()

    Main()