# loc, iloc
import pandas as pd

df = pd.read_csv("data/people.csv")

result = df.set_index("이름")

print(df["도시"]) # 1개 타입은 Series, 2개 이상은 DataFrame

print(result.loc["가영"])

print(result.iloc[3,2])
