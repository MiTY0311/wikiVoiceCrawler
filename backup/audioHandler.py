from pydub import AudioSegment
import requests
import os

def mp3ToWav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")
    os.remove(mp3_path)
    return wav_path

# 단일 오디오 다운로드
def download_audio(url, filename, downloadPath, headers, tempPath):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            mp3Path = os.path.join(tempPath, filename)
            with open(mp3Path, 'wb') as f:
                f.write(response.content)
            
            filename = os.path.splitext(filename)[0] + ".wav"
            wavPath = os.path.join(downloadPath, filename)
            
            mp3ToWav(mp3Path, wavPath)
            
            print(f"다운로드 및 WAV 변환 완료: {wavPath}")
            return True, wavPath, filename
        else:
            print(f"다운로드 실패 (상태 코드: {response.status_code}): {url}")
            return False, None, None
    except Exception as e:
        print(f"다운로드 중 오류 발생: {url}, 오류: {str(e)}")
        return False, None, None

# 여러 오디오 파일을 하나로 합치는 함수 (WAV 형식으로)
def combine_download_audio(urls, filename, downloadPath, headers, tempPath):
    try:
        wavFiles = []
        
        # 각 URL에서 오디오 파일 다운로드 및 임시 저장
        for i, url in enumerate(urls):
            tempFilename = f"temp_{i+1}.mp3"
            success, wavPath, _ = download_audio(url, tempFilename, downloadPath, headers, tempPath)
            if success:
                wavFiles.append(wavPath)
        
        if not wavFiles:
            return False, None, None
            
        # 오디오 파일 병합
        combined = AudioSegment.from_file(wavFiles[0])
        for wavPath in wavFiles[1:]:
            audio = AudioSegment.from_file(wavPath)
            combined += audio
            
        # 결과 파일을 WAV로 저장
        filename = os.path.splitext(filename)[0] + ".wav"
        filepath = os.path.join(downloadPath, filename)

        combined.export(filepath, format="wav")
        
        # 임시 WAV 파일 삭제
        for wavPath in wavFiles:
            try:
                os.remove(wavPath)
            except Exception as e:
                print(f"임시 파일 삭제 실패: {wavPath}, 오류: {str(e)}")
                
        print(f"오디오 파일 병합 및 WAV 변환 완료: {filepath}")
        return True, filename, filepath
    except Exception as e:
        print(f"오디오 파일 병합 중 오류 발생: {str(e)}")
        return False, None, None