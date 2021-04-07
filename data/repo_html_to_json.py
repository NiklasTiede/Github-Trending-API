
import json
import bs4
from scraping import filter_articles, scraping_repositories

from pprint import pprint

with open('repodata6.html', 'r') as f:
    articles_html = f.read()

bla = filter_articles(articles_html)
soup = bs4.BeautifulSoup(bla, "lxml")
stuff =  soup.find_all("article", class_="Box-row")
html = scraping_repositories(stuff, since='daily')

with open('repodata6.json', 'w') as fw:
    fw.write(json.dumps(html, indent=4))
