import requests
from bs4 import BeautifulSoup
from collections import deque
# from urllib.parse import urljoin
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.config import Config
from util.audioHandler import audios_to_dataset
from util.pathManager import setup

def voice_crawler(character):
    
    BASE_URL = "https://bluearchive.wiki"
    PAGE_URL = f"{BASE_URL}/wiki/{character}/audio"
    
    # 설정 및 경로 초기화
    config = Config()
    headers = config.headers
    path = config.outputPath
    
    downloadPath, tempPath, txtPath, logPath = setup(path, character)
    
    # 데이터 저장용 리스트 초기화
    txtList = deque()
    log = []
    
    try:
        response = requests.get(PAGE_URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.find_all("table")
        
        print(f"찾은 테이블 수: {len(tables)}")
        
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
            
            # 각 행 처리
            for row_idx, row in enumerate(data):
                tds = row.find_all("td")
                if len(tds) < 4:
                    print(f"헤더 감지로 패스")
                    continue

                tag = tds[0].text.strip()          # 데이터셋 태그네임
                parsingAudios = tds[1]             # 오디오소스
                parsingTexts = tds[2]              # jp텍스트
                
                # 텍스트 파싱
                # texts = []
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
                    if source.get("type") == "audio/mpeg":
                        url = "https:" + source.get("src")
                        urls.append(url)
                
                # 오디오 URL이 없는 경우 건너뛰기
                if not urls:
                    print(f"행 {row_idx+1}({tag})에서 오디오 URL을 찾을 수 없습니다. 건너뜁니다.")
                    log.append({
                        "table": table_idx+1,
                        "row": row_idx+1,
                        "tag": tag,
                        "reason": "오디오 URL 없음"
                    })
                    continue

                print(f"처리 중: {tag}")
                
                # 오디오 다운로드 및 데이터셋 생성
                success, output_path, audioText = audios_to_dataset(
                    headers,
                    urls,
                    tag,
                    tempPath,
                    downloadPath,

                    character,
                    texts,
                )
                
                if success:
                    txtList.append(audioText)
                    success_count += 1

                    print(f"처리 완료 {tag}")
                    print("text : ",audioText)

        with open(txtPath, 'w', encoding='utf-8') as f:
            for entry in txtList:
                f.write(entry + '\n')

        if log:
            with open(logPath, 'w', encoding='utf-8') as f:
                for item in log:
                    f.write(f"테이블 {item['table']}, 행 {item['row']}, 태그: {item['tag']}, 이유: {item['reason']}\n")
    

        print(f"\n=== 크롤링 완료 ===")
        print(f"성공한 항목: {success_count}개")
        print(f"건너뛴 항목: {len(log)}개")
        print(f"데이터셋 파일: {txtPath}")
        print(f"로그 파일: {logPath}")
        
        return True, success_count, len(log), log
        
    except requests.exceptions.RequestException as e:
        print(f"HTTP 요청 실패: {e}")
        return False, 0, 0, []
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        return False, 0, 0, []
    
# 출력 예시
# print("\n=== 파싱 결과 ===")
# pprint(result[:5])  # 처음 5개 항목만 출력 (결과가 너무 많을 경우)
# print(f"... 외 {max(0, len(result)-5)}개 항목 (총 {len(result)}개)")

# print(f"\n총 {len(result)}개 항목 처리 완료")
# print(f"건너뛴 항목: {len(log)}개 (자세한 내용은 {log} 파일 참조)")
# print(f"오디오 파일 저장 위치: {os.path.abspath(download)}")
# print(f"데이터셋 파일 저장 위치: {os.path.abspath(dataset_file)}")
# print(f"데이터셋 항목 수: {len(dataset_entries)}개")