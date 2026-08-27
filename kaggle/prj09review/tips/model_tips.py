import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 데이터 불러오기
df = sns.load_dataset("tips")

# 전처리
df["tip_pct"] = df["tip"] / df["total_bill"] * 100

features = ['total_bill', 'size', 'tip_pct']
X = df[features]
y = df["tip"]

X_train, X_test, y_train, y_test = train_test_split (
    X, y, test_size=0.2, random_state=42)

# 학습
m = RandomForestRegressor(n_estimators=1000, random_state=42)
m.fit(X_train, y_train)

# 예측
y_pred = m.predict(X_test)

# 평가
r2 = r2_score(y_test, y_pred)

print("R²:", r2)

y_calc = X_test["total_bill"] * X_test["tip_pct"] / 100

print(r2_score(y_test, y_calc))