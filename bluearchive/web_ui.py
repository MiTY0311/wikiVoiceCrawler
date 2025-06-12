import gradio as gr
import os
import sys

# 상위 디렉토리 모듈 import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from util.config import Config
from getStudentList import get_student_list
from voiceCrawler import voice_crawler

config = Config()

def download_dataset(school, student, version):
    """데이터셋 다운로드 처리"""
    # 입력 검증
    if not all([school, student, version]) or school == "-" or student == "전체":
        return "❌ 학원, 학생, 버전을 모두 선택해주세요."
    
    try:
        print(version)

        # character_name = version.split(' (')[0] if '(' in version else version
        character_name = version.replace(' ', '_')
        print(character_name)
        # 크롤링 시작 메시지
        start_msg = f"🚀 {school}의 {student} ({version}) 크롤링 시작...\n"
        
        # voice_crawler 함수 실행
        success, success_count, failed_count, logs = voice_crawler(character_name)
        
        if success:
            result_msg = (
                f"✅ 크롤링 완료!\n"
                f"📊 성공: {success_count}개\n"
                f"⚠️ 실패: {failed_count}개\n"
                f"💾 캐릭터: {character_name}\n"
                f"🏛️ 학원: {school}\n"
                f"🎭 버전: {version}"
            )
            
            if failed_count > 0:
                result_msg += f"\n\n📝 실패 사유는 로그 파일을 확인하세요."
                
        else:
            result_msg = (
                f"❌ 크롤링 실패!\n"
                f"🎯 캐릭터: {character_name}\n"
                f"🏛️ 학원: {school}\n"
                f"🎭 버전: {version}\n"
                f"💡 네트워크 연결이나 사이트 접근을 확인해주세요."
            )
            
        return start_msg + result_msg
        
    except Exception as e:
        error_msg = (
            f"❌ 예상치 못한 오류 발생!\n"
            f"🎯 캐릭터: {character_name if 'character_name' in locals() else 'Unknown'}\n"
            f"🏛️ 학원: {school}\n"
            f"🎭 버전: {version}\n"
            f"🔧 오류 내용: {str(e)}"
        )
        return error_msg

def load_student_data():
    """학생 데이터 로드"""
    # get_student_list 함수는 이제 4개의 값만 반환합니다.
    success, schools_list, students_data, total_students = get_student_list()
    
    if success:
        return (
            True,
            students_data,
            f"✅ 로드 완료! {len(schools_list)}개 학교, {total_students}명 학생",
            gr.update(choices=["-"] + sorted(schools_list), visible=True),
            gr.update(visible=True)  # selection_panel 표시
        )
    else:
        # 에러 메시지를 직접 터미널 확인 요청으로 변경
        error_msg = "❌ 로드 실패: 터미널에서 에러 로그를 확인하세요."
        return (
            False,
            None,
            error_msg,
            gr.update(visible=False),
            gr.update(visible=False)  # selection_panel 숨김
        )

def update_students(school, students_data):
    """학원 선택 시 학생 목록 업데이트"""
    if not students_data or school == "-":
        return gr.update(choices=["전체"], visible=False), gr.update(visible=False)
    
    students = list(students_data.get(school, {}).keys())
    return (
        gr.update(choices=["전체"] + sorted(students), value="전체", visible=True),
        gr.update(visible=False)
    )

def update_versions(school, student, students_data):
    """학생 선택 시 버전 목록 업데이트"""
    if not students_data or student == "전체":
        return gr.update(choices=[], visible=False), gr.update(visible=False)
    
    versions = students_data.get(school, {}).get(student, [])
    return (
        gr.update(choices=versions, value=versions[0] if versions else None, visible=True),
        gr.update(visible=bool(versions))
    )

def create_interface():
    """Gradio 인터페이스 생성"""
    with gr.Blocks(title="Blue Archive Voice Crawler") as demo:
        gr.Markdown("# 🎮 블루 아카이브 음성 크롤러")
        
        # 데이터 상태
        loaded = gr.State(False)
        students_data = gr.State(None)
        
        # 데이터 로드 섹션
        with gr.Row():
            load_btn = gr.Button("📚 학생 데이터 불러오기", variant="primary")
            status = gr.Textbox(label="상태", value="데이터를 불러오세요", interactive=False)
        
        # 선택 섹션
        with gr.Column(visible=False) as selection_panel:
            school = gr.Dropdown(label="🏛️ 학원", choices=["-"], value="-")
            student = gr.Dropdown(label="👤 학생", choices=["전체"], visible=False)
            version = gr.Dropdown(label="🎭 버전", choices=[], visible=False)
            download_btn = gr.Button("⬇️ 다운로드", variant="secondary", visible=False)
            result = gr.Textbox(label="결과", interactive=False)
        
        # 이벤트 연결
        load_btn.click(
            fn=load_student_data,
            outputs=[loaded, students_data, status, school, selection_panel]
        )
        
        school.change(
            fn=update_students,
            inputs=[school, students_data],
            outputs=[student, download_btn]
        )
        
        student.change(
            fn=update_versions,
            inputs=[school, student, students_data],
            outputs=[version, download_btn]
        )
        
        version.change(
            fn=lambda v: gr.update(visible=bool(v)),
            inputs=[version],
            outputs=[download_btn]
        )
        
        download_btn.click(
            fn=download_dataset,
            inputs=[school, student, version],
            outputs=[result]
        )
    
    return demo

if __name__ == "__main__":
    demo = create_interface()
    print(f"🚀 웹 UI 시작: http://localhost:{config.bluearchive_port}")
    demo.launch(server_port=config.bluearchive_port)