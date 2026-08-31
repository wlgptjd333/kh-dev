from typing import Any

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, root_mean_squared_error

# 한글 설정
plt.rcParams['font.family'] = ['Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

# 데이터 불러오기
data = fetch_california_housing()
X = data.data
y = data.target

# df 만들기
df = pd.DataFrame(X, columns=data.feature_names)
df['Price'] = y

# csv 저장
df.to_csv('california_housing.csv', index=False)

# 데이터 정보 확인
print("df. describe(): ", df.describe())
print("df.shape: ", df.shape)
print("df. head(): ", df.head())

# 결측치 확인
print("df.isnull().sum(): ", df.isnull().sum())

# 데이터 탐색
plt.figure(figsize=(10, 10))
plt.hist(df['Price'], bins=50)
plt.title('Histogram of Price')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# 데이터 학습 준비
X_data = df.drop('Price', axis=1)
y_data = df['Price']
X_train, X_test, y_train, y_test = train_test_split(
    X_data, y_data, test_size=0.2, random_state=42)

# 스케일링
scaler = StandardScaler()
scaler.fit_transform(X_train)
scaler.transform(X_test)

# 학습
m = LinearRegression()
m.fit(X_train, y_train)

# 예측
y_pred = m.predict(X_test)

# 평가
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
rmse = root_mean_squared_error(y_test, y_pred)

print("R2 score: ", r2)
print("MAE score: ", mae)
print("RMSE score: ", rmse)
