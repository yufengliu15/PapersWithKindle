# scrape from https://jeffhuang.com/best_paper_awards/conferences.html
# this is because it sorts it by category for me :D

from bs4 import BeautifulSoup
import requests, re, json

URL = "https://jeffhuang.com/best_paper_awards/conferences.html"

res = requests.get(URL)
htmlData = res.content
parsedData = BeautifulSoup(htmlData, "html.parser")
tables = parsedData.find_all('table')

# regex
pattern = r'\((.*?)\)'


# functions to extract html
# -----------------------------
def extractTitle(row):
    try:
        # extract Title
        return row.find('td', class_="paper-title").string
    except:
        print("Unable to parse for Title!")    
        
def extractLink(row):
    try:
        # extract Link
        return row.find('td', class_="paper-title").find('a').attrs['href']
    except:
        print("Unable to parse for Link!")
        
def extractAuthor(row):
    try:
        # extract Authors
        return row.find('td', class_="authors").contents[0]
    except:
        print("Unable to parse for Author!")  

papers = {}

# Structure:
# { "Category 1": [{
#      "Year": value,
#      "Title": value,
#      "Authors": value,
#      "Link": value,
#      "FilePath": value
#   }],
#   "Category 2": [{
#       .... 
#   }]
# }
for table in tables:
    category = re.findall(pattern, table.find('th').string)[0]
    rows = table.find('tbody').find_all('tr')
    
    if (not category in papers):
        papers[category] = []

    for row in rows:
        link = extractLink(row)
        title = extractTitle(row)

        try: 
        # extract Year
            if (row.find('th') is None):
                year = lastYear
            else:
                year = row.find('th').find('a').string
                lastYear = year
        except:
            print("Unable to parse for Year!")
            
        author = extractAuthor(row)

        # add all parsed fields into an array
        paper = {"year": year, "title": title, "author": author, "link": link}
        papers[category].append(paper)
    
# export as JSON
try:  
    with open("papers.json", "w") as outfile:
        json.dump(papers,outfile)
    print("Successfully Exported to JSON")
except:
    print("Unable to Export to JSON")

