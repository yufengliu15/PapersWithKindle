# scrape from https://jeffhuang.com/best_paper_awards/conferences.html
# this is because it sorts it by category for me :D

from bs4 import BeautifulSoup
import requests, re, json, time, random

from urllib.parse import urlparse


URL = "https://jeffhuang.com/best_paper_awards/conferences.html"

res = requests.get(URL)
htmlData = res.content
parsedData = BeautifulSoup(htmlData, "html.parser")
tables = parsedData.find_all('table')

# regex
pattern = r'\((.*?)\)'

user_agent_list = [
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
]

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
        
#def extractSemanticScholarFile(link):
#    try:
#        welp = None
#    except:
#        print("Unable to download the PDF from Sematic Scholar")
#
#def extractGoogleFile(link):
#    #try:
#    for _ in user_agent_list:
#        #Pick a random user agent
#        user_agent = random.choice(user_agent_list)
#        #Set the headers 
#        headers = {'User-Agent': user_agent}
#        
#    _parsedData = BeautifulSoup(requests.get(link, headers=headers).content, "html.parser")
    
    #except:
    #    print("Unable to download the PDF from Google Scholar")   

papers = {}
sites = {}

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
    
    papers[category] = None
    papersOfCategory = []
    for row in rows:
        link = extractLink(row)
        #key = urlparse(link).netloc
        #if (key == 'scholar.google.com'):
        #    filePath = extractGoogleFile(link)
        #elif (key == 'www.semanticscholar.org'):
        #    filePath = extractSemanticScholarFile(link)
        #else:
        #    continue
        
        try: 
        # extract Year
            if (row.find('th') is None):
                year = lastYear
            else:
                year = row.find('th').find('a').string
                lastYear = year
        except:
            print("Unable to parse for Year!")
            
        title = extractTitle(row)
        author = extractAuthor(row)


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
