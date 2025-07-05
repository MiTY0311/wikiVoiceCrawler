import gradio as gr
import os
import sys

# 모듈 import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.config import Config
from honkaiStarRail.getCharacter import getCharacters, languages
from voiceCrawler import voice_crawler

config = Config()
characters = None  # 전역 캐릭터 데이터

def load_characters():
    """캐릭터 데이터 로드 및 UI 업데이트"""
    global characters
    success, data, msg = getCharacters()
    
    if not success:
        return msg
    
    characters = data
    groups = sorted(data.keys())
    total = sum(len(v) for v in data.values())
    
    return (f"✅ 로드 완료! {len(groups)}개 팩션, {total}명 캐릭터",
            gr.update(choices=["-"] + groups), 
            gr.update(choices=["전체"]), 
            gr.update(choices=[]),
            gr.update(value="📁 데이터셋 생성"))

def download_voice(group, character, voice_language):
    if not characters:
        return "❌ 먼저 캐릭터를 불러와주세요."
    if not all([group != "-", character != "전체", voice_language]):
        return "❌ 그룹, 캐릭터, 언어를 모두 선택해주세요."
    
    try:
        success, msg = voice_crawler(character, voice_language)
        return msg
    except:
        return "❌ 다운로드 오류!"

def on_button_click(group, character, voice_language):
    """버튼 클릭 핸들러"""
    # characters가 None이면 로드, 있으면 다운로드
    if characters is None:
        return load_characters()
    else:
        return (download_voice(group, character, voice_language), 
                gr.update(), gr.update(), gr.update(), gr.update())

def on_group_change(group):
    """그룹 변경 시 캐릭터 목록 업데이트"""
    if not characters or group == "-":
        return gr.update(choices=["전체"], value="전체")
    return gr.update(choices=["전체"] + sorted(characters[group]), value="전체")

def on_character_change(character):
    """캐릭터 변경 시 언어 목록 업데이트"""
    if not characters or character == "전체":
        return gr.update(choices=[])
    
    try:
        _, available_languages = languages(character)
        return gr.update(choices=available_languages, 
                        value=available_languages[0] if available_languages else None)
    except:
        return gr.update(choices=[])

# UI 구성
with gr.Blocks(title="honkaiStarRailVoiceCrawler") as demo:
    gr.HTML('<h1 style="text-align:center">honkai StarRail VoiceCrawler</h1>')
    
    with gr.Row():
        group = gr.Dropdown(label="🏛️ 그룹", choices=["-"], value="-")
        character = gr.Dropdown(label="👤 캐릭터", choices=["전체"], value="전체")
        voice_language = gr.Dropdown(label="🌐 음성 언어", choices=[])
    
    btn = gr.Button("📚 캐릭터 불러오기", variant="primary")
    result = gr.Textbox(label="결과", interactive=False)
    
    # 이벤트 연결
    btn.click(on_button_click, [group, character, voice_language], 
              [result, group, character, voice_language, btn])
    group.change(on_group_change, [group], [character])
    character.change(on_character_change, [character], [voice_language])

if __name__ == "__main__":
    print(f"🚀 웹 UI 시작: http://localhost:{config.honkaistarrail_port}")
    demo.launch(server_port=config.honkaistarrail_port)