import pandas as pd

# 직원 데이터
emp = pd.DataFrame({
    "이름": ["가영", "나은", "다희", "라온", "마루", "바다", "사랑"],
    "부서코드": ["D01", "D02", "D01", "D03", "D02", "D05", "D01"]
})

# 부서 데이터
dept = pd.DataFrame({
    "부서코드": ["D01", "D02", "D03", "D04"],
    "부서명": ["개발팀", "영업팀", "인사팀", "총무팀"]
})

result = pd.merge(emp, dept, how="left")

print(result)
