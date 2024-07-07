# scrape from https://jeffhuang.com/best_paper_awards/conferences.html
# this is because it sorts it by category for me :D

from bs4 import BeautifulSoup
import requests, re, json, time, random

from urllib.parse import urlparse

URL = "https://jeffhuang.com/best_paper_awards/conferences.html"
READER_API = "https://r.jina.ai/"

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

def download_file(url, filename):
    response = requests.get(url)
    
    with open("./papers/" + filename, 'wb') as file:
        file.write(response.content)
    
    return "./papers/" + filename

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

def extractSemanticScholar(title, link):
    #er
    return

def extractGoogleScholar(title, link):
    #try:
        res = requests.get(READER_API + link, headers={"X-Proxy-Url": "brd.superproxy.io:22225", "X-Timeout": "10"})
        htmlData = res.content
        print(htmlData)
        #parsedData = BeautifulSoup(htmlData, "html.parser")
        #span = parsedData.findAll('span')
        #if (not span):
        #    print(urlparse(link).netloc)
        #else:
        #    print(urlparse(link).netloc)
        #    if (len(span) < 95):
        #        print(span)
        #        return
        #    link_to_pdf = span[95].parent["href"]
        #    print(f"span[95].parent['href']: {link_to_pdf}")
        #    print(f"span[95]: {span[95].text}")
        #    #if (span[95].content)
        #    if (not ("/scholar_alerts" in link_to_pdf)):
        #        return download_file(link_to_pdf, title + ".pdf")
    #except:
    #    print("Unable to download the PDF from Sematic Scholar")

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
    
    papers[category] = None
    papersOfCategory = []
    for row in rows:
        link = extractLink(row)
        title = extractTitle(row)
        key = urlparse(link).netloc
        if (key == "www.semanticscholar.org"):
            filePath = extractSemanticScholar(title, link)
        elif (key == "scholar.google.com"):
            filePath = extractGoogleScholar(title, link)
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
        paper = [year, title, author, link, filePath]
        papersOfCategory.append(paper)
        
    
    # send to dictionary
    papers[category] = papersOfCategory
    break
    

# export as JSON
try:  
    with open("papers.json", "w") as outfile:
        json.dump(papers,outfile)
    print("Successfully Exported to JSON")
except:
    print("Unable to Export to JSON")

