import gradio as gr
import os
import sys

# 모듈 import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.config import Config
from blueArchive.getCharacters import getCharacters
from voiceCrawler import voice_crawler

config = Config()

# 전역 상태
class AppState:
    def __init__(self):
        self.characters = None
        self.selected_school = None
        self.selected_character = None

state = AppState()

def limit_selection(items):
    """체크박스에서 하나만 선택되도록 제한"""
    return [items[-1]] if len(items) > 1 else items

def create_update(choices=None, value=None, visible=None):
    """gr.update 객체 생성 헬퍼"""
    update_dict = {}
    if choices is not None:
        update_dict['choices'] = choices
    if value is not None:
        update_dict['value'] = value
    if visible is not None:
        update_dict['visible'] = visible
    return gr.update(**update_dict)

def load_characters():
    """캐릭터 데이터 자동 로드"""
    success, data = getCharacters()

    print(data)
    
    if not success:
        return ("❌ 데이터 로드 실패", 
                create_update(choices=[], value=[]), 
                create_update(visible=False), 
                create_update(visible=False), 
                create_update(visible=False))
    
    state.characters = {group: dict(chars) for group, chars in data.items()}
    sch = list(state.characters.keys())
    total = sum(len(v) for v in state.characters.values())
    
    return (f"✅ 로드 완료! {len(sch)}개 학교, {total}명 학생",
            create_update(choices=sch, value=[]),
            create_update(visible=True),
            create_update(visible=False), 
            create_update(visible=False))

def handle_school_select(schools):
    schools = limit_selection(schools)
    state.selected_character = None
    
    if not schools or not state.characters:
        state.selected_school = None
        return (create_update(value=schools),
                create_update(choices=[], value=[]), 
                create_update(visible=False),
                create_update(choices=[], value=[]), 
                create_update(visible=False))
    
    state.selected_school = schools[0]
    characters = list(state.characters[state.selected_school].keys())
    
    return (create_update(value=schools),
            create_update(choices=characters, value=[]), 
            create_update(visible=True),
            create_update(choices=[], value=[]), 
            create_update(visible=False))

def handle_character_select(characters_selected):
    characters_selected = limit_selection(characters_selected)
    
    if not characters_selected or not state.selected_school or not state.characters:
        state.selected_character = None
        return (create_update(value=characters_selected),
                create_update(choices=[], value=[]), 
                create_update(visible=False))
    
    state.selected_character = characters_selected[0]
    versions = state.characters[state.selected_school][state.selected_character]
    
    return (create_update(value=characters_selected),
            create_update(choices=versions, value=[]), 
            create_update(visible=True))

def handle_version_select(versions):
    """버전 선택 시 다운로드 버튼 표시"""
    show = bool(versions)
    return create_update(visible=show), create_update(visible=show)

def download_voices(versions_selected):
    """음성 데이터 다운로드"""
    if not all([state.selected_school, state.selected_character, versions_selected]):
        return "❌ 학교, 캐릭터, 버전을 모두 선택해주세요."
    
    results = []
    for version in versions_selected:
        try:
            success, msg = voice_crawler(version.replace(' ', '_'))
            status = "✅" if success else "❌"
            results.append(f"{status} {state.selected_school}의 {state.selected_character} ({version}): {msg}")
        except Exception as e:
            results.append(f"❌ {state.selected_character} ({version}): 다운로드 오류 - {str(e)}")
    
    return "\n".join(results)

# CSS 스타일
css = """
.title { 
    text-align: center; 
    padding: 20px; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
    border-radius: 10px; 
    color: white; 
    margin-bottom: 20px;
}
.checkbox-group {
    max-height: 300px;
    overflow-y: auto;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
}
.step-title {
    font-weight: bold;
    font-size: 16px;
    margin-bottom: 10px;
    color: #333;
}
"""

# UI 구성
with gr.Blocks(css=css, title="wikiVoiceCrawler") as demo:
    gr.HTML('<div class="title"><h1>Blue Archive Make Dataset Tool</h1></div>')
    
    # 상태 표시
    status = gr.Textbox(label="상태", value="📡 캐릭터 데이터 로딩 중...", interactive=False)
    
    # 선택 단계들
    with gr.Column():
        # 학교 선택
        with gr.Group(visible=False) as sch_is_active:
            sch_list = gr.CheckboxGroup(label="학교", choices=[], elem_classes=["checkbox-group"])
        
        # 캐릭터 선택
        with gr.Group(visible=False) as char_is_active:
            char_list = gr.CheckboxGroup(label="캐릭터", choices=[], elem_classes=["checkbox-group"])
        
        # 버전 선택
        with gr.Group(visible=False) as ver_is_active:
            ver_list = gr.CheckboxGroup(label="버전", choices=[], elem_classes=["checkbox-group"])
    
    # 다운로드 섹션
    download_btn = gr.Button("📁 데이터셋 생성", variant="primary", size="lg", visible=False)
    result = gr.Textbox(label="다운로드 결과", interactive=False, lines=5, visible=False)
    
    # 이벤트 연결
    demo.load(load_characters, outputs=[status, sch_list, sch_is_active, char_is_active, ver_is_active])
    
    sch_list.change(handle_school_select, [sch_list], 
                        [sch_list, char_list, char_is_active, ver_list, ver_is_active])
    
    char_list.change(handle_character_select, [char_list], 
                           [char_list, ver_list, ver_is_active])
    
    ver_list.change(handle_version_select, [ver_list], [download_btn, result])
    
    download_btn.click(download_voices, [ver_list], [result])

if __name__ == "__main__":
    print(f"🚀 웹 UI 시작: http://localhost:{config.bluearchive_port}")
    demo.launch(server_port=config.bluearchive_port)