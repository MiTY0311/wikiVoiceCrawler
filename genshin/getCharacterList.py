import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.parserSetup import parserSetup

def get_character_list():
    try:
        URL = "https://genshin-impact.fandom.com/wiki/Character"
        soup = parserSetup(URL)

        total = 0

        characters_by_group = {}
        all_classes = ["fandom-table", "article-table", "sortable", "alternating-colors-table", "jquery-tablesorter"]
        all_tr = soup.find_all("table",class_=all_classes)[0].find("tbody").find_all("tr")[1:]

        for tr in all_tr:
            name = tr.find_all('td')[1].find('a').text.strip()
            if name != "Traveler":                                          # 주인공은 제외
                faction = tr.find_all('td')[5].text.strip()
                characters_by_group.setdefault(faction, []).append(name)
                total+=1           
                
        return characters_by_group, total
    
    except:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"Error in get_student_list:\n{error_traceback}")
        return False, None

lst1 , lst2 = get_character_list()
print(lst1)