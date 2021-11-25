import requests
import string
from bs4 import BeautifulSoup
import os

url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'  # &page=3'
page_count = int(input('pages:'))
article_theme = input('theme:')

titles = []
article_types = []
news_links = []
news_articles_title = []
news_articles_links = []


def Punctuation(name):
    name = name.translate(str.maketrans('', '', string.punctuation))
    name = name.replace(' ', '_')
    return name
def PoiskArticlesTheme(theme, url, fold_name):

        page = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup = BeautifulSoup(page.content, 'html.parser')
        title = soup.find('ul', {'class': 'app-article-list-row'}).find_all('h3', {'class': 'c-card__title'})
        tupe = soup.find('ul', {'class': 'app-article-list-row'}).find_all('span', {'class': 'c-meta__type'})
        link = soup.find('ul', {'class': 'app-article-list-row'}).find_all('a', {'class': 'c-card__link u-link-inherit'})
        for t in title:
            titles.append(t.text.strip('\n'))
        for t in tupe:
            article_types.append(t.text)
        for l in link:
            news_links.append(l.get('href'))
        for t in range(len(article_types)):
            if article_types[t] == theme:
                news_articles_title.append(titles[t])
                news_articles_links.append(news_links[t])
        for url in news_articles_links:
            LoadArticle(url, fold_name)
def LoadArticle(url, fold_name):
    url = 'https://www.nature.com' + url
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')
    body = soup.find('div', {'class': 'c-article-body'}).text.strip()
    body = body.replace("\n", "")

    title = soup.find('h1', {'class': 'c-article-magazine-title'}).text
    name = Punctuation(title)
    SaveFile(f'{name}.txt', body, fold_name)
def SaveFile(name, content, fold):
    file = open(f"/Users/admin/PycharmProjects/Web Scraper1/Web Scraper/task/{fold}/{name}", 'w')
    file.write(content)
    file.close()
def MakeDir(name_dir):
    os.mkdir(name_dir)



for i in range(page_count):
    MakeDir(f"Page_{i+1}")
    url_new = url + f'&page={i+1}'
    PoiskArticlesTheme(article_theme, url_new, f"Page_{i+1}")




