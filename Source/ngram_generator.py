import json

nSize = 4
wordlist_path = "Source/wordlists/english_wordlist.txt"
ngrams_path = "Source/ngrams/"


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

def Main():
    #open word list file
    try:
        file = open(wordlist_path, "r", encoding = "UTF-8")
    except FileNotFoundError:
        print(f"File {wordlist_path} not found.")
        input()
        return # exit program

    wordlist = file.read().split(" ")
    ngrams : list[tuple[str, str]] = []

    # get ngrams
    for word in wordlist:
        GenerateNGrams(nSize, word, ngrams)

    # process weights
    weights = ProcessWeights(ngrams)

    # dump weights into json file
    # first, get the prefix
    fileName = wordlist_path.split("/")[-1]
    prefixTuple =  fileName.split("_")[0:-1] # remove "_wordlist.txt"
    prefix = "_".join(prefixTuple)
    ngramFile = ngrams_path+prefix+"_ngrams.json"

    with open(ngramFile, "w") as file:
        json.dump(weights, file, indent=2)

    print(f"n-grams successfuly created to {ngramFile}")
    input()

if __name__ == "__main__":
    Main()