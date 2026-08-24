import pandas as pd
from lightgbm import LGBMClassifier

# 1. 데이터 불러오기 및 합치기
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')
all_data = pd.concat([train, test], ignore_index=True)

# 2. 파생 변수 만들기 (이전의 강력했던 특징들 유지)
expenses = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
for col in expenses:
    all_data[col] = all_data[col].fillna(0)
all_data['TotalSpend'] = all_data[expenses].sum(axis=1)

all_data[['Deck', 'Num', 'Side']] = all_data['Cabin'].str.split('/', expand=True)

# PassengerId에서 '일행(Group)' 규모 파악하기
all_data['Group'] = all_data['PassengerId'].str.split('_').str[0]
all_data['GroupSize'] = all_data.groupby('Group')['PassengerId'].transform('count')

# 3. 결측치 처리 및 변환
all_data['CryoSleep'] = all_data['CryoSleep'].fillna(all_data['TotalSpend'] == 0).astype(int)
all_data['Age'] = all_data['Age'].fillna(all_data['Age'].median())
all_data['VIP'] = all_data['VIP'].fillna(False).astype(int)

# 4. 글자를 숫자로 변환
features_to_encode = ['HomePlanet', 'Destination', 'Deck', 'Side', 'Group']
for col in features_to_encode:
    all_data[col] = pd.factorize(all_data[col])[0]

# 5. 데이터 다시 나누기
features = ['HomePlanet', 'CryoSleep', 'Destination', 'Age', 'VIP', 'TotalSpend',
            'Deck', 'Side', 'GroupSize'] + expenses
X_train = all_data[all_data['Transported'].notnull()][features]
y_train = all_data[all_data['Transported'].notnull()]['Transported'].astype(int)
X_test = all_data[all_data['Transported'].isnull()][features]

# 6. LightGBM 모델 학습
m = LGBMClassifier(n_estimators=500, max_depth=7, learning_rate=0.05, random_state=42)
m.fit(X_train, y_train)

# 7. 결과
result = m.predict(X_test)
test["Transported"] = result.astype(bool)
test[["PassengerId", "Transported"]].to_csv('data/submission_v2.csv', index=False)