import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import os, sys
import json

def get_student_list():
    try:
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from util.config import Config
        config = Config()
        headers = config.headers
        
        URL = "https://bluearchive.wiki/wiki/Characters"
        
        response = requests.get(URL, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        table = soup.find_all("table")[0]
        tbody = table.find_all("tbody")[0]
        trList = tbody.find_all("tr")
        trList = trList[1:]  # 헤더 제거
        
        students_by_school = defaultdict(lambda: defaultdict(list))
        
        for tr in trList:
            tdList = tr.find_all("td")
            name = tdList[1].get_text(strip=True)
            school = tdList[3].get_text(strip=True)
            
            if '(' in name:
                base_name = name.split(' (')[0]
                students_by_school[school][base_name].append(name)
            else:
                students_by_school[school][name].append(name)
        
        for school in students_by_school:
            students_by_school[school] = dict(students_by_school[school])
        students_data = dict(students_by_school)
        
        schools_list = list(students_data.keys())
        
        return True, schools_list, students_data, None
    
    except requests.exceptions.RequestException as e:
        print(f"웹 요청 오류: {str(e)}")
        return False, None, None, e
    except (IndexError, KeyError, AttributeError) as e:
        print(f"데이터 파싱 오류: {str(e)}")
        return False, None, None, e
    except Exception as e:
        print(f"예상치 못한 오류: {str(e)}")
        return False, None, None, e

def save_json_files(schools_list, students_data):
    """
    학교 목록과 학생 데이터를 JSON 파일로 저장하는 함수
    
    Args:
        schools_list (list): 학교 목록
        students_data (dict): 학교별 학생 데이터
        
    Returns:
        bool: 저장 성공 여부
    """
    try:
        # 학교 목록만 저장
        with open('bluearchive/schools.json', 'w', encoding='utf-8') as f:
            json.dump(schools_list, f, ensure_ascii=False, indent=2)
        
        # 전체 학생 정보 저장
        with open('bluearchive/students.json', 'w', encoding='utf-8') as f:
            json.dump(students_data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"파일 저장 중 오류 발생: {str(e)}")
        return False

def update_student_data():
    """
    학생 데이터를 업데이트하는 주 함수
    
    Returns:
        tuple: (성공 여부, 학교 수, 학생 수)
    """
    try:
        # 학생 데이터 가져오기
        schools_list, students_data = get_student_list()
        
        # 결과 출력
        school_count = len(schools_list)
        student_count = sum(len(students) for students in students_data.values())
        print(f"총 {school_count}개 학교, {student_count}명의 학생 정보를 찾았습니다.")
        
        # JSON 파일 저장
        save_success = save_json_files(schools_list, students_data)
        if save_success:
            print("schools.json 및 students.json 파일 저장 완료")
            return True, school_count, student_count
        else:
            print("파일 저장 실패")
            return False, 0, 0
    
    except Exception as e:
        print(f"데이터 업데이트 중 오류 발생: {str(e)}")
        return False, 0, 0

# 직접 실행될 때만 데이터 업데이트 수행
if __name__ == "__main__":
    success, school_count, student_count = update_student_data()
    if success:
        print(f"데이터 업데이트 성공: {school_count}개 학교, {student_count}명의 학생")
    else:
        print("데이터 업데이트 실패")
        sys.exit(1)