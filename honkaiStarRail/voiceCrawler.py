import os, sys
from pprint import pprint
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.parserSetup import parserSetup

def voice_crawler(character):
    URL = f"https://honkai-star-rail.fandom.com/wiki/{character}/Voice-Overs/Japanese"
    soup = parserSetup(URL)
    tables = soup.find_all("table", class_="wikitable")

    for table_idx, table in enumerate(tables):
        print(f"\n테이블 {table_idx+1} 처리 중...")

        tbody = table.find_all("tbody")
        trs = tbody[0].find_all("tr")[1:][1::2]

        
        
        pprint(trs[1])
        print(len(trs))
    # print(len(table))


    
    # language=""


    return None

character = "Acheron"
print(voice_crawler(character))