# 오디오 다운받을려면 필요함
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 다운로드 기본경로
outputPath= "output"

class Config:
    def __init__(self):
        self.headers = headers
        self.outputPath = outputPath
