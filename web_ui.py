import gradio as gr
import subprocess
import sys
import os
import time
from util.config import Config

# 설정 로드
config = Config()

# 게임 정보 정의 (아이콘 제거)
GAMES = [
    {
        "id": "bluearchive",
        "name": "블루 아카이브",
        "port": config.bluearchive_port,
        "path": "blueArchive/web_ui.py"
    },
    {
        "id": "starrail",
        "name": "붕괴: 스타레일",
        "port": config.honkaistarrail_port,
        "path": "honkaiStarRail/web_ui.py"
    },
]

# 게임별 프로세스 저장
game_processes = {}

def toggle_game(game):
    game_id = game["id"]
    
    # 실행 중 확인
    is_running = (game_id in game_processes and 
                 game_processes[game_id] is not None and 
                 game_processes[game_id].poll() is None)
    
    if is_running:
        # 종료 처리
        try:
            process = game_processes[game_id]
            process.terminate()
            time.sleep(1)
            
            if process.poll() is None:
                process.kill()
                
            game_processes[game_id] = None
            return f"❌ {game['name']} 종료됨"
        except Exception as e:
            return f"⚠️ {game['name']} 종료 실패: {str(e)}"
    else:
        # 시작 처리
        try:
            root_dir = os.path.dirname(os.path.abspath(__file__))
            game_path = os.path.join(root_dir, game["path"])
            
            if not os.path.exists(game_path):
                return f"❌ 모듈을 찾을 수 없음: {game_path}"
                
            game_processes[game_id] = subprocess.Popen([
                sys.executable, game_path
            ])
            
            # 짧은 대기 후 프로세스 확인
            time.sleep(2)
            if game_processes[game_id].poll() is None:
                return f"✅ {game['name']} 시작됨!\n🌐 http://localhost:{game['port']}"
            else:
                game_processes[game_id] = None
                return f"❌ {game['name']} 시작 실패"
        except Exception as e:
            game_processes[game_id] = None
            return f"❌ 실행 실패: {str(e)}"

def launch_coming_soon():
    return "🔄 업데이트 예정\n새로운 게임 준비 중..."

# 프로그램 종료 시 정리
def cleanup():
    for game_id, process in list(game_processes.items()):
        if process is not None and process.poll() is None:
            try:
                process.terminate()
                time.sleep(0.5)
                if process.poll() is None:
                    process.kill()
            except:
                pass

# CSS 스타일 (너비 조정 추가)
css = """
.title { 
    text-align: center; 
    padding: 20px; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 10px; 
    color: white; 
    margin-bottom: 20px;
}

/* 버튼과 텍스트박스 컨테이너 너비 통일 */
.game-column {
    width: 100% !important;
    max-width: 250px !important;
    margin: 0 auto !important;
}

/* 버튼 스타일 */
.game-btn { 
    height: 50px !important; 
    font-size: 16px !important; 
    margin: 10px 0 !important;
    width: 100% !important;
    min-width: 200px !important;
}

/* 상태 텍스트박스 스타일 */
.status-box {
    margin: 10px 0 !important;
    width: 100% !important;
}

.status-box textarea {
    width: 100% !important;
    min-width: 200px !important;
    resize: none !important;
}

/* 열 간격 조정 */
.gradio-row {
    gap: 15px !important;
}

/* 전체 컨테이너 너비 조정 */
.gradio-container {
    max-width: 1200px !important;
    margin: 0 auto !important;
}
"""

# UI 생성 및 실행
with gr.Blocks(css=css, title="wikiVoiceCrawler") as demo:
    # 제목
    gr.HTML('<div class="title"><h1>wikiVoiceCrawler</h1><p>게임 캐릭터 음성 데이터셋 다운로더</p></div>')
    
    # 게임 버튼 및 상태
    with gr.Row(elem_classes=["gradio-row"]):
        for game in GAMES:
            with gr.Column(elem_classes=["game-column"]):
                btn = gr.Button(
                    game['name'], 
                    variant="primary",
                    elem_classes=["game-btn"]
                )
                
                status = gr.Textbox(
                    label="Status", 
                    value="대기 중...", 
                    interactive=False,
                    lines=2,
                    elem_classes=["status-box"]
                )
                
                # 이벤트 연결
                btn.click(
                    fn=lambda g=game: toggle_game(g), 
                    outputs=status
                )
        
        # 업데이트 예정 버튼
        with gr.Column(elem_classes=["game-column"]):
            coming_soon_btn = gr.Button(
                "업데이트 예정", 
                elem_classes=["game-btn"]
            )
            coming_soon_status = gr.Textbox(
                label="업데이트 예정 상태", 
                value="대기 중...", 
                interactive=False,
                lines=2,
                elem_classes=["status-box"]
            )
            
            coming_soon_btn.click(fn=launch_coming_soon, outputs=coming_soon_status)

# 종료 시 정리 함수 등록
import atexit
atexit.register(cleanup)

if __name__ == "__main__":
    try:
        demo.launch(server_port=config.main_port)
    finally:
        cleanup()