import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.parserSetup import parserSetup

def getCharacters():
    try:
        URL = "https://honkai-star-rail.fandom.com/wiki/Character"
        soup = parserSetup(URL)

        data = {}

        trs=[]
        all_classes = ['nowraplinks', 'hlist', 'thc1', 'mw-collapsible', 'navbox-inner', 'mw-made-collapsible']
        all_tr = soup.find_all(class_=all_classes)[-1].find("tbody").find_all("tr")
        
        for tr in all_tr:
            has_td = tr.find('td') is not None
            has_th = tr.find('th') is not None
    
            if has_td and has_th:
                trs.append(tr)
        
        for tr in trs:
            group = tr.find("th").find("a").text
            data[group] = []
            span_list = tr.find_all("span", class_="card-image-container")
            for span in span_list:
                img = span.find("img")
                name = img["alt"]
                if name == "Trailblazer":
                    continue
                data[group].append(name)
        
        # print(data)
        return True, data, None
    except:
        import traceback
        e = traceback.format_exc()
        print(f"Error in get_student_list:\n{e}")
        return False, None, "error"

def languages(character):
    try:
        URL = f"https://honkai-star-rail.fandom.com/wiki/{character}/Voice-Overs"
        soup = parserSetup(URL)
        div = soup.find_all("div", class_="custom-tabs-language custom-tabs")
        
        default = div[0].find_all("strong", class_="mw-selflink selflink")          # fandom 위키는 무조건 영어가 디폴트
        
        languages = []
        languages.append(default[0].text)                                           # 나머지 존재하는 다른 언어의 데이터셋 서치
        div = div[0].find_all("a")

        for language in div:
            languages.append(language.text)

        return True, languages, None
    except:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error in get_student_list:\n{error_traceback}")
        return False, None, "error"
    
if __name__ == "__main__":
    result, data = getCharacters()
    # character = characters['Astral Express'][2]
    # a, b = languages(character)