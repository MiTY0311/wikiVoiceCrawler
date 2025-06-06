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
from util.audioHandler import download_audio, combine_audio_from_urls
from util.pathManager import setup

character = "Mika"  #첫단어 대문자로해야함 (wiki주소 이슈)

BASE_URL = "https://bluearchive.wiki"
PAGE_URL = f"{BASE_URL}/wiki/{character}/audio"

config = Config()
headers = config.headers

path = config.outputPath

downloadPath, tempPath, txtPath = setup(path, character)

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
        
        # len(mp3_url)의 길이가 1인지 True False 여부 체크
        is_single_audio = len(urls) == 1
        
        if is_single_audio:
            url = urls[0]
            filename = f"{tag}.mp3"
            success, filepath, filename = download_audio(url, 
                                                         filename, 
                                                         downloadPath, 
                                                         headers, 
                                                         tempPath
                                                         )

            if success:
                audioText = "".join(texts)
                audioText = f"{character}\\{filename}|{audioText}"
                txtList.append(audioText)

                result.append({
                    "table": table_idx+1,
                    "row": row_idx+1,
                    "tag": tag,
                    "audio": urls[0],
                    "ja": texts,
                    "filename": filename,
                    "audioText": audioText
                })
        else:
            if len(urls) != len(texts):
                print(f"경고: 행 {row_idx+1}에서 오디오 URL ({len(urls)}개)과 일본어 텍스트 ({len(texts)}개)의 개수가 일치하지 않습니다.")
                print("오디오 파일을 병합하고 텍스트를 통합합니다.")

                audioText = "".join(texts)
                
                filename = f"{tag}"
                success, output_path, actual_filename = combine_audio_from_urls(urls, filename, headers, tempPath)
                
#                 if success:
#                     # 데이터셋 항목 추가
#                     text = f"{character}\\{actual_filename}|{text}"
#                     datasets.append(text)
                    
#                     result.append({
#                         "table": table_idx+1,
#                         "row": row_idx+1,
#                         "name": name,
#                         "audio_count": len(urls),
#                         "original_audio_urls": urls,
#                         "ja": texts,
#                         "filename": actual_filename,
#                         "dataset_entry": text,
#                         "note": "불일치 데이터 - 오디오 및 텍스트 통합"
#                     })
#             else:
#                 # 다중 오디오 다운로드 (오디오와 텍스트 수가 일치하는 경우)
#                 downloaded_files = []
#                 multi_entries = []
                
#                 for i, (audio_url, jp_text) in enumerate(zip(urls, texts)):
#                     # 파일명 형식: {이름}_{인덱스}.mp3
#                     filename = f"{name}_{i+1:03d}.mp3"  # 001, 002 형식으로 인덱스 포맷팅
#                     success, file_path, actual_filename = download_audio(audio_url, filename, download, headers, temp)
                    
#                     if success:
#                         downloaded_files.append(actual_filename)
                        
#                         # 데이터셋 항목 추가 (파일경로|일본어텍스트)
#                         dataset_entry = f"{character}\\{actual_filename}|{jp_text}"
#                         datasets.append(dataset_entry)
#                         multi_entries.append(dataset_entry)
                
#                 # 다중 오디오: 리스트로 유지
#                 result.append({
#                     "table": table_idx+1,
#                     "row": row_idx+1,
#                     "name": name,
#                     "audio_count": len(urls),
#                     "filenames": downloaded_files,
#                     "ja": texts,
#                     "dataset_entries": multi_entries
#                 })

#         time.sleep(0.1)
# print(dataset_entries)
# # 데이터셋 파일 저장
# with open(dataset_file, 'w', encoding='utf-8') as f:
#     for entry in datasets:
#         f.write(entry + '\n')

# # 건너뛴 항목 기록
# log_file = f"{character}_log.txt"
# with open(log_file, 'w', encoding='utf-8') as f:
#     for item in log:
#         f.write(f"테이블 {item['table']}, 행 {item['row']}, 이름: {item['name']}, 이유: {item['reason']}\n")

# # 임시 폴더 정리
# try:
#     if os.path.exists(temp) and os.path.isdir(temp):
#         for temp_file in os.listdir(temp):
#             os.remove(os.path.join(temp, temp_file))
#         os.rmdir(temp)
#         print(f"임시 폴더 {temp} 삭제 완료")
# except Exception as e:
#     print(f"임시 폴더 정리 중 오류 발생: {str(e)}")

# # 출력 예시
# print("\n=== 파싱 결과 ===")
# pprint(result[:5])  # 처음 5개 항목만 출력 (결과가 너무 많을 경우)
# print(f"... 외 {max(0, len(result)-5)}개 항목 (총 {len(result)}개)")

# print(f"\n총 {len(result)}개 항목 처리 완료")
# print(f"건너뛴 항목: {len(log)}개 (자세한 내용은 {log_file} 파일 참조)")
# print(f"오디오 파일 저장 위치: {os.path.abspath(download)}")
# print(f"데이터셋 파일 저장 위치: {os.path.abspath(dataset_file)}")
# print(f"데이터셋 항목 수: {len(dataset_entries)}개")