import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import StratifiedKFold

# 1. 데이터 불러오기
train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')
all_data = pd.concat([train, test], ignore_index=True)

# 2. 일행(Group)과 가족(Surname) 정보 추출
all_data['Group'] = all_data['PassengerId'].str.split('_').str[0]
all_data['GroupSize'] = all_data.groupby('Group')['PassengerId'].transform('count')

# ⭐️ 수정 포인트 1: 성씨를 추출한 뒤, 그걸 바탕으로 '가족 규모(FamilySize)'를 반드시 계산합니다!
all_data['Surname'] = all_data['Name'].fillna('Unknown Unknown').str.split(' ').str[-1]
all_data['FamilySize'] = all_data.groupby('Surname')['PassengerId'].transform('count')

# 3. 2중 데이터 복원 (결측치 0에 도전)
# (1) 같은 일행이면 고향이 같다
home_group_map = all_data.groupby('Group')['HomePlanet'].first().to_dict()
all_data['HomePlanet'] = all_data['HomePlanet'].fillna(all_data['Group'].map(home_group_map))

# (2) 일행이 달라도 성씨가 같으면 고향이 같다 (2차 방어)
home_surname_map = all_data.groupby('Surname')['HomePlanet'].first().to_dict()
all_data['HomePlanet'] = all_data['HomePlanet'].fillna(all_data['Surname'].map(home_surname_map))
all_data['HomePlanet'] = all_data['HomePlanet'].fillna(all_data['HomePlanet'].mode()[0])

# 같은 그룹이면 같은 객실(Cabin)을 쓴다
cabin_map = all_data.groupby('Group')['Cabin'].first().to_dict()
all_data['Cabin'] = all_data['Cabin'].fillna(all_data['Group'].map(cabin_map))

# 객실 분해 및 숫자 변환
all_data[['Deck', 'Num', 'Side']] = all_data['Cabin'].str.split('/', expand=True)
all_data['Num'] = pd.to_numeric(all_data['Num'], errors='coerce')
all_data['Num'] = all_data['Num'].fillna(all_data['Num'].median())

# 4. 부대비용 및 냉동수면 논리적 처리
expenses = ['RoomService', 'FoodCourt', 'ShoppingMall', 'Spa', 'VRDeck']
for col in expenses:
    all_data[col] = all_data[col].fillna(0)
all_data['TotalSpend'] = all_data[expenses].sum(axis=1)

# 돈 안 썼으면 냉동수면 중
all_data['CryoSleep'] = all_data['CryoSleep'].fillna(all_data['TotalSpend'] == 0).astype(int)

# 5. 나이 결측치 처리 및 '어린이' 파생 변수 추가
all_data['Age'] = all_data['Age'].fillna(all_data.groupby('HomePlanet')['Age'].transform('median'))
all_data['Age'] = all_data['Age'].fillna(all_data['Age'].median())

# 핵심 아이디어: 12세 이하는 재난 상황에서 특별 보호를 받았다!
all_data['Is_Child'] = (all_data['Age'] <= 12).astype(int)
all_data['VIP'] = all_data['VIP'].fillna(False).astype(int)

# 6. 글자를 숫자로 변환 (Surname은 제외하여 과적합 원천 차단)
features_to_encode = ['HomePlanet', 'Destination', 'Deck', 'Side']
for col in features_to_encode:
    all_data[col] = pd.factorize(all_data[col])[0]

# 7. ⭐️ 수정 포인트 2: 학습 리스트에 'FamilySize'를 추가합니다! (Surname은 철저히 배제)
features = ['HomePlanet', 'CryoSleep', 'Destination', 'Age', 'Is_Child', 'VIP', 'TotalSpend',
            'Deck', 'Num', 'Side', 'GroupSize', 'FamilySize'] + expenses

X_train = all_data[all_data['Transported'].notnull()][features]
y_train = all_data[all_data['Transported'].notnull()]['Transported'].astype(int)
X_test = all_data[all_data['Transported'].isnull()][features]

# =====================================================================
# 8. K-Fold 교차 검증 + 앙상블 (캐글 랭커들의 필살기)
# =====================================================================
lgbm = LGBMClassifier(n_estimators=400, max_depth=6, learning_rate=0.03, random_state=42, verbose=-1)
xgb = XGBClassifier(n_estimators=400, max_depth=5, learning_rate=0.03, random_state=42)
rf = RandomForestClassifier(n_estimators=400, max_depth=9, random_state=42)

ensemble = VotingClassifier(
    estimators=[('lgbm', lgbm), ('xgb', xgb), ('rf', rf)],
    voting='soft',
    weights=[2, 2, 1]
)

# 데이터를 5등분하여 돌아가며 모의고사를 치름 (StratifiedKFold)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# 최종 정답을 담을 빈 바구니 준비 (확률을 누적하기 위해 0으로 채움)
test_predictions = np.zeros(len(X_test))

print("🚀 K-Fold 학습 시작 (5번의 모의고사를 봅니다)...")
for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train)):
    # 5등분 한 데이터 중 4개는 공부용(X_tr), 1개는 모의고사용(X_val)으로 쪼갬
    X_tr, y_tr = X_train.iloc[train_idx], y_train.iloc[train_idx]

    # 모델 학습
    ensemble.fit(X_tr, y_tr)

    # 캐글에 제출할 진짜 시험지(X_test)를 풀어서 확률을 누적함
    # predict_proba는 [살아남을 확률, 전송될 확률]을 반환하므로 [:, 1](전송될 확률)만 가져옴
    test_predictions += ensemble.predict_proba(X_test)[:, 1] / skf.n_splits
    print(f"✅ Fold {fold + 1} 완료!")

# 9. 결과 저장 (누적된 확률의 평균이 50%를 넘으면 True, 아니면 False)
test["Transported"] = (test_predictions > 0.5).astype(bool)
test[["PassengerId", "Transported"]].to_csv('data/submission_final.csv', index=False)
print("🎉 최종 예측 완료! submission_final.csv 파일이 생성되었습니다.")