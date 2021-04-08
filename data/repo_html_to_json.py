"""This script scrapes data from local HTML files (repositories).
The generated JSON-files are compared to their HTML counterparts to ensure
proper data extraction. The HTML/JSON is used to test scraping-functions
"""

# this file has to be moved into the same folder as the
# scraping.py file (app/) to be working smoothly

import json

import bs4

from scraping import filter_articles, scraping_repositories

with open("repodata4.html", "r") as f:
    articles_html = f.read()

bla = filter_articles(articles_html)
soup = bs4.BeautifulSoup(bla, "lxml")
stuff = soup.find_all("article", class_="Box-row")
html = scraping_repositories(stuff, since="daily")

with open("repodata4.json", "w") as fw:
    fw.write(json.dumps(html, indent=4))
