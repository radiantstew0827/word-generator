import os, json
from dotenv import load_dotenv

# constants
ignoreTags = {"letter", "morpheme", "suffix", "prefix", "archaic", "abbreviation", "initialism", "alt-of"}

def ProccessFile(file, langCodes : str, keepPhrases : str, charLimit : int, transThreshhold : int) ->dict[str, set[str]]:
    currentLine : int = 0
    wordLists = {}

    for line in file:
        currentLine+=1

        # inform user every 10k lines
        if (currentLine % 10000 == 0):
            print(f"Done line {currentLine}")

        # process line
        wordTuple = ProcessLine(line, langCodes, keepPhrases, charLimit, transThreshhold)

        if (not wordTuple): continue # wikt entry filtered out
        word = wordTuple[0]
        langCode = wordTuple[1]

        #insert it
        if (langCode not in wordLists):
            wordLists[langCode] = set()
        
        wordLists[langCode].add(word)
        
        

    return wordLists

def ProcessLine(data, langCodes : str, keepPhrases : str, charLimit : int, transThreshhold : int) -> tuple[str, str] | None:
    jsonLine = json.loads(data)
    if ("word" not in jsonLine): return # not a word
    if ("lang_code" not in jsonLine): return # doen't have a language?
    langCode = jsonLine["lang_code"]

    # skip not wanted languages
    if (langCode not in langCodes): return
    senses = jsonLine["senses"][0]

    # translation count threshold
    if (transThreshhold > 0): # some words have no trlations. Only check for trlations if threshhold allows it
        if ("translations" not in jsonLine): return # no translations

        translationCount = len(jsonLine["translations"])
        if (translationCount < transThreshhold): return

    # ingore these tags (not words)
    if ("tags" in senses):
        tags = set(senses["tags"])
        if (not tags.isdisjoint(ignoreTags)): return

    word : str = jsonLine["word"]

    #process word
    if (not keepPhrases and " " in word or "-" in word): return # multiple words
    if (len(word) > charLimit): return # above character limit
    word = word.lower()

    return word, langCode


def ToFile(langCode : str, wordlist : set[str], separator):
    print("Dumping word lists to files")

    with open(f"{os.getenv("WORDLIST_PATH")}{langCode}_wordlist.txt", "w", encoding = "UTF-8") as file:
        wordlistStr = separator.join(wordlist)

        file.write(wordlistStr)
        file.close()

def Parse(inputFile : str, langCodes : str, keepPhrases : str, charLimit : int, transThreshhold : int, separator : str):
    load_dotenv()

    inputFilePath = f"{os.getenv("RAW_PATH")}{inputFile}"
    try:
        with open(inputFilePath, encoding="utf-8") as file:
            wordLists = ProccessFile(file, langCodes, keepPhrases, charLimit, transThreshhold)
            
    except(FileNotFoundError):
        print(f"File {inputFilePath} not found.")
        return

    # inserts words to files
    for langCode in wordLists:
        ToFile(langCode, wordLists[langCode], separator)