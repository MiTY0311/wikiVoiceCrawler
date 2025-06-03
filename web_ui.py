import gradio as gr

# 임시 함수 (실제 기능 없음, UI 테스트용)
def download_character_audio(character):
    """UI 테스트를 위한 더미 함수"""
    if not character:
        return "캐릭터 이름을 입력해주세요.", None
    
    return f"""
    [UI 테스트 모드]
    
    캐릭터: {character}
    
    실제 다운로드는 수행되지 않습니다. 이것은 UI 디자인 확인용 더미 출력입니다.
    
    실제 구현 시:
    - 위키에서 오디오 파일 다운로드
    - WAV로 변환
    - 데이터셋 생성
    - ZIP 파일로 압축
    
    이 과정이 실행됩니다.
    """, None

def create_ui():
    with gr.Blocks(title="블루 아카이브 오디오 다운로더") as app:
        gr.Markdown("""
        # 블루 아카이브 오디오 다운로더
        
        이 도구는 블루 아카이브 위키에서 캐릭터 음성 파일을 다운로드하고 WAV 형식으로 변환합니다.
        
        **사용법:**
        1. 캐릭터 이름을 영문으로 입력하세요 (예: Mika, Arisu 등).
        2. '다운로드 시작' 버튼을 클릭하세요.
        3. 처리가 완료되면 ZIP 파일로 다운로드할 수 있습니다.

        """)
        
        with gr.Row():
            character_input = gr.Textbox(label="캐릭터 이름 (영문)", placeholder="예: Mika", value="Mika")
            start_button = gr.Button("다운로드 시작", variant="primary")
        
        with gr.Row():
            output_text = gr.Textbox(label="처리 결과", lines=10)
            download_button = gr.File(label="다운로드")
        
        # 진행 상황 표시 예시 추가
        with gr.Row():
            gr.Markdown("## 진행 상황 미리보기 (실제 작동하지 않음)")
        
        with gr.Row():
            progress_bar = gr.Progress()
            status_text = gr.Markdown("상태: 대기 중...")
        
        # 예시 결과 미리보기 추가
        with gr.Accordion("결과 미리보기 (예시)", open=False):
            gr.Markdown("""
            ```
            처리 완료!
            
            총 24개 항목 다운로드 완료
            건너뛴 항목: 3개
            데이터셋 항목 수: 42개
            
            파일은 ZIP 아카이브로 압축되었습니다.
            ```
            """)
            
            gr.HTML("""
            <div style="border: 1px solid #ddd; padding: 10px; border-radius: 5px; margin-top: 10px;">
                <h4>다운로드된 파일 구조 예시:</h4>
                <pre>
Mika_audio_files.zip
├── Mika_audio/
│   ├── MemorialLobby_0.wav
│   ├── MemorialLobby_1_001.wav
│   ├── MemorialLobby_1_002.wav
│   └── ...
├── Mika_dataset.txt
└── Mika_log.txt
                </pre>
            </div>
            """)
        
        start_button.click(
            fn=download_character_audio,
            inputs=[character_input],
            outputs=[output_text, download_button]
        )
        
        gr.Markdown("""
        ## 시스템 요구 사항
        - Python 3.6 이상
        - FFmpeg (오디오 변환에 필요)
        - 필요한 Python 라이브러리: gradio, requests, beautifulsoup4, pydub
        
        ## 참고
        이 도구는 교육 및 개인 사용 목적으로만 제공됩니다. 다운로드한 오디오 파일의 저작권은 원 저작권자에게 있습니다.
        """)
    
    return app

# 메인 실행 함수
def main():
    app = create_ui()
    app.launch(share=True)  # share=True 옵션은 임시 공개 URL 생성

if __name__ == "__main__":
    main()