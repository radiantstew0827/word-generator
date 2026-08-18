# This script converts the 'maori.pdf' file into a list of words, which then can be tokenised elsewhere.
# it filters out duplicates

# importing required classes
from pypdf import PdfReader
from dotenv import load_dotenv
import re, os

# get env files
load_dotenv()
wordlistPath = os.getenv("WORDLIST_PATH")
rawPath = os.getenv("RAW_PATH")
seperator = os.getenv("SEPERATOR")

# creating a pdf reader object
reader = PdfReader(f"{rawPath}maori.pdf")

wordlist : str = ""
lastWord : str = ""

# read each page
for page in reader.pages:
    pageText = page.extract_text()
    lines = pageText.split("\n")

    #trim to remove headers and footer
    lines.pop()
    lines.pop()
    lines.pop(0)
    lines.pop(0)

    # loop thru each line. Entries with maori words have atleast 3 strings if split by " "
    for line in lines:
        if (re.search("^[0-9]", line)): continue # if begins with a number, skip

        line = re.sub("/(.*/) ", "", line) # remove weird grammar stuff, so wordtype is second

        words = line.split(" ")

        maori = words[0]
        #wordtype = words[1]

        #if (wordtype != "n"): continue # filter out non-noun word types

        maori = maori.lower()

        #remove dupilcates, dictionary is alphabetical order
        if (lastWord == maori): continue

        lastWord = maori
        wordlist += maori + seperator


# save word list to file
# file will create itself if not exist
with open(f"{wordlistPath}maori_wordlist.txt", "w", encoding = "UTF-8") as file:
    file.write(wordlist)
    file.close()

print("Finished")
input()

