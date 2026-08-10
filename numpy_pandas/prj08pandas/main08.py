# 행 + 열 동시 선택
import pandas as pd

df = pd.read_csv("data/people.csv")
df = df.set_index("이름")
print(df.loc["라라",["나이","연봉"]])

print(df.loc[["가영","나은","다희"],["나이","연봉"]])