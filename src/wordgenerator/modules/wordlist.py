import re, os, json, random
from dotenv import load_dotenv

def GetTotalWeight(weightedList : dict[any, int|float]) -> float|int:
    totalWeight = 0

    for key in weightedList:
        weight = weightedList[key]
        totalWeight += weight

    return totalWeight

def FromWeightedList(weightedList : dict[any, int|float]) -> any:
    totalWeight = GetTotalWeight(weightedList)

    rng = random.uniform(0, totalWeight)


    for key in weightedList:
        weight = weightedList[key]
        rng -= weight

        if (rng <= 0):
            return key

    return("#") # indicates error

def TrimWord(word : str) -> str:
    return re.sub("[_0]", "", word)

def GenerateWord(weights : dict[str, dict[str, int]]) -> str:
    keys = list(weights.keys())

    # get n
    contextSize = len(keys[0])
    n = contextSize + 1

    # generate start size of context with start character, so it could work with ngrams
    word = "_"*contextSize

    # 0 is end character
    while (word[-1] != "0"):
        context = word[-contextSize:]

        if (context not in weights): return TrimWord(word) # if it cannot any contexts, complete word

        weightedOutcomes = weights[context]
        char = FromWeightedList(weightedOutcomes)

        # add generated char onto the word
        word += char

    return TrimWord(word)

def GenerateList(inputFile: str, wordCount : int = 50, separator : str = " | ", wordsPerLine : int = -1, filterContextSized : bool = False):
    load_dotenv()
    print(inputFile, wordCount, separator, wordsPerLine, filterContextSized)

    inputFilePath = f"{os.getenv("NGRAM_PATH")}{inputFile}"
    
    # open file
    try:
        with open(inputFilePath, "r") as file:
            weights = json.load(file)
    except FileNotFoundError:
        print(f"File {inputFilePath} not found.")
        return

    # generate words
    words = []
    while len(words) < wordCount:
        keys = list(weights.keys())
        contextSize = len(keys[0])

        word = GenerateWord(weights)

        #filter Context Sized
        if (filterContextSized and len(word) <= contextSize): continue

        words.append(word)

    # print the words
    newLines = wordsPerLine != -1
    for i in range(wordCount):
        newLineNow = newLines and (i+1) % wordsPerLine == 0
        print(words[i], end="\n" if newLineNow else separator)