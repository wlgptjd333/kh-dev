import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = "Malgun Gothic"
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
df = sns.load_dataset("flights")
df.to_csv("flights.csv")

# 데이터 구조 파악

# 전처리
df["date"] = pd.to_datetime(
    df["year"].astype(str) + "-" + df["month"].astype(str)
    , format="%Y-%b")

df.sort_values("date").reset_index(drop=True)

print(df)


# 단변량


# 이변량


# 상관관계
