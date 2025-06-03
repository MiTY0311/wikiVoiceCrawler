from pydub import AudioSegment
import requests
import os

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