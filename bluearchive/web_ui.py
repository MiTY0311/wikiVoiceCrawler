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

import gradio as gr
import os
import sys

# 모듈 import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.config import Config
from bluearchive.getCharacters import getCharacters
from voiceCrawler import voice_crawler

config = Config()

def load_data():
    """학생 데이터 로드"""
    success, data = getCharacters()
    
    if success:
        characters = {group: dict(characters) for group, characters in data.items()}
        groups = list(characters.keys())
        total = sum(len(v) for v in characters.values())
        
        status_msg = f"✅ 로드 완료! {len(groups)}개 학교, {total}명 학생"
        choices = ["-"] + sorted(groups)
        return (characters, status_msg, 
                gr.update(choices=choices, visible=True),
                gr.update(visible=True))
    else:
        return (None, "", 
                gr.update(visible=False), gr.update(visible=False))

def update_students(groups, characters):
    """학원 선택 시 학생 목록 업데이트"""
    if not characters or groups == "-":
        return gr.update(choices=["전체"], visible=False), gr.update(visible=False)
    
    students = ["전체"] + sorted(characters.get(groups, {}).keys())
    return (gr.update(choices=students, value="전체", visible=True),
            gr.update(visible=False))

def update_versions(groups, student, characters):
    """학생 선택 시 버전 목록 업데이트"""
    if not characters or student == "전체" or groups == "-":
        return gr.update(visible=False), gr.update(visible=False)
    
    versions = characters.get(groups, {}).get(student, [])
    if versions:
        return (gr.update(choices=versions, value=versions[0], visible=True),
                gr.update(visible=True))
    return gr.update(visible=False), gr.update(visible=False)

def download_voice(groups, student, version):
    """음성 데이터 다운로드"""
    if not all([groups, student, version]) or groups == "-" or student == "전체":
        return "❌ 학원, 학생, 버전을 모두 선택해주세요."
    
    try:
        character_name = version.replace(' ', '_')
        start_msg = f"🚀 {groups}의 {student} ({version}) 크롤링 시작...\n"
        success, msg = voice_crawler(character_name)
        return start_msg + f"성공 여부: {success}\n{msg}"
    except:
        return "❌ 예상치 못한 오류 발생!"

# 메인 인터페이스
with gr.Blocks(css=css, title="wikiVoiceCrawler") as demo:
    # 헤더
    gr.HTML('<div class="title"><h1>🎮 wikiVoiceCrawler</h1><p>위키 음성 크롤러</p></div>')
    
    characters = gr.State(None)
    
    # 데이터 로드 섹션
    with gr.Row():
        with gr.Column(scale=1, min_width=150):
            load_btn = gr.Button("📚\n학생\n데이터\n불러오기", 
                               variant="primary", elem_classes="square-btn")
        with gr.Column(scale=3):
            status = gr.Textbox(label="상태", value="데이터를 불러오세요", interactive=False)
    
    with gr.Column(visible=False) as panel:
        school = gr.Dropdown(label="🏛️ 학원", choices=["-"], value="-")
        student = gr.Dropdown(label="👤 학생", visible=False)
        version = gr.Dropdown(label="🎭 버전", visible=False)
        download_btn = gr.Button("⬇️ 다운로드", variant="secondary", visible=False)
        result = gr.Textbox(label="결과", interactive=False)
    
    # 이벤트 연결
    load_btn.click(load_data, outputs=[characters, status, school, panel])

    school.change(update_students, [school, characters], [student, download_btn])
    student.change(update_versions, [school, student, characters], [version, download_btn])
    version.change(lambda v: gr.update(visible=bool(v)), [version], [download_btn])
    download_btn.click(download_voice, [school, student, version], [result])

if __name__ == "__main__":
    print(f"🚀 웹 UI 시작: http://localhost:{config.bluearchive_port}")
    demo.launch(server_port=config.bluearchive_port)