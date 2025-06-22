import requests
from pydub import AudioSegment
from pathlib import Path
from io import BytesIO
import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.config import Config
config = Config()
headers = config.headers

def create_dataset(urls, download, temp, character, tag, texts):
    if not urls:
        return False, None, None
    
    try:
        wav_files = []
        for i, url in enumerate(urls):

            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"다운로드 실패: {url}")
                continue
            
            audiotype = response.headers.get('content-type', '').lower()
            if audiotype in ['audio/mpeg', 'audio/mp3']:
                format = "mp3"
            elif audiotype in ['audio/ogg', 'application/ogg']:
                format = "ogg"
            
            mp3_data = BytesIO(response.content)
            mp3_audio = AudioSegment.from_file(mp3_data, format=format)
            
            # 임시 WAV 파일 저장
            wav_path = Path(temp) / f"{tag}_{i+1:03d}.wav"
            mp3_audio.export(wav_path, format="wav")
            wav_files.append(wav_path)
        
        if not wav_files:
            return False, None, None
        
        # WAV 파일 병합
        combined = AudioSegment.from_file(wav_files[0])
        silence = AudioSegment.silent(duration=500)
        for wav_file in wav_files[1:]:
            combined += silence
            combined += AudioSegment.from_file(wav_file)
        
        # 최종 파일 저장
        output_filename = f"{tag}.wav"
        output_path = Path(download) / output_filename
        combined.export(output_path, format="wav")

        if output_path.exists():
            audioText = "".join(texts)
            audioText = f"{character}\\{output_filename}|{audioText}"
        
        # 임시 파일 정리
        for wav_file in wav_files:
            wav_file.unlink(missing_ok=True)
        
        return True, audioText
        
    except Exception as e:
        print(f"오디오 처리 오류: {e}")
        return False, None