import gradio as gr

def create_header(header_text):

    css ="""
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
        gr.HTML(f'<div class="title"><h1>🎮 wikiVoiceCrawler</h1><p>{header_text}</p></div>')

        with gr.Row():
            with gr.Column(scale=1, min_width=150):
                load_btn = gr.Button("📚\n학생\n데이터\n불러오기", 
                                   variant="primary", 
                                   elem_classes="square-btn")
            with gr.Column(scale=3):
                status = gr.Textbox(label="상태", value="데이터를 불러오세요", interactive=False)
    
    return status, load_btn


# 앱 실행
if __name__ == "__main__":
    print(f"🚀 웹 UI 시작: http://localhost:7666")
    demo.launch(server_port=7666)