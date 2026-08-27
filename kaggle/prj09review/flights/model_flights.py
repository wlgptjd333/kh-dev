from operator import concat

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

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

df = df.sort_values("date").reset_index(drop=True)

df_month_dummies = pd.get_dummies(df['month'], drop_first=True)


# df_concat = pd.concat([df[["passengers"]], df_month_dummies], axis=1)
# df_concat['t'] = np.arange(len(df))
df_month_dummies['t'] = np.arange(len(df))
# 데이터 분리
n_test = 12

X = df_month_dummies
y = df["passengers"]
X_train = X.iloc[:-n_test]
y_train = y.iloc[:-n_test]
X_test = X.iloc[-n_test:]
y_test = y.iloc[-n_test:]


# 학습
m = LinearRegression()
m.fit(X_train, y_train)


# 예측
y_pred = m.predict(X_test)

# 평가
r2 = r2_score(y_test, y_pred)
print(r2)