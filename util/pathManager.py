import os
import shutil

def setup(path, name):

    char_path = os.path.join(path, name)
    if os.path.exists(char_path):
        print(f"기존 디렉토리 '{char_path}' 삭제 중...")
        try:
            shutil.rmtree(char_path)
            print(f"'{char_path}' 삭제 완료")
        except Exception as e:
            print(f"디렉토리 삭제 중 오류 발생: {str(e)}")
    os.makedirs(char_path, exist_ok=True)
    
    # 오디오
    download_dir = os.path.join(char_path, "audio")
    os.makedirs(download_dir, exist_ok=True)
    
    # 오디오 temp
    temp_dir = os.path.join(char_path, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # txt
    txt_path = os.path.join(char_path, f"{name}.txt")
    with open(txt_path, 'w', encoding='utf-8') as f:
        pass

    # log
    log_path = os.path.join(char_path, "log.txt")
    with open(log_path, 'w', encoding='utf-8') as f:
        pass
    
    return download_dir, temp_dir, txt_path, log_path
