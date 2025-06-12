import os, sys
from pprint import pprint
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.parserSetup import parserSetup

def voice_crawler(character,language):
    URL = "https://honkai-star-rail.fandom.com/wiki/"
    soup = parserSetup(URL)
    div = soup.find_all("div", class_="custom-tabs-language custom-tabs")

    languages = []
    default = div[0].find_all("strong", class_="mw-selflink selflink")
    languages.append(default[0].text)
    div = div[0].find_all("a")
    for language in div:
        languages.append(language.text)

    if len(languages)==4:
        pass
    else:
        return "1"
    
    # language=""


    return None

character = "Natasha"
print(voice_crawler(character))