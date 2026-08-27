import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

# 한글 폰트 및 마이너스 기호 깨짐 방지 설정
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 데이터 로드 및 저장
df = pd.read_csv("train.csv")

# 전처리 (결측치, 중복제거, 인코딩, 파생변수)

df["Age"] = df["Age"].fillna(df["Age"].median())
df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
df["Fare"] = df["Fare"].fillna(df["Fare"].median())
df["Sex"] = df["Sex"].map({"male": 0, "female": 1})
df["Embarked"] = df["Embarked"].map({"S": 0, "C": 1, "Q": 2})
df["FamilySize"] = df["Parch"] + df["SibSp"] + 1

# 모델 (데이터분리, 학습, 예측, 평가)
features = ["Age", "Embarked", "FamilySize", "Sex", "Fare", "Pclass"]
X = df[features]
y = df["Survived"]

X_train, X_test, y_train, y_test = \
    train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

m = LogisticRegression()
m.fit(X_train, y_train)

y_pred = m.predict(X_test)

acc_score = accuracy_score(y_test, y_pred)
print(y_pred)
print("acc_score: ", acc_score)

sr = pd.Series(m.coef_[0], index=features).sort_values(ascending=False)
print(sr)

result = classification_report(y_test, y_pred, target_names=["사망", "생존"])
print("=====result=====")
print(result)

# cm = confusion_matrix(y_test, y_pred)
# plt.figure(figsize = (10,10))
# sns.heatmap(cm, annot=True, fmt="d"
#             , cmap="Blues"
#             , xticklabels = ["사망예측", "생존예측"]
#             , yticklabels = ["사망실제", "생존실제"]
#             )
#
# plt.title("Confusion Matrix")
# plt.tight_layout()
# plt.show()
