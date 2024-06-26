# scrape from https://jeffhuang.com/best_paper_awards/conferences.html
# this is because it sorts it by category for me :D

from bs4 import BeautifulSoup
import requests
import re

URL = "https://jeffhuang.com/best_paper_awards/conferences.html"

res = requests.get(URL)
htmlData = res.content
parsedData = BeautifulSoup(htmlData, "html.parser")
tables = parsedData.find_all('table')

# regex
# Regular expression pattern
pattern = r'\((.*?)\)'


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
    for row in rows:
        # extract Year
        if (row.find('th') is None):
            year = lastYear
        else:
            year = row.find('th').find('a').string
            lastYear = year
            
        # extract Title
        title = row.find('td', class_="paper-title").string
        
        # extract Link
        link = row.find('td', class_="paper-title").find('a').attrs['href']
        
        # extract Authors
        author = row.find('td', class_="authors").contents[0]
        print(author)
        
    break
        
        


