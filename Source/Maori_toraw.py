# This script converts the 'maori.pdf' file into a list of words, which then can be tokenised elsewhere.
# it filters out all words but nouns and removes duplicates

# importing required classes
from pypdf import PdfReader
import re 

# creating a pdf reader object
reader = PdfReader("Source/raw/maori.pdf")

wordlist : str = ""

# read each page
for page in reader.pages:
    pageText = page.extract_text()
    lines = pageText.split("\n")

    # loop thru each line. Entries with maori words have atleast 3 strings if split by " "
    for line in lines:
        words = line.split(" ")

        # sometimes the word type is merged with the word. Unmerge
        # there are otehr types other than 'n', but since we filter only for n, we can ignore those
        # note: no maori words ending with n
        if (words[0].endswith("n")):
            maori = words[0][0:-1]
            words = [maori, "n", "3rd field"]

        if (len(words) < 3): continue # has atleast maori, word type and def. It means its not the title or a page number
        maori = words[0]
        wordtype = words[1]

        if (wordtype != "n") : continue # ignore everything not noun
        if (re.search(r"[()+← ]", maori)) : continue # some entries have weird chars and are rare enough to safely discard

        wordlist += maori + " "


# save word list to file
# file will create itself if not exist
with open("Source/wordlists/maori_wordlist.txt", "w", encoding = "UTF-8") as file:
    file.write(wordlist)
    file.close()

