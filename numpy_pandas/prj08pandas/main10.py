# 전처리
import pandas as pd

# 데이터 준비
df = pd.read_csv("data/people.csv")

# 결측치 처리
# df = df.dropna()
df["나이"] = df["나이"].fillna(df["나이"].mean())
df["도시"] = df["도시"].fillna("미상")
df["연봉"] = df["연봉"].fillna(df["연봉"].mean())

# 중복 제거

print("@@@@@@@@@@")
print(df.drop_duplicates())
print("@@@@@@@@@@")


# 결측치 확인
print(df.isna().sum())

print(df.head(10))