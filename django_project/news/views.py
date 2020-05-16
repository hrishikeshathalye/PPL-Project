from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
# scraping WHO news
who_r = requests.get("https://www.who.int/emergencies/diseases/novel-coronavirus-2019/media-resources/news")
who_soup = BeautifulSoup(who_r.content, 'html5lib')

who_headings = who_soup.find_all("a", {"class": "link-container"})

who_news = []

for wh in who_headings:
    who_news.append([wh["href"], wh.text])

#scrape ToI news
toi_r = requests.get("https://timesofindia.indiatimes.com/briefs")
toi_soup = BeautifulSoup(toi_r.content, 'html5lib')

toi_headings = toi_soup.find_all('h2')

toi_headings = toi_headings[2:-13] # excluding header and removing footers

toi_news = []

for th in toi_headings:
    toi_news.append(["https://timesofindia.indiatimes.com/"+th.find('a')["href"], th.find('a').text])

def index(req):
    return render(req, 'news/index.html', {'who_news':who_news, 'toi_news': toi_news})