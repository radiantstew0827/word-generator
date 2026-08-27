from src.modules.wikt_parser import Parse
import argparse

# argparse
parser = argparse.ArgumentParser()
parser.add_argument("input_file", help="name of the wiktionary data dump to be converted into wordlist training data.")
parser.add_argument("lang_codes", help="language codes of languages to look for. Can be a single lang code or a list such as \"en es de fr\".")
parser.add_argument("-p", "--keep_phrases", help="do not filter out phrases - entries with more than one word", action="store_true")
parser.add_argument("-c", "--char_limit", help="filter out words above this character limit", type = int, default=99)
parser.add_argument("-t", "--trns_threshhold", help="translation count decently reflects usage frequency of the word. entries with translations below the threshold - and therefore less common - will be filtered out.", type = int, default=0)
parser.add_argument("-s", "--separator", help="the seperator used in the wordlist", default=", ")

def Main():
    args = parser.parse_args()

    Parse(args.input_file, args.lang_codes, args.keep_phrases, args.char_limit, args.trns_threshhold, args.separator)
    
    
if __name__ == "__main__":
    Main()