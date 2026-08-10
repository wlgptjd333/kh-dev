# 전처리
import pandas as pd

# 데이터 준비
df = pd.read_csv("data/people.csv")

# 전처리
df["나이"] =  df["나이"].fillna(30)

# astype
df["나이"] = df["나이"].astype(int)

# 결과
print(df.info())
