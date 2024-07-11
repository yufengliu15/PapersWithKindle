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
    
    with open("./papers/" + filename + ".pdf", 'wb') as file:
        file.write(response.content)
    
    return "./papers/" + filename + ".pdf"

def extract(content: str, title):
    entity_extraction_system_message = {"role": "system", "content": "Return the PDF link to the paper with title: "+ title +". If the link is hyperlinked with PDF, return that link. If not, then look for a url that contains the words PDF. If there are multiple papers, look for the first occurence of the PDF paper with the provided title. Return as a JSON: {'link': 'url'}"}
    messages = [entity_extraction_system_message]
    messages.append({"role": "user", "content": content})

    response = client.chat.completions.create(
          model="gpt-4o",
          messages=messages,
          stream=False,
          response_format={"type": "json_object"}
      )

    print(response.usage)
    return response.choices[0].message.content
     

def extractPDFUrl(link, title):
    scraped_data = app.scrape_url(link)['markdown']

    response = extract(scraped_data, title)
    res = json.loads(response)
    print(res)
    return download_file(res["link"], title)

def iterateJSON(counter):
    loopcounter = 0
    for category in data:
        for paper in data[category]:
            if counter == 20:
                return
            if loopcounter < counter:
                loopcounter += 1
                continue
            filePath = extractPDFUrl(paper["link"], paper["title"])
                        
            print(f"Successfully extract {paper["title"]}")
            print(f"Currently on paper: {counter} (0 index)")
            counter += 1
            

iterateJSON(counter=9)








