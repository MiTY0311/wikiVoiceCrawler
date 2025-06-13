import os, sys
from pprint import pprint
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.parserSetup import parserSetup

def get_character_list():
    try:
        URL = "https://genshin-impact.fandom.com/wiki/Character"
        soup = parserSetup(URL)

        characters_by_group = {}
        all_classes = ["fandom-table", "article-table", "sortable", "alternating-colors-table", "jquery-tablesorter"]
        all_tr = soup.find_all("table",class_=all_classes)[0].find("tbody").find_all("tr")[1:]

        for tr in all_tr:
            name = tr.find_all('td')[1].find('a').text.strip()
            if name == "Traveler":
                pass
            else:
                faction = tr.find_all('td')[5].text
                

            # if faction == 
            # print(name, faction)
            

        # print(all_tr[0])
        # print(tbody)
        characters_by_group = {}


    except:
        error_traceback = traceback.format_exc()
        print(f"Error in get_student_list:\n{error_traceback}")
        return False, None

print(get_character_list())