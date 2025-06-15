import os, sys
from pprint import pprint
import traceback

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.parserSetup import parserSetup

def voice_crawler(character, language):

    if language !="English":    
        URL = f"https://honkai-star-rail.fandom.com/wiki/{character}/Voice-Overs/{language}"
    else:
        URL = f"https://honkai-star-rail.fandom.com/wiki/{character}/Voice-Overs"

    soup = parserSetup(URL)

    tables = soup.find_all("table", class_="wikitable")

    for idx, table in enumerate(tables):
        print(f"\n테이블 {idx+1} 처리 중...")

        tbody = table.find_all("tbody")
        trs = tbody[0].find_all("tr")[1:]

        ################################################### 텍스트 파싱관련 예상치못한 오류대비 주석
        # for tr in trs:
        #     th = tr.find("th")

        #     if th == None:
        #         continue

        #     if th.get('class') and 'mobile-only' in th.get('class'):
        #         continue 

        #     if language != "English":
        #         tag = th.find("small").text.strip()
        #         tag = tag[1:-1]
        #     else:
        #         tag = th.find("span").text.strip()
            
        #     td = tr.find("td")
        #     span = td.find_all('span', attrs={"lang":True})
        #     if len(span[0].find_all("span"))==0:
        #         text = span[0].text.strip()
        #         print(f"{tag} :", text)
        #     else:
        #         continue

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
                        continue
                
                current_tag = tag
            # th가 없는 경우 (같은 카테고리의 추가 대사)
            else:
                # 이전 태그가 없으면 건너뛰기
                if prev_tag is None:
                    continue
                
                # 카운터 증가
                counter += 1
                # 언더스코어와 번호를 추가한 새 태그 생성
                current_tag = f"{prev_tag}_{counter}"
            
            # 텍스트와 오디오 URL 추출
            span = td.find_all('span', attrs={"lang":True})
            if span and len(span) > 0:
                if len(span[0].find_all("span")) == 0:
                    text = span[0].text.strip()

                    if text:
                        audio_link = td.find("a", class_="internal")
                        if audio_link:
                            audio_url = audio_link.get("href")
                            print(f"{current_tag} : {text}")
                            print(f"{audio_url}")
                            print()  # 빈 줄 추가로 구분
                        else:
                            print("데이터셋에 필요한 오디오 링크가 없어 패스합니다.")
                    else:
                        print("데이터셋에 참고할 텍스트가 없어 패스합니다.")
                    
                    # audio_link = td.find("a", class_="internal")
                    # if audio_link:
                    #     audio_url = audio_link.get("href")
                    #     print(f"{current_tag} : {text}")
                    #     print(f"{audio_url}")
                    #     print()  # 빈 줄 추가로 구분
                    # else:
                    #     print(f"{current_tag} : {text}")
                    #     print("오디오 URL을 찾을 수 없습니다.")
                    #     print()


    return "asdf"

character = "Acheron"
language = "English"
print(voice_crawler(character, language))