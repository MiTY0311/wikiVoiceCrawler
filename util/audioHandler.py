from pydub import AudioSegment
import requests
import os
import shutil
from pathlib import Path
from io import BytesIO

def audios_to_dataset(headers, 
                      urls, 
                      filename, 
                      tempPath, 
                      downloadPath, 
                      character, 
                      texts
                      ):
    if not urls:
        return False, None, None
    
    try:
        wav_files = []
        
        # 다운로드 및 변환 (한 번에 처리)
        for i, url in enumerate(urls):
            # MP3 다운로드
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"다운로드 실패: {url}")
                continue
            
            # 메모리에서 직접 WAV 변환 (임시 파일 없이)
            mp3_audio = AudioSegment.from_file_using_temporary_files(
                response.content, format="mp3"
            )
            
            # 임시 WAV 파일 저장
            wav_path = Path(tempPath) / f"{filename}_{i+1:03d}.wav"
            mp3_audio.export(wav_path, format="wav")
            wav_files.append(wav_path)
        
        if not wav_files:
            return False, None, None
        
        # WAV 파일 병합
        combined = AudioSegment.from_file(wav_files[0])
        for wav_file in wav_files[1:]:
            combined += AudioSegment.from_file(wav_file)
        
        # 최종 파일 저장
        output_filename = f"{filename}.wav"
        output_path = Path(downloadPath) / output_filename
        combined.export(output_path, format="wav")

        if output_path.exists():
            audioText = "".join(texts)
            audioText = f"{character}\\{output_filename}|{audioText}"
        
        # 임시 파일 정리
        for wav_file in wav_files:
            wav_file.unlink(missing_ok=True)
        
        return True, str(output_path), audioText
        
    except Exception as e:
        print(f"오디오 처리 오류: {e}")
        return False, None, None