import json, random, re, os
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

def Main():
    ngramFileName = input("Name of the NGram file: ")
    ngramPath = f"{os.getenv("NGRAM_PATH")}{ngramFileName}"

    try:
        with open(ngramPath, "r") as file:
            weights = json.load(file)
    except FileNotFoundError:
        print(f"File {ngramPath} not found.")
        input()
        return

    for i in range(1,50):
        print(GenerateWord(weights), end="\n" if i % 5 == 0 else ", ")

    input()

if (__name__ == "__main__"):
    load_dotenv()

    Main()