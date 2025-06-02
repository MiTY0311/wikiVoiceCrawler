import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import time
from pprint import pprint
from pydub import AudioSegment
import io

character = "Mika"  #첫단어 대문자로해야함 (wiki주소 이슈)

BASE_URL = "https://bluearchive.wiki"
PAGE_URL = f"{BASE_URL}/wiki/{character}/audio"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"   ## 오디오 다운받을려면 필요함
}

response = requests.get(PAGE_URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

download = f"{character}_audio"
os.makedirs(download, exist_ok=True)
temp = f"{character}_temp"
os.makedirs(temp, exist_ok=True)

# 데이터셋 파일 생성
dataset_file = f"{character}_dataset.txt"

# 오디오 파일 다운로드 함수 (MP3 다운로드 후 WAV로 변환)
def download_audio(url, filename, dir=download):
    try:
        audio_response = requests.get(url, headers=headers)
        if audio_response.status_code == 200:
            # MP3 파일 임시 저장
            temp_mp3_path = os.path.join(temp, f"temp_{filename}")
            with open(temp_mp3_path, 'wb') as f:
                f.write(audio_response.content)
            
            # WAV 파일명 생성 (확장자 변경)
            wav_filename = os.path.splitext(filename)[0] + ".wav"
            wav_path = os.path.join(dir, wav_filename)
            
            # MP3를 WAV로 변환
            audio = AudioSegment.from_mp3(temp_mp3_path)
            audio.export(wav_path, format="wav")
            
            # 임시 MP3 파일 삭제
            os.remove(temp_mp3_path)
            
            print(f"다운로드 및 WAV 변환 완료: {wav_filename}")
            return True, wav_path, wav_filename
        else:
            print(f"다운로드 실패 (상태 코드: {audio_response.status_code}): {url}")
            return False, None, None
    except Exception as e:
        print(f"다운로드 중 오류 발생: {url}, 오류: {str(e)}")
        return False, None, None

# 여러 오디오 파일을 하나로 합치는 함수 (WAV 형식으로)
def combine_audio_from_urls(urls, output_filename):
    try:
        if not urls:
            return False, None, None
            
        temp_files = []
        
        # 각 URL에서 오디오 파일 다운로드 및 임시 저장
        for i, url in enumerate(urls):
            temp_filename = f"temp_{i+1}.mp3"
            success, file_path, _ = download_audio(url, temp_filename, temp)
            if success:
                temp_files.append(file_path)
        
        if not temp_files:
            return False, None, None
            
        # 오디오 파일 병합
        combined = AudioSegment.from_file(temp_files[0])
        for file_path in temp_files[1:]:
            audio = AudioSegment.from_file(file_path)
            combined += audio
            
        # 결과 파일을 WAV로 저장
        wav_output_filename = os.path.splitext(output_filename)[0] + ".wav"
        output_path = os.path.join(download, wav_output_filename)
        combined.export(output_path, format="wav")
        
        # 임시 파일 삭제
        for file_path in temp_files:
            try:
                os.remove(file_path)
            except:
                pass
                
        print(f"오디오 파일 병합 및 WAV 변환 완료: {wav_output_filename}")
        return True, output_path, wav_output_filename
    except Exception as e:
        print(f"오디오 파일 병합 중 오류 발생: {str(e)}")
        return False, None, None

dataset_entries = []
result = []
log = []

tables = soup.find_all("table")
for table_idx, table in enumerate(tables):
    print(f"\n테이블 {table_idx+1} 처리 중...")
    
    # 테이블에서 tbody 찾기
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
            print(f"행 {row_idx+1}에 충분한 열이 없습니다. 다음 행으로 넘어갑니다.")
            continue
        
        name = tds[0].text.strip()
        print(f"행 {row_idx+1} 처리 중: {name}")

        # 일본어 텍스트 셀 확인 - 비어있는지 체크
        jp_cell = tds[2]
        jp_paragraphs = jp_cell.find_all("p")
        jp_texts = []
        
        for p in jp_paragraphs:
            text = p.get_text(separator="", strip=True)
            if text:
                jp_texts.append(text)
        
        # 일본어 텍스트가 비어있는지 확인
        if not jp_texts and jp_cell.get_text(strip=True) == "":
            print(f"{name} 의 일본어 텍스트가 비어 있습니다. 건너뜁니다.")
            log.append({
                "table": table_idx+1,
                "row": row_idx+1,
                "name": name,
                "reason": "일본어 텍스트 없음"
            })
            continue

        # 모든 .mp3 링크 추출
        audio_sources = tds[1].find_all("source")
        mp3_urls = []
        
        for source in audio_sources:
            if source.get("type") == "audio/mpeg":
                mp3_url = "https:" + source.get("src")
                mp3_urls.append(mp3_url)
        
        if not mp3_urls:
            print(f"행 {row_idx+1}({name})에서 오디오 URL을 찾을 수 없습니다. 건너뜁니다.")
            log.append({
                "table": table_idx+1,
                "row": row_idx+1,
                "name": name,
                "reason": "오디오 URL 없음"
            })
            continue
            
        # 영어 텍스트 처리 (필요시 사용)
        en_paragraphs = tds[3].find_all("p")
        en_texts = []
        
        for p in en_paragraphs:
            text = p.get_text(separator=" ", strip=True)
            if text:
                en_texts.append(text)
        
        # 오디오 다운로드 및 데이터셋 항목 생성
        is_single_audio = len(mp3_urls) == 1
        
        if is_single_audio:
            # 단일 오디오 다운로드
            audio_url = mp3_urls[0]
            filename = f"{name}.mp3"
            success, file_path, actual_filename = download_audio(audio_url, filename)

            if success:
                # 단일 오디오: 모든 p 태그 내용을 하나로 합치기
                combined_jp = "".join(jp_texts)

                # 데이터셋 항목 추가 (파일경로|일본어텍스트)
                dataset_entry = f"{character}\\{actual_filename}|{combined_jp}"
                dataset_entries.append(dataset_entry)

                result.append({
                    "table": table_idx+1,
                    "row": row_idx+1,
                    "name": name,
                    "audio": mp3_urls[0],
                    "ja": combined_jp,
                    "filename": actual_filename,
                    "dataset_entry": dataset_entry
                })
        else:
            if len(mp3_urls) != len(jp_texts):
                print(f"경고: 행 {row_idx+1}에서 오디오 URL ({len(mp3_urls)}개)과 일본어 텍스트 ({len(jp_texts)}개)의 개수가 일치하지 않습니다.")
                print("오디오 파일을 병합하고 텍스트를 통합합니다.")
                
                # 모든 텍스트 통합
                combined_jp_text = "".join(jp_texts)
                
                # 모든 오디오 URL에서 파일 다운로드 및 병합
                combined_filename = f"{name}_combined.mp3"
                success, output_path, actual_filename = combine_audio_from_urls(mp3_urls, combined_filename)
                
                if success:
                    # 데이터셋 항목 추가
                    dataset_entry = f"{character}\\{actual_filename}|{combined_jp_text}"
                    dataset_entries.append(dataset_entry)
                    
                    result.append({
                        "table": table_idx+1,
                        "row": row_idx+1,
                        "name": name,
                        "audio_count": len(mp3_urls),
                        "original_audio_urls": mp3_urls,
                        "ja": combined_jp_text,
                        "filename": actual_filename,
                        "dataset_entry": dataset_entry,
                        "note": "불일치 데이터 - 오디오 및 텍스트 통합"
                    })
            else:
                # 다중 오디오 다운로드 (오디오와 텍스트 수가 일치하는 경우)
                downloaded_files = []
                multi_entries = []
                
                for i, (audio_url, jp_text) in enumerate(zip(mp3_urls, jp_texts)):
                    # 파일명 형식: {이름}_{인덱스}.mp3
                    filename = f"{name}_{i+1:03d}.mp3"  # 001, 002 형식으로 인덱스 포맷팅
                    success, file_path, actual_filename = download_audio(audio_url, filename)
                    
                    if success:
                        downloaded_files.append(actual_filename)
                        
                        # 데이터셋 항목 추가 (파일경로|일본어텍스트)
                        dataset_entry = f"{character}\\{actual_filename}|{jp_text}"
                        dataset_entries.append(dataset_entry)
                        multi_entries.append(dataset_entry)
                
                # 다중 오디오: 리스트로 유지
                result.append({
                    "table": table_idx+1,
                    "row": row_idx+1,
                    "name": name,
                    "audio_count": len(mp3_urls),
                    "filenames": downloaded_files,
                    "ja": jp_texts,
                    "dataset_entries": multi_entries
                })
        
        # 너무 빠른 요청을 방지하기 위한 딜레이
        time.sleep(0.2)

# 데이터셋 파일 저장
with open(dataset_file, 'w', encoding='utf-8') as f:
    for entry in dataset_entries:
        f.write(entry + '\n')

# 건너뛴 항목 기록
log_file = f"{character}_log.txt"
with open(log_file, 'w', encoding='utf-8') as f:
    for item in log:
        f.write(f"테이블 {item['table']}, 행 {item['row']}, 이름: {item['name']}, 이유: {item['reason']}\n")

# 임시 폴더 정리
try:
    if os.path.exists(temp) and os.path.isdir(temp):
        for temp_file in os.listdir(temp):
            os.remove(os.path.join(temp, temp_file))
        os.rmdir(temp)
        print(f"임시 폴더 {temp} 삭제 완료")
except Exception as e:
    print(f"임시 폴더 정리 중 오류 발생: {str(e)}")

# 출력 예시
print("\n=== 파싱 결과 ===")
pprint(result[:5])  # 처음 5개 항목만 출력 (결과가 너무 많을 경우)
print(f"... 외 {max(0, len(result)-5)}개 항목 (총 {len(result)}개)")

print(f"\n총 {len(result)}개 항목 처리 완료")
print(f"건너뛴 항목: {len(log)}개 (자세한 내용은 {log_file} 파일 참조)")
print(f"오디오 파일 저장 위치: {os.path.abspath(download)}")
print(f"데이터셋 파일 저장 위치: {os.path.abspath(dataset_file)}")
print(f"데이터셋 항목 수: {len(dataset_entries)}개")