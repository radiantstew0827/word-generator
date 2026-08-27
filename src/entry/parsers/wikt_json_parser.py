import json
from dotenv import load_dotenv
import os

wiktFilePath = ""
langCodes = []
wordLists : dict[str, set[str]] = {}

# settings
ignoreTags = {"letter", "morpheme", "suffix", "prefix", "archaic", "abbreviation", "initialism", "alt-of"}
filterPhrases = True # whether to filter out entries with multiple words
characterLimit = 20 # filter out words with more than these characters
translationThreshhold = 0 # translation count decently reflects usage frequency of the word. Entries with less translations than this will be skipped

def ProccessFile(file):
    currentLine : int = 0

    for line in file:
        ProcessLine(line)
        
        currentLine+=1
        # inform user every 10k lines
        if (currentLine % 10000 == 0):
            print(f"Done line {currentLine}")

def ProcessLine(data):
    global wordLists

    jsonLine = json.loads(data)
    if ("word" not in jsonLine): return # not a word
    if ("lang_code" not in jsonLine): return # doen't have a language?
    langCode = jsonLine["lang_code"]

    # skip not wanted languages
    if (langCode not in langCodes): return
    senses = jsonLine["senses"][0]

    # translation count threshold
    if (translationThreshhold > 0): # some words have no trlations. Only check for trlations if threshhold allows it
        if ("translations" not in jsonLine): return # no translations

        translationCount = len(jsonLine["translations"])
        if (translationCount < translationThreshhold): return

    # ingore these tags (not words)
    if ("tags" in senses):
        tags = set(senses["tags"])
        if (not tags.isdisjoint(ignoreTags)): return

    word : str = jsonLine["word"]

    #process word
    if (" " in word or "-" in word): return # multiple words
    if (len(word) > characterLimit): return # above character limit
    word = word.lower()

    # create entry of it in wordlists
    if (langCode not in wordLists):
        wordLists[langCode] = set()

    wordLists[langCode].add(word)


def ToFile(langCode : str, wordlist : set[str]):
    print("Dumping word lists to files")

    with open(f"{os.getenv("WORDLIST_PATH")}{langCode}_wordlist.txt", "w", encoding = "UTF-8") as file:
        seperator = os.getenv("SEPERATOR")
        wordlistStr = seperator.join(wordlist)

        file.write(wordlistStr)
        file.close()


def Main():
    global wiktFilePath, langCodes
    
    wiktFilePath = input("Relative path for wiktionary json data dump: ")
    langCodes = input("Language codes to look for: ").split(" ")

    try:
        with open(wiktFilePath, encoding="utf-8") as file:
            ProccessFile(file)
            
    except(FileNotFoundError):
        print(f"File {wiktFilePath} not found.")
        input()
        return

    # inserts words to files
    for langCode in wordLists:
        ToFile(langCode, wordLists[langCode])

    input("Finished")
    
    
if __name__ == "__main__":
    load_dotenv()

    Main()