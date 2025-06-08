import requests
from bs4 import BeautifulSoup

from config import Config
config = Config()

def parserSetup(URL):

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(URL, headers)
    soup = BeautifulSoup(response.text, "html.parser")

    return soup

if __name__ == "__main__":
    # 테스트 URL
    test_url = "https://bluearchive.wiki/wiki/Characters"
    print(f"URL 파싱 중: {test_url}")
    soup = parserSetup(test_url)
    print(soup)