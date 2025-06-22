import requests
from bs4 import BeautifulSoup

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.config import Config

config = Config()
headers = config.headers

def parserSetup(URL):

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    return soup

if __name__ == "__main__":
    # 테스트 URL
    test_url = "https://bluearchive.wiki/wiki/Characters"
    print(f"URL 파싱 중: {test_url}")
    soup = parserSetup(test_url)
    print(soup)