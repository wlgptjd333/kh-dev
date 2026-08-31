import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor

# 1. 데이터 로드
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# 2. 강력한 파생 변수 추가 (Feature Engineering)
for df in [train, test]:
    df['TotalSF'] = df['TotalBsmtSF'] + df['1stFlrSF'] + df['2ndFlrSF']
    # 욕실 수 통합 (HalfBath는 0.5개로 계산)
    df['TotalBath'] = df['FullBath'] + (0.5 * df['HalfBath']) + df['BsmtFullBath'] + (0.5 * df['BsmtHalfBath'])
    # 집의 연식 (팔린 연도 - 지어진 연도)
    df['HouseAge'] = df['YrSold'] - df['YearBuilt']

# 3. X, y 분리 및 정답 로그 변환
X = train.drop(['Id', 'SalePrice'], axis=1)
X_test = test.drop(['Id'], axis=1)
y_log = np.log1p(train['SalePrice'])

# 4. 데이터 분할 및 전처리 파이프라인
num_cols = X.select_dtypes(exclude=['object']).columns
cat_cols = X.select_dtypes(include=['object']).columns

num_pipe = make_pipeline(SimpleImputer(strategy='median'), StandardScaler())
cat_pipe = make_pipeline(SimpleImputer(strategy='most_frequent'), OneHotEncoder(handle_unknown='ignore'))

preprocessor = ColumnTransformer([('num', num_pipe, num_cols), ('cat', cat_pipe, cat_cols)])

# 5. 캐글 1티어 부스팅 모델 2개 준비
xgb = make_pipeline(preprocessor, XGBRegressor(n_estimators=500, learning_rate=0.05, random_state=42))
lgbm = make_pipeline(preprocessor, LGBMRegressor(n_estimators=500, learning_rate=0.05, random_state=42, verbose=-1))

# 6. 각각 학습
print("XGBoost 학습 중...")
xgb.fit(X, y_log)
print("LightGBM 학습 중...")
lgbm.fit(X, y_log)

# 7. 블렌딩 (예측 결과 5:5 혼합) 및 원래 가격 복원
# 각각 예측 후 로그값을 원래 집값(달러)으로 풉니다
xgb_preds = np.expm1(xgb.predict(X_test))
lgbm_preds = np.expm1(lgbm.predict(X_test))

# 두 모델의 결과를 절반씩 섞습니다
final_preds = (xgb_preds * 0.5) + (lgbm_preds * 0.5)

# 8. 캐글 제출용 파일 생성
submission = pd.DataFrame({'Id': test['Id'], 'SalePrice': final_preds})
submission.to_csv('submission_v4_blend.csv', index=False)
print("✅ 제출 파일(submission_v4_blend.csv) 생성 완료!")