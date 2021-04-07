import bs4
import typing
import aiohttp


async def get_request(*args, **kwargs):
    """ GET request performed with aiohttp to make
    asynchronous requests. 
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(*args, **kwargs) as resp:
                return await resp.text()
    except aiohttp.ClientConnectorError as cce:
        return cce


def filter_articles(raw_html: str) -> str:
    """Filters html out, which is not enclosed by article-tags.
    Beautifulsoup is inaccurate and slow when applied on a larger 
    html string, this filtration fixes this.
    """
    raw_html = raw_html.split("\n")

    # count number of article tags within the document (varies from 0 to 50):
    article_tags_count = 0
    tag = "article"
    for line in raw_html:
        if tag in line:
            article_tags_count += 1

    # copy HTML enclosed by first and last article-tag:
    articles_arrays, is_article = [], False
    for line in raw_html:
        if tag in line:
            article_tags_count -= 1
            is_article = True
        if is_article:
            articles_arrays.append(line)
        if not article_tags_count:
            is_article = False
    return "".join(articles_arrays)


def make_soup(articles_html: str) -> bs4.element.ResultSet:
    """ html enclosed by article-tags is converted into a 
    soup for further data extraction. 
    """
    soup = bs4.BeautifulSoup(articles_html, "lxml")
    return soup.find_all("article", class_="Box-row")


def scraping_repositories(
    matches: bs4.element.ResultSet, since: str
) -> typing.List[typing.Dict]:
    """ Data about all trending repositories are extracted.
    """
    trending_repositories = []
    for rank, match in enumerate(matches):

        # description
        if match.p:
            description = match.p.get_text(strip=True)
        else:
            description = None

        # relative url
        rel_url = match.h1.a["href"]

        # absolute url:
        repo_url = "https://github.com" + rel_url

        # name of repo
        repository_name = rel_url.split("/")[-1]

        # author (username):
        username = rel_url.split("/")[-2]

        # language and color
        progr_language = match.find("span", itemprop="programmingLanguage")
        if progr_language:
            language = progr_language.get_text(strip=True)
            lang_color_tag = match.find("span", class_="repo-language-color")
            lang_color = lang_color_tag["style"].split()[-1]
        else:
            lang_color, language = None, None

        stars_built_section = match.div.findNextSibling("div")

        # total stars:
        if stars_built_section.a:
            raw_total_stars = stars_built_section.a.get_text(strip=True)
            if "," in raw_total_stars:
                raw_total_stars = raw_total_stars.replace(",", "")
        if raw_total_stars:
            try:
                total_stars = int(raw_total_stars)
            except ValueError as VE:
                print(VE)
        else:
            total_stars = None

        # forks
        if stars_built_section.a.findNextSibling("a"):
            raw_forks = stars_built_section.a.findNextSibling("a").get_text(strip=True)
            if "," in raw_forks:
                raw_forks = raw_forks.replace(",", "")
        if raw_forks:
            try:
                forks = int(raw_forks)
            except ValueError as VE:
                print(VE)
        else:
            forks = None

        # stars in period
        if stars_built_section.find("span", class_="d-inline-block float-sm-right"):
            raw_stars_since = (
                stars_built_section.find(
                    "span", class_="d-inline-block float-sm-right")
                .get_text(strip=True)
                .split()[0]
            )
            if "," in raw_stars_since:
                raw_stars_since = raw_stars_since.replace(",", "")
        if raw_stars_since:
            try:
                stars_since = int(raw_stars_since)
            except ValueError as VE:
                print(VE)
        else:
            stars_since = None

        # builtby
        built_section = stars_built_section.find(
            "span", class_="d-inline-block mr-3")
        if built_section:
            contributors = stars_built_section.find(
                "span", class_="d-inline-block mr-3").find_all("a")
            built_by = []
            for contributor in contributors:
                contrib_data = {}
                contrib_data["username"] = contributor["href"].strip("/")
                contrib_data["url"] = "https://github.com" + \
                    contributor["href"]
                contrib_data["avatar"] = contributor.img["src"]
                built_by.append(dict(contrib_data))
        repositories = {
            "rank": rank + 1,
            "username": username,
            "repositoryName": repository_name,
            "url": repo_url,
            "description": description,
            "language": language,
            "languageColor": lang_color,
            "totalStars": total_stars,
            "forks": forks,
            "starsSince": stars_since,
            "since": since,
            "builtBy": built_by,
        }
        trending_repositories.append(repositories)
    return trending_repositories


def scraping_developers(matches: bs4.element.ResultSet, since: str) -> typing.List[typing.Dict]:
    """ Data about all trending developers are extracted.
    """
    all_trending_developers = []
    for rank, match in enumerate(matches):

        # relative url of developer
        rel_url = match.div.a["href"]

        # absolute url of developer
        dev_url = "https://github.com" + rel_url

        # username of developer
        username = rel_url.strip("/")

        # developers full name
        name = match.h1.a.get_text(strip=True) if match.h1.a else None

        # avatar url of developer
        avatar = match.img["src"] if match.img else None

        # data about developers popular repo:
        if match.article:
            raw_description = match.article.find("div", class_="f6 color-text-secondary mt-1")
            repo_description = raw_description.get_text(strip=True) if raw_description else None
            pop_repo = match.article.h1.a
            if pop_repo:
                repo_name = pop_repo.get_text(strip=True)
                repo_url = "https://github.com" + pop_repo["href"]
            else:
                repo_name = None
                repo_url = None
        else:
            repo_description = None
            repo_name = None
            repo_url = None

        one_developer = {
            "rank": rank + 1,
            "username": username,
            "name": name,
            "url": dev_url,
            "avatar": avatar,
            "since": since,
            "popularRepository": {
                "repositoryName": repo_name,
                "description": repo_description,
                "url": repo_url,
            },
        }
        all_trending_developers.append(one_developer)
    return all_trending_developers
