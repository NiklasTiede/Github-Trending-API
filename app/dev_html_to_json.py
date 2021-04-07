
import json
import bs4
from scraping import filter_articles, scraping_repositories, scraping_developers

from pprint import pprint

with open('devdata1.html', 'r') as f:
    articles_html = f.read()

bla = filter_articles(articles_html)
soup = bs4.BeautifulSoup(bla, "lxml")
stuff =  soup.find_all("article", class_="Box-row")
html = scraping_developers(stuff, since='daily')

with open('devdata1.json', 'w') as fw:
    fw.write(json.dumps(html, indent=4))
