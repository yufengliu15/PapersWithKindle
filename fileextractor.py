import json, os, requests
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
import os
from urllib.parse import urlparse

load_dotenv()
API_KEY = os.getenv('API_KEY')

app = FirecrawlApp(api_key=API_KEY)

f = open('papers.json')

data = json.load(f)

def download_file(url, filename):
    response = requests.get(url)
    
    with open("./papers/" + filename, 'wb') as file:
        file.write(response.content)
    
    return "./papers/" + filename

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

def iterateJSON(counter):
    for category in data:
        for paper in data[category]:
            if counter == 1:
                return
            counter += 1
            paper["filepath"] = "blah"
            print(paper)

iterateJSON(counter=0)




