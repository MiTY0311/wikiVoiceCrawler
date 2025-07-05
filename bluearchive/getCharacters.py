from collections import defaultdict
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.parserSetup import parserSetup

def getCharacters():
    try:
        URL = "https://bluearchive.wiki/wiki/Characters"
        soup = parserSetup(URL)
        
        data = defaultdict(lambda: defaultdict(list))
        
        for tr in soup.find("table").find("tbody").find_all("tr")[1:]:
            td_list = tr.find_all("td")
            name = td_list[1].get_text(strip=True)
            group = td_list[3].get_text(strip=True)
            
            base_name = name.split(' (')[0] if '(' in name else name
            data[group][base_name].append(name)
        
        return True, data
        
    except:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error in voice_crawler:\n{error_traceback}")
        return False, None
    
if __name__ == "__main__":

    result = getCharacters()
    
    if result[0]:
        success, data= result
        characters = {group: dict(characters) for group, characters in data.items()}
        groups = list(characters.keys())
        total = sum(len(v) for v in characters.values())
        from pprint import pprint
        pprint(characters)
    else:  # 실패한 경우
        print("학생 데이터 로드 실패")
