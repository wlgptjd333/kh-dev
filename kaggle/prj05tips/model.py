import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import seaborn as sns

# 데이터 준비
df = sns.load_dataset("tips")

X = df[['total_bill']]
y = df['tip']

# 데이터 전처리

# 데이터 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 학습
m = LinearRegression()
m.fit(X_train, y_train)

# 1. 예측
y_pred = m.predict(X_test)

# 2-1. MAE (평균 절대 오차) 구하기 - 함수 사용
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print(f"평균 절대 오차(MAE): {mae}")
print(f"결정계수(R^2): {r2}")
print(f"RMSE: {rmse}")