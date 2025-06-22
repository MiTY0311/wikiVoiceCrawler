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
from honkaiStarRail.getCharacter import getCharacters, languages
# from voiceCrawler import voice_crawler

config = Config()

def load_data():
    """캐릭터 데이터 로드"""
    success, data = getCharacters()
    
    if success:
        characters = data
        groups = list(data.keys())
        total = sum(len(v) for v in data.values())
        
        status_msg = f"✅ 로드 완료! {len(groups)}개 팩션, {total}명 캐릭터"
        choices = ["-"] + sorted(groups)
        return (characters, status_msg, 
                gr.update(choices=choices, visible=True),
                gr.update(visible=True))
    else:
        return (None, "", 
                gr.update(visible=False), gr.update(visible=False))

def update_characters(group, characters):
    """그룹 선택 시 캐릭터 목록 업데이트"""
    if not characters or group == "-":
        return gr.update(choices=["전체"], visible=False), gr.update(visible=False)
    
    character_list = ["전체"] + sorted(characters.get(group, []))
    return (gr.update(choices=character_list, value="전체", visible=True),
            gr.update(visible=False))

def update_languages(group, character, characters):
    """캐릭터 선택 시 언어 목록 업데이트"""
    if not characters or character == "전체" or group == "-":
        return gr.update(visible=False), gr.update(visible=False)
    
    try:
        character_url, available_languages = languages(character)
        if available_languages:
            return (gr.update(choices=available_languages, value=available_languages[0], visible=True),
                    gr.update(visible=True))
        return gr.update(visible=False), gr.update(visible=False)
    except:
        return gr.update(visible=False), gr.update(visible=False)

def download_voice(group, character, voice_language):
    """음성 데이터 다운로드"""
    if not all([group, character, voice_language]) or group == "-" or character == "전체":
        return "❌ 그룹, 캐릭터, 언어를 모두 선택해주세요."
    
    try:
        start_msg = f"🚀 {group}의 {character} ({voice_language} 음성) 크롤링 시작...\n"
        
        # 향후 voice_crawler 구현 시 활성화
        # success, msg = voice_crawler(character, voice_language)
        # return start_msg + f"성공 여부: {success}\n{msg}"
        
        # 임시 구현
        return start_msg + "성공 여부: True\n✅ 크롤링 완료! (임시 구현)"
    except:
        return "❌ 예상치 못한 오류 발생!"

# 메인 인터페이스
with gr.Blocks(css=css, title="honkaiStarRailVoiceCrawler") as demo:
    # 헤더
    gr.HTML('<div class="title"><h1>🌠 honkaiStarRailVoiceCrawler</h1><p>붕괴: 스타레일 음성 크롤러</p></div>')
    
    characters = gr.State(None)
    
    # 데이터 로드 섹션
    with gr.Row():
        with gr.Column(scale=1, min_width=150):
            load_btn = gr.Button("📚\n캐릭터\n데이터\n불러오기", 
                               variant="primary", elem_classes="square-btn")
        with gr.Column(scale=3):
            status = gr.Textbox(label="상태", value="데이터를 불러오세요", interactive=False)
    
    with gr.Column(visible=False) as panel:
        group = gr.Dropdown(label="🏛️ 그룹", choices=["-"], value="-")
        character = gr.Dropdown(label="👤 캐릭터", visible=False)
        voice_language = gr.Dropdown(label="🌐 음성 언어", visible=False)
        download_btn = gr.Button("⬇️ 다운로드", variant="secondary", visible=False)
        result = gr.Textbox(label="결과", interactive=False)
    
    # 이벤트 연결
    load_btn.click(load_data, outputs=[characters, status, group, panel])

    group.change(update_characters, [group, characters], [character, download_btn])
    character.change(update_languages, [group, character, characters], [voice_language, download_btn])
    voice_language.change(lambda v: gr.update(visible=bool(v)), [voice_language], [download_btn])
    download_btn.click(download_voice, [group, character, voice_language], [result])

if __name__ == "__main__":
    print(f"🚀 웹 UI 시작: http://localhost:{config.honkaistarrail_port}")
    demo.launch(server_port=config.honkaistarrail_port)