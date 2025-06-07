from pydub import AudioSegment
import requests
import os
import shutil

def mp3ToWav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")
    os.remove(mp3_path)


def audios_to_dataset(headers, urls, filename, tempPath, downloadPath):
    temp_files = []
    temp_wav_files = []
    
    try:
        # MP3 파일 다운로드
        for i, url in enumerate(urls):
            mp3_filename = f"{filename}_{i+1:03d}.mp3"
            mp3_path = os.path.join(tempPath, mp3_filename)
            
            try:
                response = requests.get(url, headers=headers)
                
                if response.status_code == 200:
                    with open(mp3_path, 'wb') as f:
                        f.write(response.content)
                    
                    temp_files.append(mp3_path)
                else:
                    print(f"다운로드 실패 (상태 코드: {response.status_code}): {url}")
                    return False, None, None
            except Exception as e:
                print(f"다운로드 중 오류: {str(e)}")
        
        if not temp_files:
            print(f"변환된 WAV 파일이 없습니다.")
            return False, None, None
        
        # MP3 파일을 WAV로 변환
        for mp3_path in temp_files:
            try:
                wav_filename = os.path.splitext(os.path.basename(mp3_path))[0] + ".wav"
                wav_path = os.path.join(tempPath, wav_filename)
                
                mp3ToWav(mp3_path, wav_path)
                
                temp_wav_files.append(wav_path)
            except Exception as e:
                print(f"변환 실패: {os.path.basename(mp3_path)}, 오류: {str(e)}")
        
        if not temp_wav_files:
            print(f"변환된 WAV 파일이 없습니다.")
            return False, None, None
        
        # WAV 파일 병합
        try:
            if len(temp_wav_files) == 1:
                combined = AudioSegment.from_file(temp_wav_files[0])
            else:
                combined = AudioSegment.from_file(temp_wav_files[0])
                
                for wav_path in temp_wav_files[1:]:
                    audio = AudioSegment.from_file(wav_path)
                    combined += audio
        except Exception as e:
            print(f"오디오 병합 중 오류: {str(e)}")
            return False, None, None
        
        # 최종 WAV 파일 저장
        try:
            output_filename = f"{filename}.wav"
            output_path = os.path.join(downloadPath, output_filename)
            combined.export(output_path, format="wav")
        except Exception as e:
            print(f"파일 저장 중 오류: {str(e)}")
            return False, None, None
        
        # 임시 파일 정리
        for wav_path in temp_wav_files:
            try:
                os.remove(wav_path)
            except Exception as e:
                print(f"임시 파일 삭제 실패: {os.path.basename(wav_path)}")
        
        return True, output_path, output_filename

    except Exception as e:
        print(f"오디오 처리 중 오류: {str(e)}")
        return False, None, None