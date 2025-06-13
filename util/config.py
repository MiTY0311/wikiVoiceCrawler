# 오디오 다운받을려면 필요함
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# 다운로드 기본경로
outputPath= "output"

main_port = 7680
bluearchive_port = 7681
honkaistarrail_port = 7682
genshin_port = 7683

class Config:
    def __init__(self):
        self.headers = headers
        self.outputPath = outputPath

        self.main_port = main_port
        self.bluearchive_port = bluearchive_port
        self.honkaistarrail_port = honkaistarrail_port
        self.genshin_port = genshin_port
