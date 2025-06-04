import gradio as gr
import json
import os
import sys

# 상수 정의
CONFIG_PATH = "bluearchive/students.json"
DEFAULT_MESSAGE = "학원을 선택해주세요."

# 데이터 로드 함수
def load_student_data():
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("학생 데이터 로드 완료")
        return data
    except Exception as e:
        print(f"학생 데이터 로드 실패: {e}")
        sys.exit(1)

# 데이터셋 다운로드 함수
def download_dataset(school, student, version):
    """데이터셋 다운로드 처리 함수"""
    # 실제 다운로드 로직 구현 위치
    message = f"{school} 학원의 {student} 학생의 {version} 버전 데이터셋 다운로드 시작..."
    progress = gr.update(value=0.5, visible=True)
    
    # TODO: 여기에 실제 다운로드 로직 추가
    
    return message, progress

def create_interface():
    """Gradio 인터페이스 생성 함수"""
    # 학생 데이터 로드
    students_data = load_student_data()
    schools_list = list(students_data.keys())
    
    # Gradio 블록 정의
    with gr.Blocks(
        title="Blue Archive Character Browser",
        theme=gr.themes.Soft(primary_hue="blue", secondary_hue="cyan", neutral_hue="slate")
    ) as demo:
        gr.Markdown("# 블루 아카이브 캐릭터 브라우저")
        
        with gr.Column():
            # UI 요소 정의
            school_filter = gr.Dropdown(
                choices=["-"] + sorted(schools_list),
                value="-",
                label="학원",
                interactive=True
            )
            
            student_filter = gr.Dropdown(
                choices=["전체"],
                value="전체",
                label="학생 목록",
                visible=False,
                interactive=True
            )
            
            version_filter = gr.Dropdown(
                choices=[],
                label="학생 버전",
                visible=False,
                interactive=True
            )
            
            download_button = gr.Button(
                "데이터셋 다운로드",
                visible=False
            )
            
            progress_bar = gr.Slider(
                minimum=0,
                maximum=1,
                value=0,
                label="다운로드 진행 상태",
                interactive=False,
                visible=False
            )
            
            output_message = gr.Textbox(
                label="상태 메시지",
                interactive=False,
                value=DEFAULT_MESSAGE
            )
        
        # 이벤트 핸들러 정의
        def get_students_by_school(school):
            """학원 선택 시 해당 학원의 학생 목록 가져오기"""
            if school == "-":
                return [
                    gr.update(choices=["전체"], value="전체", visible=False),
                    gr.update(visible=False),
                    gr.update(visible=False),
                    f"학원 선택: {school} - 학생 목록 드롭다운 숨김"
                ]
            
            students_in_school = list(students_data.get(school, {}).keys())
            
            return [
                gr.update(choices=["전체"] + sorted(students_in_school), value="전체", visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                f"학원 선택: {school} - 학생 목록: {', '.join(students_in_school)}"
            ]
        
        def get_versions_by_student(school, student):
            """학생 선택 시 해당 학생의 버전 목록 가져오기"""
            if student == "전체" or school == "-":
                return [
                    gr.update(choices=[], visible=False),
                    gr.update(visible=False),
                    f"학교: {school}, 학생: {student} - 버전 드롭다운 숨김"
                ]
            
            versions = students_data.get(school, {}).get(student, [])
            debug_msg = f"학교: {school}, 학생: {student}, 버전 목록: {versions}"
            
            return [
                gr.update(choices=versions, value=versions[0] if versions else None, visible=True),
                gr.update(visible=False),
                debug_msg
            ]
        
        def show_download_button(version):
            """버전 선택 시 다운로드 버튼 표시"""
            if version:
                return gr.update(visible=True), f"버전 선택: {version} - 다운로드 버튼 표시됨"
            return gr.update(visible=False), "버전이 선택되지 않음 - 다운로드 버튼 숨김"
        
        # 이벤트 연결
        school_filter.change(
            get_students_by_school,
            inputs=[school_filter],
            outputs=[student_filter, download_button, progress_bar, output_message]
        )
        
        student_filter.change(
            get_versions_by_student,
            inputs=[school_filter, student_filter],
            outputs=[version_filter, download_button, output_message]
        )
        
        version_filter.change(
            show_download_button,
            inputs=[version_filter],
            outputs=[download_button, output_message]
        )
        
        download_button.click(
            download_dataset,
            inputs=[school_filter, student_filter, version_filter],
            outputs=[output_message, progress_bar]
        )
    
    return demo

# 메인 실행 부분
if __name__ == "__main__":
    demo = create_interface()
    demo.launch(ssl_verify=False)