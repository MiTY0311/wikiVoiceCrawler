import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os, sys
import time
from pprint import pprint
from pydub import AudioSegment
import io

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.config import Config
# from util.audioHandler import download_audio, combine_download_audio
from util.audioHandler import audios_to_dataset
from util.pathManager import setup

character = "Mika"  #첫단어 대문자로해야함 (wiki주소 이슈)

BASE_URL = "https://bluearchive.wiki"
PAGE_URL = f"{BASE_URL}/wiki/{character}/audio"

config = Config()
headers = config.headers
path = config.outputPath

downloadPath, tempPath, txtPath, logPath = setup(path, character)

# 데이터셋 파일 생성
# dataset_file = f"{character}_dataset.txt"

txtList = []
result = []
log = []

response = requests.get(PAGE_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")
tables = soup.find_all("table")

pprint(len(tables))

for table_idx, table in enumerate(tables):
    print(f"\n테이블 {table_idx+1} 처리 중...")
    
    tbodies = table.find_all("tbody")
    if not tbodies:
        print(f"테이블 {table_idx+1}에서 tbody를 찾을 수 없습니다. 다음 테이블로 넘어갑니다.")
        continue
        
    tbody = tbodies[0]
    rows = tbody.find_all("tr")
    
    data = rows[2:]
    
    if not data:
        print(f"테이블 {table_idx+1}에 처리할 데이터가 없습니다. 다음 테이블로 넘어갑니다.")
        continue
        
    print(f"테이블 {table_idx+1}에서 {len(data)}개의 행을 찾았습니다.")
    
    for row_idx, row in enumerate(data):
        tds = row.find_all("td")
        if len(tds) < 4:
            print(f"헤더 감지로 패스")
            continue

        tag = tds[0].text.strip()  # 데이터셋 태그네임
        parsingAudios = tds[1]      # 오디오소스
        parsingTexts = tds[2]       # jp텍스트
        
        #텍스트 파싱 파트
        texts = []
        for t in parsingTexts.find_all("p"):
            t = t.get_text(separator="", strip=True)
            if t:
                texts.append(t)

        if not texts and parsingTexts.get_text(strip=True) == "":
            print(f"{tag} 의 텍스트가 비어있어 패스")
            log.append({
                "table": table_idx+1,
                "row": row_idx+1,
                "tag": tag,
                "reason": "일본어 텍스트 없음"
            })
            continue

        # 모든 .mp3 링크 추출
        audios = parsingAudios.find_all("source")
        urls = []
        
        for source in audios:
            if source.get("type") == "audio/mpeg":
                url = "https:" + source.get("src")
                urls.append(url)
        
        if not urls:
            print(f"행 {row_idx+1}({tag})에서 오디오 URL을 찾을 수 없습니다. 건너뜁니다.")
            log.append({
                "table": table_idx+1,
                "row": row_idx+1,
                "tag": tag,
                "reason": "오디오 URL 없음"
            })
            continue

        print(tag)
        # print(urls)
        # print(texts)
        
        success, output_path, filename = audios_to_dataset(
                            headers,
                            urls,
                            tag,
                            tempPath,
                            downloadPath,
                            )
        if success:
            audioText = "".join(texts)
            audioText = f"{character}\\{filename}|{audioText}"
            txtList.append(audioText)

            with open(txtPath, 'w', encoding='utf-8') as f:
                for entry in txtList:
                    f.write(entry + '\n')

            with open(logPath, 'w', encoding='utf-8') as f:
                for item in log:
                    f.write(f"테이블 {item['table']}, 행 {item['row']}, 이름: {item['name']}, 이유: {item['reason']}\n")
# 출력 예시
# print("\n=== 파싱 결과 ===")
# pprint(result[:5])  # 처음 5개 항목만 출력 (결과가 너무 많을 경우)
# print(f"... 외 {max(0, len(result)-5)}개 항목 (총 {len(result)}개)")

# print(f"\n총 {len(result)}개 항목 처리 완료")
print(f"건너뛴 항목: {len(log)}개 (자세한 내용은 {log} 파일 참조)")
# print(f"오디오 파일 저장 위치: {os.path.abspath(download)}")
# print(f"데이터셋 파일 저장 위치: {os.path.abspath(dataset_file)}")
# print(f"데이터셋 항목 수: {len(dataset_entries)}개")