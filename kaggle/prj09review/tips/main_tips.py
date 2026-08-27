import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 데이터 불러오기
df = sns.load_dataset("tips")
df.to_csv("tips.csv")

# 데이터 확인하기

# 전처리
df["tip_pct"] = df["tip"] / df["total_bill"] * 100

# 단변량


# 이변량


# 상관관계


