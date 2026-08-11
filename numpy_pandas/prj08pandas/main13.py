import pandas as pd

# 데이터 준비
df = pd.read_csv("data/people.csv")

# 새 칼럼 만들기
df["월급"] = df["연봉"] / 12

# 그룹
result = df.groupby("도시")["연봉"].agg(["max","min"])


##########
print(result)