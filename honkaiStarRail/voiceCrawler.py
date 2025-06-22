import os, sys
from pprint import pprint
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.parserSetup import parserSetup
from util.audioHandler import create_dataset
from util.pathManager import setup

def voice_crawler(character, language):

    download, temp, txt = setup(character)

    if language !="English":    
        URL = f"https://honkai-star-rail.fandom.com/wiki/{character}/Voice-Overs/{language}"
    else:
        URL = f"https://honkai-star-rail.fandom.com/wiki/{character}/Voice-Overs"

    soup = parserSetup(URL)
    tables = soup.find_all("table", class_="wikitable")
    txtList = []

    for idx, table in enumerate(tables):
        print(f"\n테이블 {idx+1} 처리 중...")

        tbody = table.find_all("tbody")
        trs = tbody[0].find_all("tr")[1:]

        prev_tag = None
        counter = 0

        for tr in trs:
            th = tr.find("th")
            td = tr.find("td")

            if td is None:
                continue
            
            if th is not None:
                if th.get('class') and 'mobile-only' in th.get('class'):
                    continue
                
                # fandom 위키는 보이스데이터셋 보여주는 디폴트 언어가 영어임
                if language != "English":
                    small = th.find("small")
                    if small:
                        tag = small.text.strip()
                        tag = tag[1:-1]
                        # 새로운 태그가 왔으므로 카운터 초기화
                        counter = 0
                        # 현재 태그를 이전 태그로 저장
                        prev_tag = tag
                    else:
                        print("보이스 데이터에 대한 태그가 없어 패스합니다.")
                        continue
                else:
                    span_in_th = th.find("span")
                    if span_in_th:
                        tag = span_in_th.text.strip()
                        # 새로운 태그가 왔으므로 카운터 초기화
                        counter = 0
                        # 현재 태그를 이전 태그로 저장
                        prev_tag = tag
                    else:
                        print("보이스 데이터에 대한 태그가 없어 패스합니다.")
                        continue
                
                current_tag = tag
                current_tag = current_tag.replace(' ', '_')
            # th가 없는 경우 (같은 카테고리의 추가 대사)
            else:
                # 이전 태그가 없으면 건너뛰기
                if prev_tag is None:
                    continue
                
                # 카운터 증가
                counter += 1
                # 언더스코어와 번호를 추가한 새 태그 생성
                current_tag = f"{prev_tag}_{counter}"
                current_tag = current_tag.replace(' ', '_')
                
            
            # 텍스트와 오디오 URL 추출
            span = td.find_all('span', attrs={"lang":True})
            if span and len(span) > 0:
                if len(span[0].find_all("span")) == 0:
                    text = span[0].text.strip()

                    if text:
                        audio_link = td.find("a", class_="internal")
                        if audio_link:
                            audio_url = audio_link.get("href")
                            urls=[audio_url]
                            texts=[text]
                            
                            success, audioText = create_dataset(urls, download, temp, character, current_tag, texts)
                            # urls, download, temp, character, tag, texts
                            if success==True:
                                print(audioText)
                                txtList.append(audioText)
                        else:
                            print("보이스 데이터셋에 대해 링크가 확인이 안되어 패스합니다.")
                            continue
                    else:
                        print("보이스 데이터셋에 대한 텍스트가 없어 패스합니다.")
                        continue

        with open(txt, 'w', encoding='utf-8') as f:
            for entry in txtList:
                f.write(entry + '\n')

    return "asdf"

character = "Acheron"
language = "Japanese"
print(voice_crawler(character, language))