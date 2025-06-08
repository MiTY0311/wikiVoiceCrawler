import gradio as gr
import subprocess
import sys
import os
import time
import psutil
import signal
from util.config import Config

config = Config()

# 게임별 프로세스 추적
game_processes = {
    "bluearchive": None
}

def find_process_by_port(port):
    """포트를 사용하는 프로세스 찾기"""
    try:
        for proc in psutil.process_iter(['pid', 'connections']):
            try:
                for conn in proc.connections():
                    if conn.laddr.port == port:
                        return proc.pid
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    except:
        pass
    return None

def is_game_running(game_name):
    """게임이 실행 중인지 확인"""
    if game_name == "bluearchive":
        port = config.bluearchive_port
        # 프로세스 확인
        if game_processes[game_name] and game_processes[game_name].poll() is None:
            return True
        # 포트 확인
        return find_process_by_port(port) is not None
    return False

def kill_game_process(game_name):
    """게임 프로세스 종료"""
    if game_name == "bluearchive":
        port = config.bluearchive_port
    else:
        return False
    
    try:
        # 1. 저장된 프로세스 종료
        if game_processes[game_name]:
            game_processes[game_name].terminate()
            time.sleep(1)
            if game_processes[game_name].poll() is None:
                game_processes[game_name].kill()
            game_processes[game_name] = None
        
        # 2. 포트 사용 프로세스 종료
        pid = find_process_by_port(port)
        if pid:
            os.kill(pid, signal.SIGTERM)
            time.sleep(1)
            if psutil.pid_exists(pid):
                os.kill(pid, signal.SIGKILL)
        
        return True
    except Exception as e:
        print(f"프로세스 종료 오류: {e}")
        return False

def toggle_bluearchive():
    """블루아카이브 토글 (실행/종료)"""
    if is_game_running("bluearchive"):
        # 실행 중이면 종료
        if kill_game_process("bluearchive"):
            return "❌ 블루아카이브 종료됨"
        else:
            return "⚠️ 종료 중 오류 발생"
    else:
        # 실행 중이 아니면 시작
        try:
            root_dir = os.path.dirname(os.path.abspath(__file__))
            game_processes["bluearchive"] = subprocess.Popen([
                sys.executable, 
                os.path.join(root_dir, "bluearchive", "web_ui.py")
            ])
            
            time.sleep(2)  # 실행 대기
            
            if is_game_running("bluearchive"):
                return f"✅ 블루아카이브 시작됨!\n🌐 http://localhost:{config.bluearchive_port}"
            else:
                return "❌ 시작 실패"
                
        except Exception as e:
            return f"❌ 실행 실패: {str(e)}"

def launch_coming_soon():
    """업데이트 예정"""
    return "🔄 업데이트 예정\n새로운 게임 준비 중..."

# 간단한 CSS
css = """
.title { 
    text-align: center; 
    padding: 20px; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 10px; 
    color: white; 
}
.game-btn { 
    height: 80px !important; 
    font-size: 18px !important; 
    margin: 10px !important; 
}
"""

with gr.Blocks(css=css, title="wikiVoiceCrawler") as demo:
    
    # 제목
    gr.HTML('<div class="title"><h1>🎮 wikiVoiceCrawler</h1><p>게임 캐릭터 음성 데이터셋 다운로더</p></div>')
    
    # 게임 선택 (각각 개별 상태)
    with gr.Row():
        with gr.Column():
            bluearchive_btn = gr.Button("🎓 블루 아카이브", variant="primary", elem_classes=["game-btn"])
            bluearchive_status = gr.Textbox(
                label="블루 아카이브 상태", 
                value="대기 중...", 
                interactive=False,
                lines=2
            )
        
        with gr.Column():
            coming_soon_btn = gr.Button("🔄 업데이트 예정", elem_classes=["game-btn"])
            coming_soon_status = gr.Textbox(
                label="업데이트 예정 상태", 
                value="대기 중...", 
                interactive=False,
                lines=2
            )
    
    # 이벤트 연결 (토글 기능)
    bluearchive_btn.click(fn=toggle_bluearchive, outputs=bluearchive_status)
    coming_soon_btn.click(fn=launch_coming_soon, outputs=coming_soon_status)

# 프로그램 종료 시 정리
def cleanup():
    for game_name in game_processes:
        kill_game_process(game_name)

import atexit
atexit.register(cleanup)

if __name__ == "__main__":
    demo.launch(server_port=config.main_port)