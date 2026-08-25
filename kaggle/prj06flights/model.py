from statistics import LinearRegression

import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# data
df = sns.load_dataset("flights")
x = df["year"].astype(str) + "-" + df["month"].astype(str)
df["date"] = pd.to_datetime(x, format="%Y-%b")
df = df.sort_values("date").reset_index(drop=True)

# 추세
df['t'] = np.arange(len(df))

# m 계절
month_dummies = pd.get_dummies(df["month"], drop_first=True)

# print(month_dummies)

#
X = pd.concat([df['t'], month_dummies], axis=1)
y = df["passengers"]

test_cnt = 12

X_train, X_test = X.iloc[0:-test_cnt], X.iloc[-test_cnt:]
y_train, y_test = y.iloc[0:-test_cnt], y.iloc[-test_cnt:]

# 학습
m = LinearRegression()
m.fit(X_train, y_train)

# 예측
y_pred = m.predict(X_test)

# 오차확인
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(mae)
print(rmse)
print(r2)

e = np.mean(np.abs((y_test - y_pred) / y_test) * 100)
print(e)
