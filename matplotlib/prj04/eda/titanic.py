# 데이터 로드
import pandas as pd
import seaborn
from matplotlib import pyplot as plt
import seaborn as sns

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
df = pd.read_csv(url)

# print(df.shape)
# # 데이터 파악
# print(df.isna().sum())
# 결측치 처리
df["Age"] = df["Age"].fillna(df["Age"].median())
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
df = df.drop(columns=["Cabin"])
# print(df.isna().sum())
# # 단변량 분석
# # 생존자 사망자 비율
# print(df["Survived"].value_counts(normalize=True) * 100)
# # 범주형 시각화
# fig, axes = plt.subplots(1, 3, figsize=(15, 5))
# axes[0].set_title("Survived")
# sns.countplot(x="Survived", data=df, ax=axes[0])
# axes[1].set_title("성별")
# sns.countplot(x="Sex", data=df, ax=axes[1])
# axes[2].set_title("객실 등급")
# sns.countplot(x="Pclass", data=df, ax=axes[2])
# # 나이 시각화
# plt.figure(figsize=(5, 5))
# sns.histplot(df["Age"], bins=30, kde=True)
# plt.title("나이")
#
# # 이변량 분석(성별,객실등급, 나이대, 가족 수에 따른 생존률 파악)
# fig, axes = plt.subplots(2, 2, figsize=(12, 10))
# sns.barplot(x="Sex", y="Survived", data=df, ax=axes[0, 0])
# sns.barplot(x="Pclass", y="Survived", data=df, ax=axes[0, 1])
#
# df["AgeBand"] = pd.cut(
#     df["Age"], bins=[0, 12, 18, 40, 60, 100],
#     labels=["아동", "청소년", "청년", "중년", "노년"])
#
# print(df.groupby("AgeBand")["Survived"].mean())
# sns.barplot(x="AgeBand", y = "Survived",
#             data=df, ax=axes[1, 0])
# df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
# sns.barplot(x="FamilySize", y = "Survived",
#             data=df, ax=axes[1, 1])
#


# 상관관계
# print(df.info())
# cols = ["Survived", "Pclass","Age","SibSp","Parch","Fare"]
# cor = df[cols].corr()
#
# plt.figure(figsize=(10,8))
# sns.heatmap(cor, cmap="coolwarm", annot=True, fmt=".2f")

# 인사이트
'''
남성보다 여성이 생존율이 높다
객실 등급이 좋을수록(숫자가 낮을수록) 생존율이 높다
나이가 어린 아도으이 경우 생존율이 높다
가족 규모가 2~4인 일 때 생존율이 높다
'''
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
# 성별 + 객실등급에 따른 생존율 파악
sns.barplot(x="Pclass", y="Survived", hue="Sex", data=df, ax=axes[0, 0])
axes[0, 0].set_title("성별 + 객실등급에 따른 생존율 파악")
# 탑승 항구에 따른 생존율 파악
sns.barplot(x="Embarked", y="Survived", data=df, ax=axes[0, 1])
axes[0, 1].set_title("탑승 항구에 따른 생존율 파악")
# 이름에 따른 생존율 파악
# 1. 정규표현식을 사용해 이름에서 '알파벳 + 마침표' 형태의 호칭만 쏙 뽑아냅니다.
df['Title'] = df['Name'].str.extract(r' ([A-Za-z]+)\.', expand=False)

# 2. 호칭이 너무 자잘하게 많으니, 주요 4개(Mr, Mrs, Miss, Master) 빼고는 'Other'로 묶어줍니다.
df['Title'] = df['Title'].replace(['Rev', 'Dr', 'Col', 'Major', 'Mlle', 'Countess',
                                   'Ms', 'Lady', 'Jonkheer', 'Don', 'Mme', 'Capt', 'Sir'], 'Other')

sns.barplot(x="Title", y="Survived", data=df, ax=axes[1, 0])
axes[1, 0].set_title("이름에 따른 생존율")
# 운임에 따른 생존율 파악
df['Fareband'] = pd.qcut(df['Fare'], 4, labels=["저가", "중가", "고가", "최고가"])

sns.barplot(x="Fareband", y="Survived", data=df, ax=axes[1, 1])
axes[1, 1].set_title("운임에 따른 생존율 파악")

plt.tight_layout()
plt.show()
