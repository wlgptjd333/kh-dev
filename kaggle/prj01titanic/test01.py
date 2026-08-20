import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# 1. 데이터 통합 (전처리 통일성 유지)
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')
all_data = pd.concat([train, test], sort=False).reset_index(drop=True)

# 2. 전처리 (구간화 제거, 자연스러운 숫자 그대로 유지!)
all_data["Age"] = all_data["Age"].fillna(all_data.groupby("Pclass")["Age"].transform("median"))
all_data["Fare"] = all_data["Fare"].fillna(all_data.groupby("Pclass")["Fare"].transform("median"))
all_data["Embarked"] = all_data["Embarked"].fillna('S').map({'S': 0, 'C': 1, 'Q': 2}).astype(int)
all_data["Sex"] = (all_data["Sex"] == "female").astype(int)

# 3. 핵심 특징만 남기기
all_data["FamilySize"] = all_data["SibSp"] + all_data["Parch"] + 1

all_data["Title"] = all_data["Name"].str.extract(r',\s*([^\.]+)\.', expand=False)
all_data["Title"] = all_data["Title"].replace(['Lady', 'Countess', 'Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'], 'Rare')
all_data["Title"] = all_data["Title"].replace(['Mlle', 'Ms'], 'Miss').replace('Mme', 'Mrs')
all_data["Title"] = all_data["Title"].map({"Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Rare": 5}).fillna(0)

# 4. 데이터 분리
features = ["Pclass", "Sex", "Age", "Fare", "Embarked", "Title", "FamilySize"]
X_train = all_data[all_data['Survived'].notnull()][features]
y_train = all_data[all_data['Survived'].notnull()]['Survived']
X_test = all_data[all_data['Survived'].isnull()][features]

# 5. 과적합을 막는 안정적인 모델 세팅 (max_depth=5가 핵심)
model = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
model.fit(X_train, y_train)

# 6. 예측 및 저장
test["Survived"] = model.predict(X_test).astype(int)
test[["PassengerId", "Survived"]].to_csv('data/result_balanced.csv', index=False)