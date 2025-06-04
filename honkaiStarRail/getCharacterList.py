import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os, sys
import time
from pprint import pprint
from pydub import AudioSegment
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.config import Config

config = Config()

headers = config.headers

URL = "https://honkai-star-rail.fandom.com/wiki/Honkai:_Star_Rail_Wiki"

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

from pprint import pprint
# article_tables = soup.select("table.article-table")
article_tables = soup.find_all("table", class_="article-table")[0]
tbody = article_tables.find_all("tbody")[0]
trList = tbody.find_all("tr")[1]
tdList = trList.find_all("td")[0]
divList = tdList.find_all("div", class_="card-container")

# import time
# for t in divList:
#     pprint(t)
#     time.sleep(60)
character_names = []

for div in divList:
    # card-text card-font 클래스를 가진 span 찾기
    card_text = div.find("span", class_="card-text card-font")
    
    if card_text:
        # 텍스트 추출 및 공백 제거
        name = card_text.get_text().strip()
        character_names.append(name)

# 결과 출력
pprint(character_names)


