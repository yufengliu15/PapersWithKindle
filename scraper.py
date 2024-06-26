# scrape from https://jeffhuang.com/best_paper_awards/conferences.html
# this is because it sorts it by category for me :D

from bs4 import BeautifulSoup
import requests
import re
import json

URL = "https://jeffhuang.com/best_paper_awards/conferences.html"

res = requests.get(URL)
htmlData = res.content
parsedData = BeautifulSoup(htmlData, "html.parser")
tables = parsedData.find_all('table')

# regex
# Regular expression pattern
pattern = r'\((.*?)\)'

papers = {}
# Structure:
# { "Category 1": {
#      "Year": value,
#      "Title": value,
#      "Authors": value,
#      "Link": value
#   },
#   "Category 2": {
#       .... 
#   }
# }
for table in tables:
    category = re.findall(pattern, table.find('th').string)[0]
    rows = table.find('tbody').find_all('tr')
    
    papers = {category: None}
    papersOfCategory = []
    for row in rows:
        try: 
            # extract Year
            if (row.find('th') is None):
                year = lastYear
            else:
                year = row.find('th').find('a').string
                lastYear = year
        except:
            print("Couldn't parse for Year!")
        
        try:
            # extract Title
            title = row.find('td', class_="paper-title").string
        except:
            print("Couldn't parse for Title!")
        
        try:
            # extract Link
            link = row.find('td', class_="paper-title").find('a').attrs['href']
        except:
            print("Couldn't parse for Link!")
        
        try:
            # extract Authors
            author = row.find('td', class_="authors").contents[0]
        except:
            print("Couldn't parse for Author!")
            
        # add all parsed fields into an array
        paper = [year, title, author, link]
        papersOfCategory.append(paper)
    
    # send to dictionary
    papers[category] = papersOfCategory

# export as JSON
try:  
    with open("papers.json", "w") as outfile:
        json.dump(papers,outfile)
    print("Successfully Exported to JSON")
except:
    print("Unable to Export to JSON")



