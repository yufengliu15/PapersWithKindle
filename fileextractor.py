import json, os, requests, time
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

brokenPaper = []

def download_file(url, filename):
    response = requests.get(url)
    
    with open("./papers/" + filename + ".pdf", 'wb') as file:
        file.write(response.content)
        
    if ("403 Forbidden" in str(response.content)):
        brokenPaper.append(filename)
        with open("brokenPapers.json", "w") as outfile:
            json.dump(brokenPaper,outfile)
        return None, False
    
    return "./papers/" + filename + ".pdf", True

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
    
    if (urlparse(link).netloc == "www.semanticscholar.org"):
        scraped_data = scraped_data[:1700]
    print(scraped_data)
    # TODO: semantic scholar has a lot of useless shit, almost all the things i need are in the first couple of lines. remove everything else to save token usage (money)
    response = extract(scraped_data, title)
    res = json.loads(response)
    return download_file(res["link"], title)

def iterateJSON(counter):
    loopcounter = 0
    start_time = time.time()
    for category in data:
        for paper in data[category]:
            if counter == 50:
                return
            if loopcounter < counter:
                loopcounter += 1
                print("Skipping...")
                continue
            if ((counter - prev_paper_count) % 5 == 0 and prev_paper_count != loopcounter):
                print("Waiting for firecrawl rate limit...")
                while True:
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 61:  # Check if elapsed time is greater than or equal to 61 seconds
                        start_time = time.time()
                        break
                    time.sleep(1)  # Sleep for a short while to prevent tight loop
                    
            filePath, result = extractPDFUrl(paper["link"], paper["title"])
               
            if (result):      
                print(f"Successfully extract {paper["title"]}")
            else:
                print(f"Unsuccessful extraction of {paper["title"]}")
            
            print(f"Currently on paper: {counter} (0 index)")
            counter += 1
            loopcounter += 1
            
prev_paper_count = 30
iterateJSON(prev_paper_count)








