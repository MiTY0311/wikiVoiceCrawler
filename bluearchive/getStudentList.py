import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict
import os,sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.config import Config

config = Config()

headers = config.headers

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

import json
with open('bluearchive/schools.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# groups를 JSON 파일로 저장
with open('bluearchive/students.json', 'w', encoding='utf-8') as f:
    json.dump(groups, f, ensure_ascii=False, indent=2)

# print("JSON 파일들이 저장되었습니다!")
# pprint(groups[0])
