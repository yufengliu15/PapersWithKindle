# scrape from https://jeffhuang.com/best_paper_awards/conferences.html
# this is because it sorts it by category for me :D

from bs4 import BeautifulSoup
import requests, re, json
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv
from urllib.parse import urlparse

URL = "https://jeffhuang.com/best_paper_awards/conferences.html"
load_dotenv()
API_KEY = os.getenv('API_KEY')

app = FirecrawlApp(api_key=API_KEY)
res = requests.get(URL)
htmlData = res.content
parsedData = BeautifulSoup(htmlData, "html.parser")
tables = parsedData.find_all('table')

# regex
pattern = r'\((.*?)\)'

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

#def extractGoogleScholar(title, link):
    #try:
        #link = "https://www.semanticscholar.org/paper/WinoGrande-Sakaguchi-Bras/401dc39c2c8c910253d47980cfa3b4d2f7790d9b"
        #scraped_data = app.scrape_url(link)
        #print(scraped_data['markdown'])
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
        #if (key == "www.semanticscholar.org"):
        #    filePath = extractSemanticScholar(title, link)
        #elif (key == "scholar.google.com"):
        #    filePath = extractGoogleScholar(title, link)
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

