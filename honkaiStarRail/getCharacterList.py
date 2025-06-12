import os, sys
from pprint import pprint
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.parserSetup import parserSetup

URL = "https://honkai-star-rail.fandom.com/wiki/Character"

def get_character_list(URL):
    try:

        soup = parserSetup(URL)

        characters_by_group = {}

        trs=[]
        all_classes = ['nowraplinks', 'hlist', 'thc1', 'mw-collapsible', 'navbox-inner', 'mw-made-collapsible']
        table = soup.find_all(class_=all_classes)
        tbody = table[-1].find_all("tbody")
        all_tr = tbody[0].find_all("tr")
        for tr in all_tr:
            has_td = tr.find('td') is not None
            has_th = tr.find('th') is not None
    
            if has_td and has_th:
                trs.append(tr)
        
        for tr in trs:
            group = tr.find("th").find("a").text
            characters_by_group[group] = []

            span_list = tr.find_all("span", class_="card-image-container")
            for span in span_list:
                img = span.find("img")
                name = img["alt"].replace(" ", "_")

                characters_by_group[group].append(name)
            
        return True, characters_by_group
    except:
        error_traceback = traceback.format_exc()
        print(f"Error in get_student_list:\n{error_traceback}")
        return False, None

def language(character):
    try:
        URL = f"https://honkai-star-rail.fandom.com/wiki/{character}/Voice-Overs"
        soup = parserSetup(URL)
        div = soup.find_all("div", class_="custom-tabs-language custom-tabs")

        languages = []
        default = div[0].find_all("strong", class_="mw-selflink selflink")
        print(default)
        languages.append(default[0].text)
        div = div[0].find_all("a")
        for language in div:
            languages.append(language.text)

        return True, language
    except:
        error_traceback = traceback.format_exc()
        print(f"Error in get_student_list:\n{error_traceback}")
        return False, None
    
asdf, lst = get_character_list(URL)


