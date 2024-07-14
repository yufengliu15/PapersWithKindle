import json
from PyPDF2 import PdfReader

f = open('papers.json')

data = json.load(f)

def isValidPDF(filename):
    filepath = f"./papers/{filename}.pdf"
    try:
        with open(filepath, 'rb') as file:
            PdfReader(file)
        return True
    except:
        return False

def iterateJSON(counter, brokenPaper):
    loop_counter = 0
    for category in data:
        for paper in data[category]:
            if (loop_counter > counter):
                return
            if (not isValidPDF(paper["title"])):
                brokenPaper.append(paper["title"])
                with open("brokenPapers.json", "w") as outfile:
                    json.dump(brokenPaper,outfile)
            loop_counter += 1
                    
brokenPaper = []
counter = 1507  
iterateJSON(counter, brokenPaper)

print("Calculating % of invalid PDFs in respect to the number checked.")
print(f"{len(brokenPaper)}/{counter} = {len(brokenPaper)/counter*100}")