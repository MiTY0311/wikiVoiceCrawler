import os, sys
import shutil

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.config import Config
config = Config()
path = config.path

def setup(name):

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
    download = os.path.join(char_path, "audio")
    os.makedirs(download, exist_ok=True)
    
    # 오디오 temp
    temp = os.path.join(char_path, "temp")
    os.makedirs(temp, exist_ok=True)
    
    # txt
    txt = os.path.join(char_path, f"{name}.txt")
    with open(txt, 'w', encoding='utf-8') as f:
        pass
    
    # return download_path, temp_path, txt_path
    return download, temp, txt
