import numpy as np
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import pandas as pd

# 1. 데이터 준비
df = sns.load_dataset("diamonds")

# 2. 데이터 전처리
df = df[(df["x"] > 0) & (df["y"] > 0) & (df["z"] > 0)].reset_index(drop=True)

cut_order = ['Fair', 'Good', 'Very Good', 'Premium', 'Ideal']
color_order = ['J', 'I', 'H', 'G', 'F', 'E', 'D']
clar_order = ['I1', 'SI2', 'SI1', 'VS2', 'VS1', 'VVS2', 'VVS1', 'IF']

df["cut_o"] = df["cut"].map({v: i for i, v in enumerate(cut_order)})
df["color_o"] = df["color"].map({v: i for i, v in enumerate(color_order)})
df["clar_o"] = df["clarity"].map({v: i for i, v in enumerate(clar_order)})

features = ['carat', 'cut_o', 'color_o', 'clar_o', 'depth', 'table', 'x', 'y', 'z']

X = df[features]
y = df['price']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. 학습 (LinearRegression 사용)
m = LinearRegression()
m.fit(X_train, y_train)

# 4. 예측
y_pred = m.predict(X_test)

# 5. 모델평가
mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2s = r2_score(y_test, y_pred)

print("mae :", mae)
print("rmse:", rmse)
print("r2s :", r2s)

# 6. 회귀 계수(coef_) 확인
# LinearRegression이므로 coef_를 사용하는 것이 맞습니다!
sr = pd.Series(m.coef_, index=features).sort_values(ascending=False)
print("\n[선형 회귀 계수 (Coefficients)]")
print(sr)