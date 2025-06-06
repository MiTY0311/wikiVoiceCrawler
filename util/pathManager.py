import os

def setup(path, name):
    char_path = os.path.join(path, name)
    
    # 캐릭터 이름으로 된 디렉토리
    os.makedirs(char_path, exist_ok=True)
    
    # 오디오
    download_dir = os.path.join(char_path, "audio")
    os.makedirs(download_dir, exist_ok=True)
    
    # 오디오 temp
    temp_dir = os.path.join(char_path, "temp")
    os.makedirs(temp_dir, exist_ok=True)
    
    # txt
    txt_path = os.path.join(char_path, f"{name}.txt")
    
    # 빈 데이터셋 파일 생성
    with open(txt_path, 'w', encoding='utf-8') as f:
        pass
    
    return download_dir, temp_dir, txt_path
    # return {
    #     'character_path': char_path,
    #     'download_dir': download_dir,
    #     'temp_dir': temp_dir,
    #     'dataset_file': dataset_file
    # }