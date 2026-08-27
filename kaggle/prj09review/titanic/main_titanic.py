import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 데이터 로드 및 저장
df = sns.load_dataset("titanic")
df.to_csv("titanic.csv", index=False) # index=False를 주어 불필요한 인덱스 열 생성 방지

# 1. 데이터 구조 확인 및 결측치 확인
print("=== 데이터 구조 확인 ===")
df.info()

print("\n=== 결측치 확인 ===")
print(df.isnull().sum())

# 한 번에 볼 수 있도록 시각화 레이아웃 설정
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("타이타닉 데이터 탐색적 분석(EDA)", fontsize=16)

# 2. 단변량 분석 (생존자 분포)
sns.countplot(data=df, x='survived', ax=axes[0, 0])
axes[0, 0].set_title("전체 생존자 수 (0=사망, 1=생존)")

# 3. 이변량 분석 (성별 생존율, 객실 등급별 생존율)
# 성별에 따른 생존율
sns.barplot(data=df, x='sex', y='survived', ax=axes[0, 1])
axes[0, 1].set_title("성별 생존율")

# 객실 등급(pclass)에 따른 생존율
sns.barplot(data=df, x='pclass', y='survived', ax=axes[1, 0])
axes[1, 0].set_title("객실 등급별(Pclass) 생존율")

# 4. 상관관계 (숫자형 변수만 추출하여 상관계수 확인)
# select_dtypes를 사용해 숫자형(int, float) 데이터만 필터링
numeric_df = df.select_dtypes(include=[np.number])
corr = numeric_df.corr()

# 상관계수 히트맵 시각화
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1, ax=axes[1, 1])
axes[1, 1].set_title("숫자형 변수 간 상관관계 히트맵")

plt.tight_layout()
plt.show()