import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict

URL = "https://bluearchive.wiki/wiki/Characters"

# HEADERS = {"User-Agent": "Mozilla/5.0"}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

from pprint import pprint
table = soup.find_all("table")[0]
tbody = table.find_all("tbody")[0]
trList = tbody.find_all("tr")
trList = trList[1:]     #헤더 제거

names = []
groups = defaultdict(lambda: defaultdict(list))

for tr in trList:
    tdList = tr.find_all("td")
    name = tdList[1].get_text(strip=True)
    group = tdList[3].get_text(strip=True)

    if '(' in name:
        base_name = name.split(' (')[0]
        groups[group][base_name].append(name)
    else:
        groups[group][name].append(name)

for group in groups:
    groups[group] = dict(groups[group])
result = dict(groups)

groups = list(result.keys())
pprint(groups[0])
