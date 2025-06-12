import gradio as gr
import os
import sys
import traceback

# 상위 디렉토리 모듈 import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.config import Config
from getCharacterList import get_character_list, language
# from voiceCrawler import voice_crawler

config = Config()
URL = "https://honkai-star-rail.fandom.com/wiki/Character"

def download_dataset(faction, character, voice_language):
    """데이터셋 다운로드 처리"""
    # 입력 검증
    if not all([faction, character, voice_language]) or faction == "-" or character == "전체":
        return "❌ 팩션, 캐릭터, 언어를 모두 선택해주세요."
    
    try:
        # 크롤링 시작 메시지
        start_msg = f"🚀 {faction}의 {character} ({voice_language} 음성) 크롤링 시작...\n"
        
        # 현재는 voice_crawler 함수가 완전히 구현되지 않았으므로 
        # 언어 정보를 가져온 후 미구현 메시지를 반환합니다.
        try:
            # 수정된 language 함수 호출
            character_url, available_languages = language(character)
        except Exception as e:
            error_traceback = traceback.format_exc()
            return f"❌ 언어 정보 가져오기 실패: {str(e)}\n\n{error_traceback}"
        
        # 향후 voice_crawler 구현 시 아래 코드를 활성화할 수 있습니다.
        # result = voice_crawler(URL, voice_language)
        # if result == "1":
        #     # 언어 수 검증 실패
        #     success = False
        #     result_msg = "❌ 지원되지 않는 언어 구성입니다."
        # elif result is None:
        #     # 크롤링 실패
        #     success = False
        #     result_msg = "❌ 크롤링 실패!"
        # else:
        #     # 크롤링 성공
        #     success = True
        #     result_msg = f"✅ 크롤링 완료!"
        
        # 임시 구현 - 실제 크롤링 대신 언어 정보만 표시
        result_msg = (
            f"⚠️ 크롤링 기능 구현 중입니다!\n\n"
            f"📊 캐릭터: {character}\n"
            f"🏛️ 팩션: {faction}\n"
            f"🌐 선택한 언어: {voice_language}\n\n"
            f"ℹ️ 사용 가능한 언어: {', '.join(available_languages)}\n\n"
            f"🔗 캐릭터 URL: {character_url}"
        )
            
        return start_msg + result_msg
        
    except Exception as e:
        error_traceback = traceback.format_exc()
        error_msg = (
            f"❌ 예상치 못한 오류 발생!\n"
            f"🎯 캐릭터: {character}\n"
            f"🏛️ 팩션: {faction}\n"
            f"🌐 언어: {voice_language}\n"
            f"🔧 오류 내용: {str(e)}\n\n"
            f"{error_traceback}"
        )
        return error_msg

def load_character_data():
    """캐릭터 데이터 로드"""
    try:
        success, characters_by_faction = get_character_list(URL)
        
        if success:
            factions = list(characters_by_faction.keys())
            total_characters = sum(len(chars) for chars in characters_by_faction.values())
            
            return (
                True,
                characters_by_faction,
                f"✅ 로드 완료! {len(factions)}개 팩션, {total_characters}명 캐릭터",
                gr.update(choices=["-"] + sorted(factions), visible=True),
                gr.update(visible=True)  # selection_panel 표시
            )
        else:
            error_msg = "❌ 로드 실패: 터미널에서 에러 로그를 확인하세요."
            return (
                False,
                None,
                error_msg,
                gr.update(visible=False),
                gr.update(visible=False)  # selection_panel 숨김
            )
    except Exception as e:
        error_traceback = traceback.format_exc()
        error_msg = f"❌ 캐릭터 데이터 로드 중 오류 발생: {str(e)}\n\n{error_traceback}"
        return (
            False,
            None,
            error_msg,
            gr.update(visible=False),
            gr.update(visible=False)
        )

def update_characters(faction, characters_by_faction):
    """팩션 선택 시 캐릭터 목록 업데이트"""
    if not characters_by_faction or faction == "-":
        return gr.update(choices=["전체"], visible=False), gr.update(visible=False), gr.update(visible=False)
    
    characters = characters_by_faction.get(faction, [])
    return (
        gr.update(choices=["전체"] + sorted(characters), value="전체", visible=True),
        gr.update(visible=False),
        gr.update(visible=False)
    )

def update_languages(character, selected_character):
    """캐릭터 선택 시 언어 목록 업데이트"""
    if not character or character == "전체":
        return gr.update(choices=[], visible=False), gr.update(visible=False)
    
    try:
        # 해당 캐릭터의 사용 가능한 언어 가져오기
        character_url, available_languages = language(selected_character)
        
        if available_languages:
            return (
                gr.update(choices=available_languages, value=available_languages[0], visible=True),
                gr.update(visible=True)
            )
        else:
            return (
                gr.update(choices=["언어 정보 없음"], visible=False),
                gr.update(visible=False)
            )
    except Exception as e:
        print(f"언어 목록 업데이트 오류: {e}")
        error_traceback = traceback.format_exc()
        print(error_traceback)
        return (
            gr.update(choices=["오류 발생"], visible=False),
            gr.update(visible=False)
        )

def create_interface():
    """Gradio 인터페이스 생성"""
    with gr.Blocks(title="Honkai Star Rail Voice Crawler") as demo:
        gr.Markdown("# 🌠 붕괴: 스타레일 음성 크롤러")
        
        # 데이터 상태
        loaded = gr.State(False)
        characters_data = gr.State(None)
        
        # 데이터 로드 섹션
        with gr.Row():
            load_btn = gr.Button("📚 캐릭터 데이터 불러오기", variant="primary")
            status = gr.Textbox(label="상태", value="데이터를 불러오세요", interactive=False)
        
        # 선택 섹션
        with gr.Column(visible=False) as selection_panel:
            faction = gr.Dropdown(label="🏛️ 팩션", choices=["-"], value="-")
            character = gr.Dropdown(label="👤 캐릭터", choices=["전체"], visible=False)
            
            # 선택된 캐릭터를 저장하기 위한 상태 변수
            selected_character = gr.State(None)
            
            voice_language = gr.Dropdown(label="🌐 음성 언어", choices=[], visible=False)
            download_btn = gr.Button("⬇️ 다운로드", variant="secondary", visible=False)
            result = gr.Textbox(label="결과", interactive=False, lines=10)  # 더 많은 정보를 표시하기 위해 라인 수 증가
        
        # 이벤트 연결
        load_btn.click(
            fn=load_character_data,
            outputs=[loaded, characters_data, status, faction, selection_panel]
        )
        
        faction.change(
            fn=update_characters,
            inputs=[faction, characters_data],
            outputs=[character, voice_language, download_btn]
        )
        
        # 캐릭터 선택 시 선택된 캐릭터 상태 업데이트
        def update_selected_character(char, fac, data):
            if char == "전체" or not data or not fac in data:
                return None
            return char
        
        character.change(
            fn=update_selected_character,
            inputs=[character, faction, characters_data],
            outputs=[selected_character]
        )
        
        character.change(
            fn=update_languages,
            inputs=[character, selected_character],
            outputs=[voice_language, download_btn]
        )
        
        voice_language.change(
            fn=lambda v: gr.update(visible=bool(v) and v != "언어 정보 없음" and v != "오류 발생"),
            inputs=[voice_language],
            outputs=[download_btn]
        )
        
        download_btn.click(
            fn=download_dataset,
            inputs=[faction, selected_character, voice_language],
            outputs=[result]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    print(f"🚀 웹 UI 시작: http://localhost:{config.honkaistarrail_port}")
    demo.launch(server_port=config.honkaistarrail_port)