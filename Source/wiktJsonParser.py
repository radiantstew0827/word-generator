import json

wiktFilePath = ""
langCodes = []

ignoreTags = {"letter", "morpheme", "suffix", "prefix"}
wordLists : dict[str, set[str]] = {}

def ProcessLine(data):
    global wordLists

    jsonLine = json.loads(data)
    if ("word" not in jsonLine): return
    if ("lang_code" not in jsonLine): return
    langCode = jsonLine["lang_code"]

    # skip not wanted languages
    if (langCode not in langCodes): return
    senses = jsonLine["senses"][0]

    # ingore these tags (not words)
    if ("tags" in senses):
        tags = set(senses["tags"])
        if (not tags.isdisjoint(ignoreTags)): return

    word : str = jsonLine["word"]
    word = word.lower()

    # create entry of it in wordlists
    if (langCode not in wordLists):
        wordLists[langCode] = set()

    wordLists[langCode].add(word)

    #print(word, end="\t")

def ToFile(langCode : str, wordlist : set[str]):
    print("Dumping word lists to files")

    with open(f"wordlists/{langCode}_wordlist.txt", "w", encoding = "UTF-8") as file:
        wordlistStr = " ".join(wordlist)

        file.write(wordlistStr)
        file.close()



def Main():
    global wiktFilePath, langCodes
    
    wiktFilePath = input("Relative path for wiktionary json data dump: ")
    langCodes = input("Language codes to look for: ").split(" ")
    
    with open(wiktFilePath, encoding="utf-8") as file:
        currentLine : int = 0
        for line in file:
            ProcessLine(line)
            
            currentLine+=1
            # inform user every 10k lines
            if (currentLine % 10000 == 0):
                print(f"Done line {currentLine}")

    # inserts words to files
    for langCode in wordLists:
        ToFile(langCode, wordLists[langCode])

    input("Finished")
    
    
if __name__ == "__main__":
    Main()