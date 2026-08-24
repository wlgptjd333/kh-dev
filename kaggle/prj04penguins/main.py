import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 데이터
df = sns.load_dataset("penguins")

# 결측치, 중복제거, 인코딩
df = df.dropna().reset_index(drop=True)

# 단변량 분석
# y
print(df["species"].value_counts())

# x 숫자형(부리 길이, 부리 깊이, 몸무게, 지느러미 길이)
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
sns.histplot(df["bill_length_mm"], bins=20, ax=axes[0, 0])
axes[0, 0].set_title("부리 길이 분포")

sns.histplot(df["bill_depth_mm"], bins=20, ax=axes[0, 1])
axes[0, 1].set_title("부리 깊이 분포")

sns.histplot(df["body_mass_g"], bins=20, ax=axes[1, 0])
axes[1, 0].set_title("몸무게 분포")

sns.histplot(df["flipper_length_mm"], bins=20, ax=axes[1, 1])
axes[1, 1].set_title("지느러미 분포")

# plt.tight_layout()
# plt.show()

#  x 범주형
fig, axes = plt.subplots(1, 3, figsize=(12, 8))

sns.countplot(data=df, x="species", ax=axes[0])
axes[0].set_title("종")

sns.countplot(data=df, x="island", ax=axes[1])
axes[1].set_title("서식지")

sns.countplot(data=df, x="sex", ax=axes[2])
axes[2].set_title("성별")

# plt.tight_layout()
# plt.show()

# 이변량 분석
# 종별로 신체 치수 평균
# print(df.groupby("species")["bill_length_mm"].mean())

fig, axes = plt.subplots(2, 2, figsize=(12, 8))
sns.boxplot(data=df, ax=axes[0, 0], x="species", y="bill_length_mm")
sns.boxplot(data=df, ax=axes[0, 1], x="species", y="bill_depth_mm")
sns.boxplot(data=df, ax=axes[1, 0], x="species", y="flipper_length_mm")
sns.boxplot(data=df, ax=axes[1, 1], x="species", y="body_mass_g")

# plt.tight_layout()
# plt.show()

# 종 - 섬, 성별   관계도
result = pd.crosstab(df["species"], df["island"], margins=True)
print(result)

fig, axes = plt.subplots(1, 2, figsize=(10, 6))
# sns.heatmap(result, annot=True, ax=axes[0], fmt="d")
# sns.barplot(data=df, x="species", y="bill_depth_mm", ax=axes[1], hue = "sex")

# 상관관계
df_nums = df[["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"]]
cor = df_nums.corr()
print(cor)
sns.heatmap(cor, annot=True, ax=axes[0], cmap="coolwarm")

# 산점도: 부리길이, 부리깊이
sns.scatterplot(data=df, x="bill_length_mm", y="bill_depth_mm", hue = "species")


plt.tight_layout()
plt.show()
#
