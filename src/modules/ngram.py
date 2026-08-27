from dotenv import load_dotenv
import json, os

def GenerateNGrams(n : int, word : str, ngrams : list[tuple[str, str]]):
    # add start characters so previous words aren't being read and converted into ngrams
    # add end character so the generation can choose to end the word
    contextSize = n - 1 # the n'th character is the one beign predicted. Thfre contextsize is n-1

    word = "_" * contextSize + word + "0"

    for i in range(0, len(word) - contextSize):
        context = word[i:i+contextSize] # [inclusive : exclusive]
        target = word[i + contextSize]
        ngram = (context, target)
        ngrams.append(ngram)

def ProcessWeights(ngrams : list[tuple[str, str]]) -> dict[str, dict[str, int]]:
    # outcomesWeights: for each context, is a weighted dictionary for each possible outcome
    outcomeWeights : dict[str, dict[str, int]] = {}

    for ngram in ngrams:
        context = ngram[0]
        target = ngram[1]

        if (context in outcomeWeights):
            # if context exist, change the probabiblity (weight)
            if target in outcomeWeights[context]:
                outcomeWeights[context][target] += 1
            else:
                outcomeWeights[context][target] = 1

        else:
            outcomeWeights[context] = {target : 1}
            
    return outcomeWeights

def GetWordlistFromFile(inputFileName : str, seperator : str) -> list[str]:
    wordlistPath = f"{os.getenv("WORDLIST_PATH")}{inputFileName}"
    
    #open word list file
    try:
        file = open(wordlistPath, "r", encoding = "UTF-8")
    except FileNotFoundError:
        print(f"File {wordlistPath} not found.")
        return None # exit program

    return file.read().split(seperator) # seperate string into a list

def GenerateNGramFile(inputFileName : str, outputFileName : str, n : int, seperator : str = ", "):
    load_dotenv()

    ngrams : list[tuple[str, str]] = []

    # get wordlist
    wordlist = GetWordlistFromFile(inputFileName, seperator)
    if (not wordlist): return

    # get ngrams
    for word in wordlist:
        GenerateNGrams(n, word, ngrams)

    # process weights
    weights = ProcessWeights(ngrams)

    # dump weights into json file
    ngramFilePath = f"{os.getenv("NGRAM_PATH")}{outputFileName}"

    with open(ngramFilePath, "w") as file:
        json.dump(weights, file, indent=2)

    print(f"n-grams successfuly created to {ngramFilePath}")