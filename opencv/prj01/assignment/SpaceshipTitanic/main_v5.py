import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

# 1. 데이터 불러오기 및 통합
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')
all_data = pd.concat([train, test], ignore_index=True)

# 2. ⭐️ 이름에서 성씨(Surname)와 일행(Group) 정보 완벽 추출
all_data['Group'] = all_data['PassengerId'].str.split('_').str[0]
all_data['GroupSize'] = all_data.groupby('Group')['PassengerId'].transform('count')

# 이름 결측치는 'Unknown'으로 임시 처리 후, 맨 뒷단어(성씨) 추출
all_data['Surname'] = all_data['Name'].fillna('Unknown Unknown').str.split(' ').str[-1]
# 같은 성씨를 가진 사람 수를 세어 '가족 규모' 산출
all_data['FamilySize'] = all_data.groupby('Surname')['PassengerId'].transform('count')

# 3. ⭐️ 극한의 2중 데이터 복원 (Group -> Surname)
# (1) 같은 일행(Group)이면 고향이 같다
home_group_map = all_data.groupby('Group')['HomePlanet'].first().to_dict()
all_data['HomePlanet'] = all_data['HomePlanet'].fillna(all_data['Group'].map(home_group_map))

# (2) 일행이 다르고 빈칸이더라도, 같은 성씨(가족)면 고향이 같다! (2차 방어)
home_surname_map = all_data.groupby('Surname')['HomePlanet'].first().to_dict()
all_data['HomePlanet'] = all_data['HomePlanet'].fillna(all_data['Surname'].map(home_surname_map))

# 그래도 남은 극소수는 가장 많은 'Earth'로 처리
all_data['HomePlanet'] = all_data['HomePlanet'].fillna(all_data['HomePlanet'].mode()[0])

# 같은 그룹이면 같은 객실 쓸 확률 높음
cabin_map = all_data.groupby('Group')['Cabin'].first().to_dict()
all_data['Cabin'] = all_data['Cabin'].fillna(all_data['Group'].map(cabin_map))

# 객실 분해 및 숫자 변환
all_data[['Deck', 'Num', 'Side']] = all_data['Cabin'].str.split('/', expand=True)
all_data['Num'] = pd.to_numeric(all_data['Num'], errors='coerce')
all_data['Num'] = all_data['Num'].fillna(all_data['Num'].median())

# 4. 부대비용 및 냉동수면 논리적 결측치 처리
expenses = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
for col in expenses:
    all_data[col] = all_data[col].fillna(0)
all_data['TotalSpend'] = all_data[expenses].sum(axis=1)

# 돈 안 썼으면 잤을 것이다
all_data['CryoSleep'] = all_data['CryoSleep'].fillna(all_data['TotalSpend'] == 0).astype(int)

# 고향 행성별 나이 중앙값 채우기
all_data['Age'] = all_data['Age'].fillna(all_data.groupby('HomePlanet')['Age'].transform('median'))
all_data['Age'] = all_data['Age'].fillna(all_data['Age'].median())
all_data['VIP'] = all_data['VIP'].fillna(False).astype(int)

# 5. 글자를 숫자로 변환 (Surname 추가!)
features_to_encode = ['HomePlanet', 'Destination', 'Deck', 'Side', 'Group', 'Surname']
for col in features_to_encode:
    all_data[col] = pd.factorize(all_data[col])[0]

# 6. 데이터 분리 (⭐️ Surname, FamilySize 추가)
features = ['HomePlanet', 'CryoSleep', 'Destination', 'Age', 'VIP', 'TotalSpend',
            'Deck', 'Num', 'Side', 'GroupSize', 'Surname', 'FamilySize'] + expenses

X_train = all_data[all_data['Transported'].notnull()][features]
y_train = all_data[all_data['Transported'].notnull()]['Transported'].astype(int)
X_test = all_data[all_data['Transported'].isnull()][features]

# 7. 파라미터 안정화 및 투표 앙상블
lgbm = LGBMClassifier(n_estimators=400, max_depth=6, learning_rate=0.03, random_state=42, verbose=-1)
xgb = XGBClassifier(n_estimators=400, max_depth=5, learning_rate=0.03, random_state=42)
rf = RandomForestClassifier(n_estimators=400, max_depth=9, random_state=42)

ensemble = VotingClassifier(
    estimators=[('lgbm', lgbm), ('xgb', xgb), ('rf', rf)],
    voting='soft',
    weights=[2, 2, 1]
)

# 8. 학습 및 예측
ensemble.fit(X_train, y_train)
result = ensemble.predict(X_test)

# 9. 결과 저장
test["Transported"] = result.astype(bool)
test[["PassengerId", "Transported"]].to_csv('data/submission_v5.csv', index=False)