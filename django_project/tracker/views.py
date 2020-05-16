from django.shortcuts import render
import requests
from bs4 import BeautifulSoup


def getData(url):
    r = requests.get(url)
    return r.text

data = getData("https://www.mohfw.gov.in/")
soup = BeautifulSoup(data, 'html.parser')
str = ""

for tr in soup.find_all("tbody")[0].find_all("tr"):
    str += tr.get_text()

l1 = str.split("\n\n")
l2 = []
for i in l1:
    l2.append(i.split("\n"))

l2[0] = l2[0][1:]
l2 = l2[0:-10]


i = 0
while(i < 11):
    l2[i] = l2[i] + l2[i+1]
    del(l2[i+1])
    l2[i] = l2[i] + l2[i+1]
    del(l2[i+1])
    i+=1


# Create your views here.
def index(req):
    return render(req, 'tracker/index.html', {'data':l2})

