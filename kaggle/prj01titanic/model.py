import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# data
test = pd.read_csv('data/test.csv')
train = pd.read_csv('data/train.csv')

# 전처리
for df in [train, test]:
    df["Age"] = df["Age"].fillna(df.groupby("Pclass")["Age"].transform("median"))
    df["Sex"] = (df["Sex"] == "female").astype(int)
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())

    # 특징 만들기
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["Title"] = df["Name"].str.extract(r',\s*([^\.]+)\.')
    df["Title"] = df["Title"].replace(["Mlle", "Ms"], "Miss").replace("Mme","Mrs")
    df["Title"] = df["Title"].replace(
        ['Lady','Countess','Capt','Col','Don','Dr',
         'Major','Rev','Sir','Jonkheer','Dona'], "Rare")

    title_mapping = {"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}
    df["Title"] = df["Title"].map(title_mapping).fillna(0)

# 특징 고르기
features = ["Pclass", "Sex", "Age", "SibSp", "Parch", "Fare", "FamilySize", "Title"]
x = train[features]
y = train["Survived"]

# 학습
m = RandomForestClassifier(n_estimators=1000, random_state=4241, max_depth=3)
m.fit(x, y)

# 예측
test["Survived"] = m.predict(test[features])
test[["PassengerId", "Survived"]].to_csv('data/result.csv', index=False)
