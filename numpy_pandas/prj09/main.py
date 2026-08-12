import pandas as pd
from pandas import isna

# 데이터 준비
df = pd.read_csv('data/emp.csv')

# 결측치 확인
print(df.isna().sum())

# 결측치 나이 중위값
df["나이"] = df["나이"].fillna(df["나이"].median())

# 결측치 도시 최빈값으로 채우기
x = df["도시"].mode()[0]
df["도시"] = df["도시"].fillna(x)

# 결측치 연봉 행 없애기
df= df.dropna(subset=["연봉", "이름"])

# 중복 없애기
print(df.duplicated())
df = df.drop_duplicates()

# 컬럼명 바꾸기 도시 = 지역
df = df.rename(columns={"도시":"지역"})

# 컬럼 삭제 // 이름 컬럼 삭제
df = df.drop(columns=["이름"])

# 나이 컬럼 타입 변환
df["나이"] = df["나이"].astype("int")
df["연봉"] = df["연봉"].astype("int")

# 값 치환 // 서울 -> 한양
df["지역"] = df["지역"].replace("서울", "한양")

# 새로운 칼럼 만들기
df["월급"] = (df["연봉"]/12).astype(int)

# 정렬
# df = df.sort_index(axis=1)
df = df.sort_values("월급", ascending=False)

# 결측치 확인
print("\n\n ##### 전처리 후 #####")
print(df.isna().sum())
print(df.head())
