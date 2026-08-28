import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

df = sns.load_dataset("diamonds")
df.to_csv("diamonds.csv")

# 전처리
df = df[(df['x'] > 0) & (df['y'] > 0) & (df['z'] > 0)]

# 단변량
# 가격, 캐럿 히스토그램
# fig, axes = plt.subplots(1, 2, figsize=(10,8))
# sns.histplot(data = df['carat'], ax = axes[0], bins = 20)
# sns.histplot(data = df['price'], ax = axes[1], bins = 20)
# plt.show()

# 이변량
# fig, axes = plt.subplots(1, 3, figsize=(10, 8))
# sns.scatterplot(data=df, ax=axes[0], x = 'carat', y = 'price')
# plt.show()

# 상관관계
num_cols = ['carat','depth', 'table','x','y','z', 'price']
result =df[num_cols].corr()
print(result)

# 인사이트

