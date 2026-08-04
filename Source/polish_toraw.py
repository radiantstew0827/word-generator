from pypdf import PdfReader
import re

lastWord : str = ""
wordList = ""

def ParsePage(pageText : str):
    global lastWord, wordList
    lines = pageText.split("\n")

    for line in lines:
        # filter if beginning with number
        if (re.search("^[0-9]", line)): continue

        words = line.split(" ")
        # places will have atleast 7 fields. Filter with less than that
        if (len(words) < 7): continue

        place = words[0]
        place = place.lower()

        # remove duplicates
        if (place == lastWord): continue

        #set
        wordList += place + " "
        lastWord = place

def ParsePDF(path: str, pdfIndex : int):
    reader = PdfReader(path)

    # loop thru pages
    for page in reader.pages:
        # just cuz the documents have some weird stuff, skip the first 2 pages of pdf 1
        if (pdfIndex == 1 and page.page_number >= 2): continue

        pageText = page.extract_text()
        ParsePage(pageText)

def Main():
    # loop thru each pdf
    for pdfI in range(1,6):
        filepath = f"Source/raw/Poland{pdfI}.pdf"
        ParsePDF(filepath, pdfI)

    # save word list to file
    # file will create itself if not exist
    with open("Source/wordlists/polish_wordlist.txt", "w", encoding = "UTF-8") as file:
        file.write(wordList)
        file.close()

    print("Saved")
    input()
        

if __name__ == "__main__": Main()