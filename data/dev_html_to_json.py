"""This script scrapes data from local HTML files (developers).
The generated JSON-files are compared to their HTML counterparts to ensure
proper data extraction. The HTML/JSON is used to test scraping-functions
"""
# this file has to be moved into the same folder as the
# scraping.py file (app/) to be working smoothly
import json

import bs4
from scraping import filter_articles
from scraping import scraping_developers


with open("devdata3.html") as f:
    articles_html = f.read()

bla = filter_articles(articles_html)
soup = bs4.BeautifulSoup(bla, "lxml")
stuff = soup.find_all("article", class_="Box-row")
html = scraping_developers(stuff, since="daily")

with open("devdata3.json", "w") as fw:
    fw.write(json.dumps(html, indent=4))
