
from dataclasses import dataclass

from typing import Dict
import typing
import requests
# from requests.models import HTTPError
from pprint import pprint
from bs4 import BeautifulSoup, element


# def request_html(URL: str) -> str:
#     """ Returns HTML from a requested URL. """
#     try:
#         resp = requests.get(URL)
#     except HTTPError as he:
#         print(he)
#     return resp.text


def filter_articles(html: str) -> str:
    """ Filters html out, which is not enclosed by article-tags.
    Github trending contains up to 25 repositories/developers.

    why filtering HTML instead of using beautifulsoup directly?
    Beautifulsoup skips many articles!
    """
    all_html = html.split("\n")

    # count number of article tags within the document (varies from 0 to 50):
    article_tags = 0
    for line in all_html:
        if "article" in line:
            article_tags += 1

    # copy HTML enclosed by first and last article-tag:
    articles_html, is_Article_HTML = [], False
    counter = 0
    for line in all_html:
        if "article" in line:
            article_tags -= 1
            is_Article_HTML = True
        if is_Article_HTML:
            articles_html.append(line)
        if not article_tags:
            is_Article_HTML = False

    return "".join(articles_html)


#######
def soup_matches(articles_html: str) -> element.ResultSet:
    """ refactoring code, can be used for repos and developers. """
    soup = BeautifulSoup(articles_html, 'html.parser')
    return soup.find_all('article', class_='Box-row')


def repo_extraction(matches: element.ResultSet, since: str = "daily") -> typing.List[Dict]:
    """ Data about trending repositories are extracted
    from html enclosed by article-tags. """

    # soup = BeautifulSoup(articles_html, 'html.parser')
    # articles_match = soup.find_all('article', class_='Box-row')

    trending_repos_data = []
    for rank, repo in enumerate(matches):

        # repositories ranking
        # repo_data = {}

        # repository URL
        rel_url = repo.h1.a['href']
        repo_url = "https://github.com" + rel_url
        # repo_data["repo_URL"] = repo_url

        # projectname
        proj_name = repo_url.split('/')[-1]
        # repo_data["projectname"] = proj_name

        # description
        description_match = repo.find(
            'p', class_="col-9 color-text-secondary my-1 pr-4")
        if description_match:
            description = description_match.text.strip()
        else:
            description = None
        # repo_data["description"] = description

        # language
        repo_lang = repo.find('span', itemprop="programmingLanguage")
        if repo_lang:
            # repo_data["proj_language"] = repo_lang.text
            repo_lang_val = repo_lang.text
        else:
            # repo_data["proj_language"] = None
            repo_lang_val = None

        # since-stars:
        match2 = repo.find('span', class_='d-inline-block float-sm-right')
        if match2:
            stars_today = match2.text.split()[0]
        # else:
        #     stars_today = None
            if ',' in stars_today:
                stars_today = stars_today.replace(',', '')
            stars_today = int(stars_today)
        # repo_data[f"stars_in_range"] = int(stars_today)

        # total stars
        tot_stars = repo.find('a', href=f"{rel_url}/stargazers")
        if tot_stars:
            tot_stars = tot_stars.text.strip()

            if ',' in tot_stars:
                tot_stars = tot_stars.replace(',', '')
            tot_stars = int(tot_stars)
        # repo_data["total_stars"] = int(tot_stars)

        repo_data = {
            'rank': rank + 1,
            'URL': repo_url,
            'name': proj_name,
            'description': description,
            'language': repo_lang_val,
            'since_stars': stars_today,
            'since_data_range': since,
            'total_stars': tot_stars,
        }

        trending_repos_data.append(repo_data)

    return trending_repos_data


def dev_extraction(matches: element.ResultSet, since: str) -> typing.List[Dict]:
    """ Data about trending repositories are extracted
    from html enclosed by article-tags. """

    trending_devs_data = []
    for rank, repo in enumerate(matches):

        # dev accounts URL
        rel_url = repo.div.a['href']
        dev_url = "https://github.com" + rel_url

        # devs account name
        acc_name = rel_url.strip('/')

        # devs full name
        full_name = repo.h1.a.text.strip()

        # url to the devs tiny avatar
        avatar_url = repo.img['src']

        # some devs have a popular repo, soem not:
        if repo.article:
            print('article existing')
            popular_repo = repo.article.h1.a.text.strip()
            popular_repo_url = "https://github.com" + repo.article.h1.a['href']

            if repo.article.find('div', class_='f6 color-text-secondary mt-1'):
                repo_description = repo.article.find(
                    'div', class_='f6 color-text-secondary mt-1').text.strip()
            else:
                repo_description = None
        else:
            popular_repo = None
            popular_repo_url = None
            repo_description = None
            print('article not existing')

        devs_data = {
            'rank': rank + 1,
            'URL': dev_url,
            'account_name': acc_name,
            'full_name': full_name,
            'mini_avatar_URL': avatar_url,
            'popular_repo': popular_repo,
            'popular_repo_url': popular_repo_url,
            'repo_description': repo_description,
            'since_data_range': since,
        }
        trending_devs_data.append(devs_data)

    return trending_devs_data


payload = {'since': 'daily'}
print('payload:', payload)
resp = requests.get("https://github.com/trending/scala", params=payload)

articles_html = filter_articles(resp.text)
matches = soup_matches(articles_html)
data = repo_extraction(matches, since='weekly')
pprint(data)


# class TrendingData():
#     def __init__(self, url, html) -> None:
#         self.url = url
#         self.html = html

#     def request_html(self):
#         # self.url is used
#         return

#     def filter_articles(self):
#         pass

#     @classmethod
#     def from_repositories(cls, URL):
#         cls.request_html()
#         return ''

# # rs = RepoScraper()
# # rs(URL, )
# # TrendingData.from_developers(URL, )
# # TrendingData.from_repositories(URL, )


# data = TrendingData.from_developers()
# data = TrendingData.from_repositories()
