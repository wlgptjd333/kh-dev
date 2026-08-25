import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import KFold
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from lightgbm import LGBMRegressor

df = sns.load_dataset("diamonds")


def remove_outliers(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]


df = remove_outliers(df, 'y')
df = remove_outliers(df, 'z')
df = df[(df['x'] != 0) & (df['y'] != 0) & (df['z'] != 0)]

# 파생 변수(부피) 추가
df['volume'] = df['x'] * df['y'] * df['z']

cut_dict = {'Fair': 1, 'Good': 2, 'Very Good': 3, 'Premium': 4, 'Ideal': 5}
color_dict = {'J': 1, 'I': 2, 'H': 3, 'G': 4, 'F': 5, 'E': 6, 'D': 7}
clarity_dict = {'I1': 1, 'SI2': 2, 'SI1': 3, 'VS2': 4, 'VS1': 5, 'VVS2': 6, 'VVS1': 7, 'IF': 8}

df['cut'] = df['cut'].map(cut_dict)
df['color'] = df['color'].map(color_dict)
df['clarity'] = df['clarity'].map(clarity_dict)

X = df.drop(columns=['price']).reset_index(drop=True)
y = df['price'].reset_index(drop=True)

kf = KFold(n_splits=5, shuffle=True, random_state=42)
model_lgbm = LGBMRegressor(n_estimators=100, random_state=42, verbose=-1)

mae_scores = []
r2_scores = []

print("K-Fold 교차 검증(5회) 시작...\n")

for i, (train_idx, test_idx) in enumerate(kf.split(X)):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    model_lgbm.fit(X_train, y_train)
    y_pred = model_lgbm.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    mae_scores.append(mae)
    r2_scores.append(r2)

    print(f"[{i + 1}회차] MAE: {mae:.2f} 달러 / R^2: {r2:.4f}")

print("\n" + "=" * 30)
print(f"[최종 K-Fold 평균 성적]")
print(f"평균 MAE: {np.mean(mae_scores):.2f} 달러")
print(f"평균 R^2: {np.mean(r2_scores):.4f}")
print(np.sqrt(mean_squared_error(y_test, y_pred)))
print("=" * 30)

import matplotlib.pyplot as plt

# 한글 폰트 설정 (깨짐 방지)
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 1. 모델이 학습한 변수 중요도 뽑아내기
# (마지막 5회차 학습이 끝난 모델의 기준입니다)
# 수정 전 (기본값인 split으로 계산됨)
# importance = model_lgbm.feature_importances_

# 수정 후 ('gain' 옵션을 주어 실제 오차 감소 기여도를 계산함)
importance = model_lgbm.booster_.feature_importance(importance_type='gain')
feature_names = X.columns

# 2. 보기 좋게 데이터프레임으로 묶어서 정렬하기
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': importance
})
# 중요도가 높은 순서대로 내림차순 정렬
importance_df = importance_df.sort_values(by='Importance', ascending=False)

# 3. 가로 막대 그래프(Barplot) 그리기
plt.figure(figsize=(10, 6))
sns.barplot(data=importance_df, x='Importance', y='Feature', palette='viridis')

plt.title("LightGBM 모델의 변수 중요도 (Feature Importance)")
plt.xlabel("중요도 점수 (모델이 분기점으로 사용한 횟수)")
plt.ylabel("변수 이름")
plt.show()