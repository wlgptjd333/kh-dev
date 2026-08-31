import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# 1. 데이터 로드
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# 2. 상관계수 기반 중요 특성(Feature) 선별
# 숫자형 데이터만 추출하여 상관계수 행렬 계산
numeric_df = train.select_dtypes(exclude=['object'])
corr_matrix = numeric_df.corr()

# 집값(SalePrice)과의 상관계수 절댓값이 0.4 이상인 핵심 특성만 추출
# (예: OverallQual, GrLivArea, GarageCars 등 집값과 직결되는 데이터만 남음)
high_corr_cols = corr_matrix.index[abs(corr_matrix['SalePrice']) >= 0.4].tolist()
high_corr_cols.remove('SalePrice') # 입력 데이터(X)에서 정답지(y)는 제외해야 하므로 삭제

# 문자형(범주형) 특성 목록 추출
cat_cols = train.select_dtypes(include=['object']).columns.tolist()

# 3. X, y 세팅 (선별된 특성만 사용)
selected_features = high_corr_cols + cat_cols

X = train[selected_features]
y = train['SalePrice']
X_test = test[selected_features]

# 4. 전처리 파이프라인 조립
num_pipe = make_pipeline(
    SimpleImputer(strategy='mean'),
    StandardScaler()
)

cat_pipe = make_pipeline(
    SimpleImputer(strategy='most_frequent'),
    OneHotEncoder(handle_unknown='ignore')
)

preprocessor = ColumnTransformer([
    ('num', num_pipe, high_corr_cols), # 선별된 숫자형 특성만 통과
    ('cat', cat_pipe, cat_cols)        # 문자형 특성 통과
])

# 5. 최종 파이프라인 (전처리기 + 모델) 구축
model = make_pipeline(preprocessor, RandomForestRegressor(random_state=42))

# 6. 학습 및 예측
model.fit(X, y)
preds = model.predict(X_test)

# 7. 캐글 제출용 파일 생성
submission = pd.DataFrame({
    'Id': test['Id'],
    'SalePrice': preds
})
submission.to_csv('submission_v2_corr.csv', index=False)