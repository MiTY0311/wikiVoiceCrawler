import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import os, sys

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from util.parserSetup import parserSetup

# URL = "https://bluearchive.wiki/wiki/Characters"
# soup = parserSetup(URL)

def get_student_list():
    try:
        # 설정 및 헤더 로드
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

        from util.config import Config
        config = Config()
        headers = config.headers
        
        URL = "https://bluearchive.wiki/wiki/Characters"
        
        response = requests.get(URL, headers=headers)
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

        # defaultdict를 일반 dict로 변환
        for school in students_by_school:
            students_by_school[school] = dict(students_by_school[school])

        students_data = dict(students_by_school)
        schools_list = list(students_data.keys())     #학교 목록
        total_students = sum(len(students) for students in students_data.values())
        
        # 성공 시 True와 함께 기존 3개 값 반환
        return True, schools_list, students_data, total_students, None
        
    except Exception as e:
        # 실패 시 False만 반환
        print(f"Error in get_student_list: {e}")
        return False, None, None, None, e


a,b,c ,d,e = get_student_list()
print(a,b)



if __name__ == "__main__":
    result = get_student_list()
    
    if result[0]:  # 성공한 경우
        success, schools_list, students_data, total_students,  _= result
        print(f"성공: {len(schools_list)}개 학교, {total_students}명 학생")
        print("학교 목록:", schools_list)
    else:  # 실패한 경우
        print("학생 데이터 로드 실패")
