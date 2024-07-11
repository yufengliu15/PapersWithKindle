import json, os, requests
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from urllib.parse import urlparse
from openai import OpenAI

load_dotenv()
FIRE_CRAWL_API_KEY = os.getenv('FIRE_CRAWL_API_KEY')
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')

app = FirecrawlApp(api_key=FIRE_CRAWL_API_KEY)
client = OpenAI(api_key=OPEN_AI_API_KEY)

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

def extract(content):
    entity_extraction_system_message = {"role": "system", "content": ""}

    messages = [entity_extraction_system_message]
    messages.append({"role": "user", "content": content})

    response = client.chat.completions.create(
          model="gpt-4o",
          messages=messages,
          stream=False,
          response_format={"type": "json_object"}
      )

    return response.choices[0].message.content
     

def extractPDFUrl(link):
    scraped_data = app.scrape_url(link)['markdown']
    print(scraped_data)
    
    return

def iterateJSON(counter):
    for category in data:
        for paper in data[category]:
            if counter == 1:
                return
            counter += 1
            pdfUrl = extractPDFUrl(paper["link"])
            

iterateJSON(counter=0)

with open('papers.json', 'w') as f:
    json.dump(data, f)
    f.close






