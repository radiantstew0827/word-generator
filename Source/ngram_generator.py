

nSize = 4
wordlist_path = "Source/wordlists/maori_wordlist.txt"

def GenerateNGrams(n : int, tokens : str):
    contextSize = n-1# the n'th character is the one beign predicted. Thfre contextsize is n-1
    ngrams = []

    for i in range(0, len(tokens) - n):
        context = tokens[i: i+contextSize] # [inclusive : exclusive]
        target = tokens[i + contextSize]
        ngram = (context, target)
        ngrams.append(ngram)



def Main():
    try:
        file = open(wordlist_path, "r", encoding = "UTF-8")
    except FileNotFoundError:
        #print(f"File {wordlist_path} not found.")
        input()
        return # exit program

    wordlist = file.read()

    # add start characters so previous words aren't being read and converted into ngrams
    contextSize = nSize-1
    start = "_"*contextSize

    # add end character so the generation can choose to end the word
    end = "0"
    interword = end + start

    # add end and start characters
    wordlist = wordlist.replace(" ", interword)
    wordlist = start + wordlist

    # generate ngrams
    GenerateNGrams(nSize, wordlist)

if __name__ == "__main__":
    Main()