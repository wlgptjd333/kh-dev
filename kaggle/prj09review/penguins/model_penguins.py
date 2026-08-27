import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
import pandas as pd

plt.rcParams['font.family'] = "Malgun Gothic"
plt.rcParams['axes.unicode_minus'] = False

# 데이터 준비
df = sns.load_dataset('penguins')

# 데이터 전처리 (결측치, 중복, 인코딩, 스케일, 파생칼럼)
df = df.dropna()

# 학습용 시험용 분류
print(df.columns)
features = ['bill_length_mm', 'bill_depth_mm',
            'flipper_length_mm', 'body_mass_g']
X = df[features]
y = df['species']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)



# 학습
m = LogisticRegression(max_iter=5000)
m.fit(X_train, y_train)

# 예측
y_pred = m.predict(X_test)

# 평가
print(m.score(X_test, y_test))

# 혼동 행렬 출력
# cm = confusion_matrix(y_test, y_pred)
# print("=== 혼동 행렬 (Confusion Matrix) ===")
# print(cm)
# plt.figure()
# sns.heatmap(cm, annot=True, fmt="g", cmap="Blues"
#             , xticklabels=["Adelie", "Chintoo", "Gentoo"]
#             , yticklabels=["Adelie", "Chintoo", "Gentoo"])
# plt.xlabel("예측")
# plt.ylabel("실제")
# plt.show()

print(m.coef_)

# cr = classification_report(y_test, y_pred)
# print(cr)