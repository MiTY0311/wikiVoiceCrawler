import gradio as gr
import os

def handle_bluearchive_click():
    """블루아카이브 데이터셋 다운로드 처리"""
    return "블루아카이브 데이터셋\nBlue Archive 캐릭터 음성 및 대사 데이터\n다운로드를 시작합니다..."

def handle_coming_soon_click():
    """업데이트 예정 버튼 클릭 처리"""
    return "업데이트 예정\n새로운 게임 데이터셋 준비 중...\n조금만 기다려주세요!"

# CSS 스타일링
custom_css = """
.title-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 30px;
    border-radius: 15px;
    text-align: center;
    color: white;
    margin-bottom: 30px;
}

.game-item {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 20px;
    padding: 15px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    background: transparent;
}

.game-icon {
    width: 128px !important;
    height: 128px !important;
    min-width: 128px !important;
    max-width: 128px !important;
    border-radius: 10px !important;
    font-size: 12px !important;
    flex-shrink: 0 !important;
    flex-grow: 0 !important;
    transition: transform 0.2s !important;
    padding: 0 !important;
    overflow: hidden !important;
    cursor: pointer !important;
}

.game-icon:hover {
    transform: scale(1.05) !important;
}

.coming-soon-icon {
    background: linear-gradient(135deg, #9E9E9E 0%, #757575 100%) !important;
    color: white !important;
    border: 2px solid #9E9E9E !important;
}

.coming-soon-icon:hover {
    border-color: #757575 !important;
}

.bluearchive-btn {
    background-color: #a7d7ff !important;  /* 연한 하늘색 배경 */
    color: #003366 !important;  /* 진한 남색 텍스트 */
    font-weight: bold !important;  /* 텍스트 굵게 */
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    text-align: center !important;
    line-height: 1.2 !important;
    font-size: 16px !important;
}

.game-info {
    flex: 1;
}

.status-area {
    margin-top: 30px;
    padding: 20px;
    background-color: transparent;
    border-radius: 10px;
    border-left: 4px solid #007bff;
}
"""

with gr.Blocks(css=custom_css, title="wikiVoiceCrawler") as demo:
    # 상단 제목 영역
    with gr.Row():
        gr.HTML("""
        <div class="title-section">
            <h1 style="margin: 0; font-size: 2.5em;">🎮 wikiVoiceCrawler</h1>
            <p style="margin: 15px 0 0 0; font-size: 1.2em; opacity: 0.9;">
                다양한 게임의 캐릭터 음성 데이터셋을 쉽게 다운로드하세요
            </p>
        </div>
        """)
    
    # 게임 선택 영역 (3행 2열)
    with gr.Row():
        # 왼쪽 컬럼
        with gr.Column():
            # 첫 번째 게임 (블루아카이브)
            with gr.Row(elem_classes=["game-item"]):
                # 텍스트가 있는 버튼으로 변경
                bluearchive_btn = gr.Button(
                    "블루 아카이브", 
                    elem_classes=["game-icon", "bluearchive-btn"]
                )
                status_output1 = gr.Textbox(
                    value="대기 중... 원하는 게임을 선택해주세요.",
                    label="",
                    interactive=False,
                    elem_classes=["status-area"]
                )
            bluearchive_btn.click(
                fn=handle_bluearchive_click,
                outputs=status_output1
            )
            
            # 두 번째 게임
            with gr.Row(elem_classes=["game-item"]):
                coming_soon_btn1 = gr.Button(
                    "🔄\n업데이트\n예정", 
                    elem_classes=["game-icon", "coming-soon-icon"]
                )
                status_output2 = gr.Textbox(
                    value="대기 중... 원하는 게임을 선택해주세요.",
                    label="",
                    interactive=False,
                    elem_classes=["status-area"]
                )
            coming_soon_btn1.click(
                fn=handle_coming_soon_click,
                outputs=status_output2
            )
            
        # 오른쪽 컬럼
        with gr.Column():
            # 네 번째 게임
            with gr.Row(elem_classes=["game-item"]):
                coming_soon_btn3 = gr.Button(
                    "🔄\n업데이트\n예정", 
                    elem_classes=["game-icon", "coming-soon-icon"]
                )
                status_output4 = gr.Textbox(
                    value="대기 중... 원하는 게임을 선택해주세요.",
                    label="",
                    interactive=False,
                    elem_classes=["status-area"]
                )
            coming_soon_btn3.click(
                fn=handle_coming_soon_click,
                outputs=status_output4
            )
            
            with gr.Row(elem_classes=["game-item"]):
                coming_soon_btn4 = gr.Button(
                    "🔄\n업데이트\n예정", 
                    elem_classes=["game-icon", "coming-soon-icon"]
                )
                status_output5 = gr.Textbox(
                    value="대기 중... 원하는 게임을 선택해주세요.",
                    label="",
                    interactive=False,
                    elem_classes=["status-area"]
                )
            coming_soon_btn4.click(
                fn=handle_coming_soon_click,
                outputs=status_output5
            )


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
    )