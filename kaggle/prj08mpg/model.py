import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# 데이터 준비
df = sns.load_dataset("mpg")

# 전처리
df["horsepower"] = df["horsepower"].fillna(df["horsepower"].median())
features = ['weight', 'model_year']

result = pd.get_dummies(df["origin"], drop_first=True)
X = pd.concat([df[features], result] , axis=1)
y = df["mpg"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 학습
m = LinearRegression()
m.fit(X_train, y_train)

# 예측
y_pred = m.predict(X_test)


# 모델평가
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("mae : " , mae)
print("rmse : " , rmse)
print("r2 : " , r2)

# 회귀 계수
temp = pd.Series(m.coef_, index = X.columns)
print(temp)