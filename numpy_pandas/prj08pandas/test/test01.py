from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False


# 파일 경로
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


# =========================================================
# 데이터 불러오기
# =========================================================

employees = pd.read_csv(DATA_DIR / "employees.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
departments = pd.read_csv(DATA_DIR / "departments.csv")
customers = pd.read_csv(DATA_DIR / "customers.csv")
city_grade = pd.read_csv(DATA_DIR / "city_grade.csv")


# =========================================================
# Q1 기본
# =========================================================

# Q1-1 employees 앞 5줄
print("\n[Q1-1]")
print(employees.head())


# Q1-2 (행, 열) 크기
print("\n[Q1-2]")
print(employees.shape)


# Q1-3 각 열의 자료형 + 결측치 여부
print("\n[Q1-3]")

result = pd.DataFrame({
    "자료형": employees.dtypes,
    "결측치수": employees.isna().sum()
})

print(result)


# Q1-4 나이·연봉 통계 요약
print("\n[Q1-4]")
print(employees[["나이", "연봉"]].describe())


# Q1-5 부서코드별 인원 수
print("\n[Q1-5]")
print(employees["부서코드"].value_counts())


# Q1-6 orders 카테고리별 개수
print("\n[Q1-6]")
print(orders["카테고리"].value_counts(dropna=False))


# 표기가 이상한 값 찾기
# 정상 표기:
# 가전, 전자, 식품, 의류, 뷰티
# 영어로 잘못 표기된 food, clothes도 확인
valid_categories = [
    "가전",
    "전자",
    "식품",
    "의류",
    "뷰티",
    "food",
    "clothes"
]

print("\n[Q1-6 이상값]")
print(
    orders.loc[
        ~orders["카테고리"].isin(valid_categories),
        "카테고리"
    ].value_counts(dropna=False)
)

# 영어 표기 확인
print("\n[Q1-6 영어 표기]")
print(
    orders.loc[
        orders["카테고리"].isin(["food", "clothes"]),
        "카테고리"
    ].value_counts()
)


# =========================================================
# Q2 선택 및 필터링
# =========================================================

# Q2-1 이름과 연봉
print("\n[Q2-1]")
print(employees[["이름", "연봉"]])


# Q2-2 연봉 5000 이상 + 인원 수
print("\n[Q2-2]")

result = employees[employees["연봉"] >= 5000]

print(result)
print("인원 수:", len(result))


# Q2-3 부서코드 D01 + 나이 30 미만
print("\n[Q2-3]")

result = employees[
    (employees["부서코드"] == "D01") &
    (employees["나이"] < 30)
]

print(result)


# Q2-4 연봉 상위 5명
print("\n[Q2-4]")

result = (
    employees
    .sort_values("연봉", ascending=False)
    [["이름", "연봉"]]
    .head(5)
)

print(result)


# Q2-5 iloc로 6~10번째 행
print("\n[Q2-5]")

# 사람 기준 6~10번째
# Python 위치 기준으로는 5:10
result = employees.iloc[5:10]

print(result)


# Q2-6 연봉 NaN 행의 사번·이름·부서코드
print("\n[Q2-6]")

result = employees.loc[
    employees["연봉"].isna(),
    ["사번", "이름", "부서코드"]
]

print(result)


# =========================================================
# Q3 데이터 정제
# =========================================================

# Q3-1 열별 결측치 수
print("\n[Q3-1]")

print(employees.isna().sum())


# ---------------------------------------------------------
# Q3-2 중복행 제거
# ---------------------------------------------------------

print("\n[Q3-2]")

duplicate_count = employees.duplicated().sum()

employees_clean = employees.drop_duplicates().copy()

print("중복 행 개수:", duplicate_count)
print("제거 후 행 수:", len(employees_clean))


# ---------------------------------------------------------
# Q3-3 도시 표기 통일
# ---------------------------------------------------------

print("\n[Q3-3]")

employees_clean["도시"] = (
    employees_clean["도시"]
    .str.strip()
    .replace("SEOUL", "서울")
)

print(employees_clean["도시"].value_counts())


# ---------------------------------------------------------
# Q3-4 나이 평균 / 연봉 중앙값으로 결측치 채우기
# ---------------------------------------------------------

print("\n[Q3-4]")

employees_clean["나이"] = employees_clean["나이"].fillna(
    employees_clean["나이"].mean()
)

employees_clean["연봉"] = employees_clean["연봉"].fillna(
    employees_clean["연봉"].median()
)

print(employees_clean[["나이", "연봉"]].isna().sum())


# ---------------------------------------------------------
# Q3-5 결측 제거 후 나이 정수형
# ---------------------------------------------------------

print("\n[Q3-5]")

employees_clean = employees_clean.dropna(
    subset=["나이"]
).copy()

employees_clean["나이"] = employees_clean["나이"].astype(int)

print(employees_clean["나이"].dtype)


# ---------------------------------------------------------
# Q3-6 이메일 소문자 + Gmail 사용자 수
# ---------------------------------------------------------

print("\n[Q3-6]")

employees_clean["이메일"] = (
    employees_clean["이메일"]
    .str.strip()
    .str.lower()
)

gmail_users = (
    employees_clean["이메일"]
    .drop_duplicates()
    .str.endswith("@gmail.com")
    .sum()
)

print("gmail 사용자 수:", gmail_users)


# ---------------------------------------------------------
# Q3-7 orders 정제
# ---------------------------------------------------------

print("\n[Q3-7]")

orders_clean = orders.drop_duplicates().copy()

orders_clean["카테고리"] = (
    orders_clean["카테고리"]
    .str.strip()
    .replace({
        "food": "식품",
        "clothes": "의류"
    })
)

print(orders_clean["카테고리"].value_counts())


# =========================================================
# Q4 변형 및 집계
# =========================================================

# Q4-1 연봉 / 12 → 월급
print("\n[Q4-1]")

employees_clean["월급"] = employees_clean["연봉"] / 12

print(
    employees_clean[
        ["연봉", "월급"]
    ].head()
)


# Q4-2 연봉 내림차순 상위 3명
print("\n[Q4-2]")

result = (
    employees_clean
    .sort_values("연봉", ascending=False)
    [["이름", "연봉"]]
    .head(3)
)

print(result)


# Q4-3 부서코드별 평균 연봉
print("\n[Q4-3]")

result = (
    employees_clean
    .groupby("부서코드")["연봉"]
    .mean()
)

print(result)


# Q4-4 부서코드별 인원 수 + 평균 나이
print("\n[Q4-4]")

result = (
    employees_clean
    .groupby("부서코드")
    .agg(
        인원수=("사번", "size"),
        평균나이=("나이", "mean")
    )
)

print(result)


# Q4-5 orders 매출 계산
print("\n[Q4-5]")

orders_clean["단가"] = orders_clean["단가"].fillna(
    orders_clean["단가"].median()
)

orders_clean["매출"] = (
    orders_clean["수량"] *
    orders_clean["단가"]
)

result = (
    orders_clean
    .groupby("카테고리")["매출"]
    .sum()
)

print(result)


# Q4-6 연봉 등급
print("\n[Q4-6]")

employees_clean["등급"] = employees_clean["연봉"].map(
    lambda x: "고연봉" if x >= 5000 else "일반"
)

print(employees_clean["등급"].value_counts())


# Q4-7 부서코드 × 성별 평균 연봉
print("\n[Q4-7]")

result = pd.pivot_table(
    employees_clean,
    index="부서코드",
    columns="성별",
    values="연봉",
    aggfunc="mean"
)

print(result)


# Q4-8 카테고리별 주문 건수 + 평균 매출
print("\n[Q4-8]")

result = (
    orders_clean
    .groupby("카테고리")
    .agg(
        주문건수=("카테고리", "size"),
        평균매출=("매출", "mean")
    )
)

print(result)


# =========================================================
# Q5 합치기 · 시계열 · 시각화
# =========================================================


# ---------------------------------------------------------
# Q5-1 employees + departments
# ---------------------------------------------------------

print("\n[Q5-1]")

emp_dept = employees_clean.merge(
    departments,
    on="부서코드",
    how="left"
)

result = (
    emp_dept
    .drop_duplicates()
    .groupby("부서명")
    .size()
)

print(result)


# =========================================================
# Q5-2 도시 표준화 + city_grade merge
# =========================================================

print("\n[Q5-2]")

# 도시 표기 통일
employees_clean["도시"] = (
    employees_clean["도시"]
    .str.strip()
    .replace("SEOUL", "서울")
)

# city_grade의 '등급'을 '도시등급'으로 변경
city_grade_clean = city_grade.rename(
    columns={"등급": "도시등급"}
)

# merge
employees_city = employees_clean.merge(
    city_grade_clean,
    on="도시",
    how="left"
)

# 도시등급별 평균 연봉
result = (
    employees_city
    .groupby("도시등급")["연봉"]
    .mean()
)

print(result)


# ---------------------------------------------------------
# Q5-3 주문일 날짜형 + 월
# ---------------------------------------------------------

print("\n[Q5-3]")

orders_clean["주문일"] = pd.to_datetime(
    orders_clean["주문일"]
)

orders_clean["월"] = (
    orders_clean["주문일"]
    .dt.to_period("M")
)

print(
    orders_clean[
        ["주문일", "월"]
    ].head()
)


# ---------------------------------------------------------
# Q5-4 월별 주문 건수
# ---------------------------------------------------------

print("\n[Q5-4]")

result = (
    orders_clean
    .groupby("월")
    .size()
)

print(result)


# ---------------------------------------------------------
# Q5-5 orders + customers → 도시별 총매출
# ---------------------------------------------------------

print("\n[Q5-5]")

orders_customer = orders_clean.merge(
    customers,
    on="고객ID",
    how="left"
)

result = (
    orders_customer
    .groupby("도시")["매출"]
    .sum()
)

print(result)


# ---------------------------------------------------------
# Q5-6 resample 월별 총매출
# ---------------------------------------------------------

print("\n[Q5-6]")

monthly_sales = (
    orders_clean
    .sort_values("주문일")
    .set_index("주문일")
    .resample("ME")["매출"]
    .sum()
)

print(monthly_sales)


# ---------------------------------------------------------
# Q5-7 카테고리별 총매출 그래프
# ---------------------------------------------------------

print("\n[Q5-7]")

category_sales = (
    orders_clean
    .groupby("카테고리")["매출"]
    .sum()
)

plt.figure(figsize=(8, 5))

category_sales.plot(
    kind="bar"
)

plt.title("Category Sales")
plt.xlabel("Category")
plt.ylabel("Sales")

plt.tight_layout()

chart_path = BASE_DIR / "chart.png"

plt.savefig(chart_path)
plt.close()

print("chart.png 저장 완료:")
print(chart_path)


# =========================================================
# Q6 종합
# =========================================================


# ---------------------------------------------------------
# Q6-1 전체 총매출
# ---------------------------------------------------------

print("\n[Q6-1]")

total_sales = orders_clean["매출"].sum()

print("전체 총매출:", total_sales)


# ---------------------------------------------------------
# Q6-2 매출 1위 카테고리 + 가장 큰 단일 주문
# ---------------------------------------------------------

print("\n[Q6-2]")

category_sales = (
    orders_clean
    .groupby("카테고리")["매출"]
    .sum()
)

top_category = category_sales.idxmax()
top_category_sales = category_sales.max()

max_order_index = orders_clean["매출"].idxmax()
max_order = orders_clean.loc[max_order_index]

print("매출 1위 카테고리:", top_category)
print("1위 카테고리 총매출:", top_category_sales)

print("\n가장 큰 단일 주문:")
print(max_order)


# =========================================================
# Q6-3 orders + customers + city_grade
# =========================================================

print("\n[Q6-3]")

# city_grade의 등급 → 도시등급
city_grade_clean = city_grade.rename(
    columns={"등급": "도시등급"}
)

# orders + customers
orders_city = orders_clean.merge(
    customers,
    on="고객ID",
    how="left"
)

# + city_grade
orders_city_grade = orders_city.merge(
    city_grade_clean,
    on="도시",
    how="left"
)

# 도시등급별 총매출
result = (
    orders_city_grade
    .groupby("도시등급")["매출"]
    .sum()
)

print(result)

# ---------------------------------------------------------
# Q6-4 요약 리포트
# ---------------------------------------------------------

print("\n[Q6-4]")

monthly_sales = (
    orders_clean
    .sort_values("주문일")
    .set_index("주문일")
    .resample("ME")["매출"]
    .sum()
)

top_month = monthly_sales.idxmax()
top_month_sales = monthly_sales.max()

summary = pd.DataFrame({
    "항목": [
        "총매출",
        "매출 1위 카테고리",
        "매출 1위 카테고리 매출",
        "매출이 가장 큰 달",
        "해당 월 매출"
    ],
    "결과": [
        total_sales,
        top_category,
        top_category_sales,
        str(top_month.to_period("M")),
        top_month_sales
    ]
})

print(summary)


print("\n======================================")
print("모든 문제 실행 완료")
print("======================================")