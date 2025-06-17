import sys

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient, errors
from pymongo.server_api import ServerApi

from dotenv import load_dotenv
import os
import json

import pprint

url = 'https://quotes.toscrape.com/'

response = requests.get(url)
soup_main_page = BeautifulSoup(response.text, 'lxml')

quotes = soup_main_page.find_all('span', class_='text')
authors = soup_main_page.find_all('small', class_='author')
tags = soup_main_page.find_all('div', class_='tags')
authors_select = soup_main_page.select("[href^='/author/']")

# Quotes handling
quotes_list = []
for i in range(0, len(quotes)):
    tagsforquote = tags[i].find_all('a', class_='tag')

    quotes_list.append({
        'tags': [tag.get_text(strip=True) for tag in tagsforquote],
        'author': authors[i].text,
        'quote': quotes[i].text,
    })

# Authors handling
authors_list = []

for author_page in authors_select:
    author_url = url.rstrip('/') + author_page.get('href')
    author_response = requests.get(author_url)

    soup_author_page = BeautifulSoup(author_response.text, 'lxml')

    authors_list.append({
        'fullname': soup_author_page.find('h3', class_='author-title').get_text(strip=True),
        'born_date': soup_author_page.find('span', class_='author-born-date').get_text(strip=True),
        'born_location': soup_author_page.find('span', class_='author-born-location').get_text(strip=True),
        'description': soup_author_page.find('div', class_='author-description').get_text(strip=True),
    })

# Save to json files
with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_list, f, ensure_ascii=False, indent=4)

with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors_list, f, ensure_ascii=False, indent=4)

# Save to MongoDB
load_dotenv()
db_string = os.getenv("DB_STRING")
scrapping_db = os.getenv("SCRAPPING_DB")

client = MongoClient(
    db_string,
    server_api=ServerApi('1')
)
db = client.get_database(scrapping_db)

db.quotes.insert_many(quotes_list)
db.authors.insert_many(authors_list)


# db = client.get_database(scrapping_db)

client.close()
