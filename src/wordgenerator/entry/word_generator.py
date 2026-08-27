import argparse
from wordgenerator.modules.wordlist import GenerateList

# argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="name of the txt file which contains the wordlist used to generate ngrams.")
parser.add_argument("word_count", help="number of words to generate.", type=int)
parser.add_argument("-s", "--separator", help="the seperator inserted between each word", default=" ")
parser.add_argument("-l", "--perline", help="maximum number of words on each line. -1 for no new lines", default=-1, type=int)
parser.add_argument("-c", "--ctxsized", help = "whether to filter out words which are same length or smaller than context size. Words of such length are guaranteed to already exist in training data.", action="store_true")

def main():
    args = parser.parse_args()

    GenerateList(args.input_file, args.word_count, args.separator, args.perline, args.ctxsized)

if (__name__ == "__main__"):
    main()