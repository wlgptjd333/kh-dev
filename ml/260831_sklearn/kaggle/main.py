import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# 1. 데이터 로드 (같은 폴더에 파일이 있다고 가정)
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

# 2. X, y 분리 (Id는 학습에 방해되므로 제외)
X = train.drop(['Id', 'SalePrice'], axis=1)
y = train['SalePrice']
X_test = test.drop(['Id'], axis=1)

# 3. 특성 자동 분류 (숫자형 vs 문자형)
num_cols = X.select_dtypes(exclude=['object']).columns
cat_cols = X.select_dtypes(include=['object']).columns

# 4. 전처리 파이프라인 조립
# 숫자형: 빈칸은 평균으로 채우고, 크기는 스케일링
num_pipe = make_pipeline(
    SimpleImputer(strategy='mean'),
    StandardScaler()
)

# 문자형: 빈칸은 가장 많이 나온 값(최빈값)으로 채우고, 원핫인코딩
cat_pipe = make_pipeline(
    SimpleImputer(strategy='most_frequent'),
    OneHotEncoder(handle_unknown='ignore')
)

# ColumnTransformer로 두 파이프라인을 병렬로 합치기
preprocessor = ColumnTransformer([
    ('num', num_pipe, num_cols),
    ('cat', cat_pipe, cat_cols)
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
submission.to_csv('submission_v1.csv', index=False)