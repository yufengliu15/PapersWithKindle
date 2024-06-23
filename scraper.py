# scrape from https://jeffhuang.com/best_paper_awards/conferences.html
# this is because it sorts it by category for me :D

from bs4 import BeautifulSoup

soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
print(soup.prettify())

