import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# data
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

# 전처리
for df in [train, test]:
    df["Age"] = df.groupby("Pclass")["Age"].transform("median")
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    df["Sex"] = (df["Sex"] == "female").astype(int)

# 특징 고르기
features = ["Sex", "Pclass", "Age"]
x = train[features]
y = train["Survived"]

# 학습
m = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=2)
m.fit(x, y)

# 예측
result = m.predict(test[features])
test["Survived"] = result

# 결과물 저장
test[["PassengerId", "Survived"]].to_csv('data/result.csv', index=False)
