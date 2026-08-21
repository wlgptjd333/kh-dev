import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# df 준비 : 파일 읽어오기
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

# df 전처리
for df in [train, test]:
    df.dropna(inplace=True)
    df["Sex"] = (df["Sex"] == "female").astype(int)
# df에서 특징 고르기
x = train[["Sex"]]
y = train["Survived"]

# 학습
m = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=1)
m.fit(x,y)

# 예측
result = m.predict(test[["Sex"]])
print(result)