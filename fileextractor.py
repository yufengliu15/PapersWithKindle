import json, os, requests, time
from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from urllib.parse import urlparse
from openai import OpenAI

load_dotenv()
FIRE_CRAWL2_API_KEY = os.getenv('FIRE_CRAWL2_API_KEY')
OPEN_AI_API_KEY = os.getenv('OPEN_AI_API_KEY')

app = FirecrawlApp(api_key=FIRE_CRAWL2_API_KEY)
client = OpenAI(api_key=OPEN_AI_API_KEY)

f = open('papers.json')

data = json.load(f)

brokenPaper = []

def download_file(url, filename):
    response = requests.get(url)
    
    safe_filename = filename.replace("/", "⁄")
    with open("./papers/" + safe_filename + ".pdf", 'wb') as file:
        file.write(response.content)
        
    if ("403 Forbidden" in str(response.content)):
        brokenPaper.append(safe_filename)
        with open("brokenPapers.json", "w") as outfile:
            json.dump(brokenPaper,outfile)
        return None, False
    
    return "./papers/" + safe_filename + ".pdf", True

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
    print(f"link: {link}")
    scraped_data = app.scrape_url(link)['markdown']
    
    if (urlparse(link).netloc == "www.semanticscholar.org"):
        scraped_data = scraped_data[:1700]
    elif(urlparse(link).netloc == "scholar.google.com"):
        half_char = len(scraped_data)//2
        scraped_data = scraped_data[half_char:]
    
    try:   
        response = extract(scraped_data, title)
        res = json.loads(response)
        return download_file(res["link"], title)
    except:
        return None, False

def iterateJSON(counter):
    loopcounter = 0
    for category in data:
        for paper in data[category]:
            if counter == 600:
                return
            if loopcounter < counter:
                loopcounter += 1
                if (loopcounter < 2):
                    print("Skipping...")
                continue
            if ((counter - prev_paper_count) % 5 == 0 and prev_paper_count != loopcounter):
                print("Waiting for firecrawl rate limit...")
                start_time = time.time()
                while True:
                    elapsed_time = time.time() - start_time
                    if elapsed_time >= 50:  
                        start_time = time.time()
                        break
                    time.sleep(1)  # Sleep for a short while to prevent tight loop
                    
            filePath, result = extractPDFUrl(paper["link"], paper["title"])
            
            if (result):      
                print(f"Successfully extract {paper["title"]} \n")
            else:
                print("=============================================")
                print(f"Unsuccessful extraction of {paper["title"]} \n")
            
            print(f"Currently on paper: {counter} (0 index)")
            counter += 1
            loopcounter += 1
            
prev_paper_count = 451
iterateJSON(prev_paper_count)








