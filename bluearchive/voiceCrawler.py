# wiki pedia

from collections import deque
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.parserSetup import parserSetup
from util.audioHandler import create_dataset
from util.pathManager import setup

def voice_crawler(character):

    download, temp, txt = setup(character)

    URL = f"https://bluearchive.wiki/wiki/{character}/audio"    
    # 데이터 저장용 리스트 초기화
    txtList = deque()
    log = []

    try:
        soup = parserSetup(URL)
        tables = soup.find_all("table")
        success_count = 0
        
        # 각 테이블 처리
        for table_idx, table in enumerate(tables):
            print(f"\n테이블 {table_idx+1} 처리 중...")
            
            tbodies = table.find_all("tbody")
            if not tbodies:
                print(f"테이블 {table_idx+1}에서 tbody를 찾을 수 없습니다. 다음 테이블로 넘어갑니다.")
                continue
                
            tbody = tbodies[0]
            rows = tbody.find_all("tr")
            data = rows[2:]  # 헤더 제외
            
            if not data:
                print(f"테이블 {table_idx+1}에 처리할 데이터가 없습니다. 다음 테이블로 넘어갑니다.")
                continue
                
            print(f"테이블 {table_idx+1}에서 {len(data)}개의 행을 찾았습니다.")

            for row_idx, row in enumerate(data):
                tds = row.find_all("td")
                if len(tds) < 4:
                    print(f"헤더 감지로 패스")
                    continue

                tag = tds[0].text.strip()          # 데이터셋 태그네임
                parsingAudios = tds[1]             # 오디오소스
                parsingTexts = tds[2]              # jp텍스트
                
                texts = deque()
                for t in parsingTexts.find_all("p"):
                    text_content = t.get_text(separator="", strip=True)
                    if text_content:
                        texts.append(text_content)

                # 텍스트가 비어있는 경우 건너뛰기
                if not texts and parsingTexts.get_text(strip=True) == "":
                    print(f"{tag} 의 텍스트가 비어있어 패스")
                    log.append({
                        "table": table_idx+1,
                        "row": row_idx+1,
                        "tag": tag,
                        "reason": "일본어 텍스트 없음"
                    })
                    continue

                # 오디오 URL 추출
                audios = parsingAudios.find_all("source")
                urls = []
                
                for source in audios:
                    # 오디오 ogg랑 mp3중 mp3만 가져오는 코드
                    if source.get("type") == "audio/mpeg":
                        url = "https:" + source.get("src")
                        urls.append(url)

                if not urls:
                    print(f"행 {row_idx+1}({tag})에서 오디오 URL을 찾을 수 없습니다. 건너뜁니다.")
                    continue
                
                # 경로로 경로 생성 후 데이터셋 생성
                success, audioText = create_dataset(urls, download, temp, character, tag, texts)
                
                if success:
                    txtList.append(audioText)
                    success_count += 1

                    print("처리 완료 : ",audioText)
                else:
                    print("asdf")

            with open(txt, 'w', encoding='utf-8') as f:
                for entry in txtList:
                    f.write(entry + '\n')
        print("파싱 완료")
        return True, f"{success_count}개의 오디오와 텍스트 데이터셋을 생성했습니다."
        
    except Exception as e:
        import traceback
        e= traceback.format_exc()
        print(f"Error in voice_crawler:\n{e}")
        return False, "에러가 발생했습니다. 터미널에서 에러를 확인해주세요."
    
if __name__ == "__main__":
    import time
    character = "Mika"
    
    start_time = time.time()
    success, message = voice_crawler(character)
    end_time = time.time()
    execution_time = end_time - start_time
    
    print(f"실행 결과: {message}")
    print(f"총 실행 시간: {execution_time:.2f}초")
    