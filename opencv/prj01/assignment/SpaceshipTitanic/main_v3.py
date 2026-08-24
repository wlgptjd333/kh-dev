import pandas as pd
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

# 1. 데이터 불러오기 및 통합
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')
all_data = pd.concat([train, test], ignore_index=True)

# 2. 승객 번호에서 일행(Group) 정보 뽑아내기
all_data['Group'] = all_data['PassengerId'].str.split('_').str[0]
all_data['GroupSize'] = all_data.groupby('Group')['PassengerId'].transform('count')

# 3. 같은 그룹 정보로 빈칸 채우기
home_map = all_data.groupby('Group')['HomePlanet'].first().to_dict()
all_data['HomePlanet'] = all_data['HomePlanet'].fillna(all_data['Group'].map(home_map))

cabin_map = all_data.groupby('Group')['Cabin'].first().to_dict()
all_data['Cabin'] = all_data['Cabin'].fillna(all_data['Group'].map(cabin_map))
all_data['HomePlanet'] = all_data['HomePlanet'].fillna(all_data['HomePlanet'].mode()[0])

# 객실 분해
all_data[['Deck', 'Num', 'Side']] = all_data['Cabin'].str.split('/', expand=True)

# 버려졌던 Num(객실 번호)를 숫자로 변환
all_data['Num'] = pd.to_numeric(all_data['Num'], errors='coerce')
all_data['Num'] = all_data['Num'].fillna(all_data['Num'].median())

# 4. 부대비용 및 냉동수면 결측치 처리
expenses = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
for col in expenses:
    all_data[col] = all_data[col].fillna(0)
all_data['TotalSpend'] = all_data[expenses].sum(axis=1)

# 돈을 하나도 안 썼으면 냉동수면(CryoSleep) 중이었을 것
all_data['CryoSleep'] = all_data['CryoSleep'].fillna(all_data['TotalSpend'] == 0).astype(int)

# 나이를 전체 중앙값이 아닌, 고향 행성(HomePlanet)별 중앙값으로 더 정교하게
all_data['Age'] = all_data['Age'].fillna(all_data.groupby('HomePlanet')['Age'].transform('median'))
all_data['Age'] = all_data['Age'].fillna(all_data['Age'].median())
all_data['VIP'] = all_data['VIP'].fillna(False).astype(int)

# 5. 글자를 숫자로 변환
features_to_encode = ['HomePlanet', 'Destination', 'Deck', 'Side', 'Group']
for col in features_to_encode:
    all_data[col] = pd.factorize(all_data[col])[0]

# 6. 데이터 분리 (features 리스트에 'Num' 추가)
features = ['HomePlanet', 'CryoSleep', 'Destination', 'Age', 'VIP', 'TotalSpend',
            'Deck', 'Num', 'Side', 'GroupSize'] + expenses

X_train = all_data[all_data['Transported'].notnull()][features]
y_train = all_data[all_data['Transported'].notnull()]['Transported'].astype(int)
X_test = all_data[all_data['Transported'].isnull()][features]

# 7. 파라미터 안정화 및 투표권 차등 지급
lgbm = LGBMClassifier(n_estimators=400, max_depth=6, learning_rate=0.03, random_state=42)
xgb = XGBClassifier(n_estimators=400, max_depth=5, learning_rate=0.03, random_state=42)
rf = RandomForestClassifier(n_estimators=400, max_depth=9, random_state=42)

# weights=[2, 2, 1] -> LGBM과 XGB의 의견을 2배 더 신뢰
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
test[["PassengerId", "Transported"]].to_csv('data/submission_v4.csv', index=False)