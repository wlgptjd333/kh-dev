import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# 1. 데이터 로드
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# --- [전략 1] 파생 변수 생성 ---
# 기존 면적 데이터를 다 더해서 집값 예측의 핵심인 '총 면적' 변수 추가
for df in [train, test]:
    df['TotalSF'] = df['TotalBsmtSF'] + df['1stFlrSF'] + df['2ndFlrSF']

# 2. X, y 분리
X = train.drop(['Id', 'SalePrice'], axis=1)
X_test = test.drop(['Id'], axis=1)

# --- [전략 2] 정답(집값) 로그 변환 ---
# 한쪽으로 치우친 집값 데이터를 정규분포에 가깝게 펴주어 오차를 줄임
y_log = np.log1p(train['SalePrice'])

# 3. 특성 자동 분류 (상관계수 필터링 없이 전부 다 씁니다)
num_cols = X.select_dtypes(exclude=['object']).columns
cat_cols = X.select_dtypes(include=['object']).columns

# 4. 전처리 파이프라인 조립
# 숫자형: 평균(mean) 대신 튀는 값에 방어력이 높은 중앙값(median) 사용
num_pipe = make_pipeline(
    SimpleImputer(strategy='median'),
    StandardScaler()
)

cat_pipe = make_pipeline(
    SimpleImputer(strategy='most_frequent'),
    OneHotEncoder(handle_unknown='ignore')
)

preprocessor = ColumnTransformer([
    ('num', num_pipe, num_cols),
    ('cat', cat_pipe, cat_cols)
])

# 5. 최종 파이프라인 (전처리기 + 강력한 부스팅 모델)
# 예측력 강화를 위해 GradientBoosting 사용
model = make_pipeline(
    preprocessor,
    GradientBoostingRegressor(n_estimators=400, learning_rate=0.05, max_depth=4, random_state=42)
)

# 6. 학습 및 예측
model.fit(X, y_log)           # '로그가 씌워진' 가격으로 학습
preds_log = model.predict(X_test) # 예측 결과도 '로그가 씌워진' 상태

# --- [전략 3] 예측값 복원 ---
preds = np.expm1(preds_log)   # 로그를 다시 원래 달러($) 가격으로 되돌림

# 7. 캐글 제출용 파일 생성
submission = pd.DataFrame({
    'Id': test['Id'],
    'SalePrice': preds
})
submission.to_csv('submission_v3_advanced.csv', index=False)