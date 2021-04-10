"""data scraper for selectable parameters
======================================
Script for collecting data about spoken/programming languages.
"""
# Copyright (c) 2021, Niklas Tiede.
# All rights reserved. Distributed under the MIT License.


# programming languages

from bs4 import BeautifulSoup

with open("progr_languages.html") as f:
    y = f.read()

soup = BeautifulSoup(y, "html.parser")
coding_langs = soup.find_all("a", role="menuitemradio")

for lang in coding_langs:
    before_lang_name = lang["href"].split("/")[-1].split("?")[0]

    # identifier is not allowed to contain */+/(/)/-/./, digit at the beginning
    # or using a reserved keyword -> using .replace function
    after_lang_name = (
        before_lang_name.replace("-", "_")
        .replace("+", "_")
        .replace(".", "")
        .replace(",", "")
        .replace("%", "_")
        .replace("*", "_")
        .replace("'", "")
    )

    if after_lang_name[0].isdigit():
        after_lang_name = "_" + after_lang_name

    ma_string = f'    {after_lang_name} = "{before_lang_name}"\n'

    with open("coding_languages.csv", "a") as fw:
        fw.write(ma_string)


# spoken languages

with open("spoken_languages.html") as f:
    y = f.read()

soup = BeautifulSoup(y, "html.parser")
x = soup.find_all("a", role="menuitemradio")

for lang in x:
    spoken_lang = lang.text.strip()
    spoken_lang = spoken_lang.replace(",", "").replace(" ", "_")
    abbrev = lang["href"].split("=")[-1]
    heureka = f"    {spoken_lang} = '{abbrev}'\n"

    with open("spoken_languages.csv", "a") as fw:
        fw.write(heureka)
