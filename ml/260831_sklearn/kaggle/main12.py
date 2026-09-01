# ============================================================
# main12.py
# House Prices - v9 기반 최종 실험 버전
#
# 포함:
# 1. v9 Feature Engineering
# 2. GrLivArea 치명적 이상치 제거
# 3. Skewed numerical feature Log feature 추가
# 4. 5-Fold OOF
# 5. XGB / CatBoost / GBR / Ridge
# 6. 모델별 OOF RMSE
# 7. 여러 고정 블렌딩 후보 비교
# 8. OOF 최적 가중치 자동 탐색
# 9. 전체 데이터 재학습
# 10. 최적 가중치로 Test 예측
# 11. submission_v12_final.csv 생성
#
# 평가 지표:
# RMSE on log1p(SalePrice)
# 낮을수록 좋음
# ============================================================

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

from scipy.stats import skew
from scipy.optimize import minimize

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from xgboost import XGBRegressor
from catboost import CatBoostRegressor


# ============================================================
# 0. 설정
# ============================================================

RANDOM_STATE = 42
N_SPLITS = 5

print("=" * 70)
print("HOUSE PRICES V12")
print("v9 + Outlier + Skew + OOF + Ensemble Search")
print("=" * 70)


# ============================================================
# 1. 데이터 로드
# ============================================================

train_original = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

print()
print("Original Train:", train_original.shape)
print("Test          :", test.shape)


# ============================================================
# 2. 치명적인 이상치 제거
# ============================================================
#
# Ames House Prices에서 유명한 두 개의 대형 GrLivArea 이상치.
#
# GrLivArea > 4000 이면서 SalePrice < 300000인 집은
# 일반적인 가격 패턴에서 크게 벗어나므로 학습에서 제외.
#
# Test에는 SalePrice가 없으므로 제거하지 않음.
# ============================================================

outlier_mask = (
    (train_original["GrLivArea"] > 4000)
    & (train_original["SalePrice"] < 300000)
)

print()
print("=" * 70)
print("OUTLIER CHECK")
print("=" * 70)

print("제거 대상:", outlier_mask.sum())

if outlier_mask.sum() > 0:
    print(
        train_original.loc[
            outlier_mask,
            ["Id", "GrLivArea", "SalePrice"]
        ]
    )

train = train_original.loc[~outlier_mask].copy()

print("Outlier 제거 후 Train:", train.shape)


# ============================================================
# 3. Feature Engineering
# ============================================================

def feature_engineering(df):

    df = df.copy()

    # --------------------------------------------------------
    # 면적
    # --------------------------------------------------------

    df["TotalSF"] = (
        df["TotalBsmtSF"]
        + df["1stFlrSF"]
        + df["2ndFlrSF"]
    )

    df["TotalLivingSF"] = (
        df["GrLivArea"]
        + df["TotalBsmtSF"]
    )

    df["TotalBsmtFinSF_calc"] = (
        df["BsmtFinSF1"]
        + df["BsmtFinSF2"]
    )

    df["TotalPorchSF"] = (
        df["OpenPorchSF"]
        + df["3SsnPorch"]
        + df["EnclosedPorch"]
        + df["ScreenPorch"]
        + df["WoodDeckSF"]
    )

    # --------------------------------------------------------
    # 추가 면적
    # --------------------------------------------------------

    df["TotalHouseArea"] = (
        df["GrLivArea"]
        + df["TotalBsmtSF"]
        + df["GarageArea"]
        + df["WoodDeckSF"]
        + df["OpenPorchSF"]
    )

    df["TotalFinishedSF"] = (
        df["GrLivArea"]
        + df["BsmtFinSF1"]
        + df["BsmtFinSF2"]
    )

    # --------------------------------------------------------
    # 욕실
    # --------------------------------------------------------

    df["TotalBath"] = (
        df["FullBath"]
        + 0.5 * df["HalfBath"]
        + df["BsmtFullBath"]
        + 0.5 * df["BsmtHalfBath"]
    )

    # --------------------------------------------------------
    # 연식
    # --------------------------------------------------------

    df["HouseAge"] = (
        df["YrSold"]
        - df["YearBuilt"]
    )

    df["RemodAge"] = (
        df["YrSold"]
        - df["YearRemodAdd"]
    )

    df["GarageAge"] = (
        df["YrSold"]
        - df["GarageYrBlt"]
    )

    # --------------------------------------------------------
    # 시설 존재 여부
    # --------------------------------------------------------

    df["HasGarage"] = (
        df["GarageArea"].fillna(0) > 0
    ).astype(int)

    df["HasBsmt"] = (
        df["TotalBsmtSF"].fillna(0) > 0
    ).astype(int)

    df["HasFireplace"] = (
        df["Fireplaces"].fillna(0) > 0
    ).astype(int)

    df["HasPool"] = (
        df["PoolArea"].fillna(0) > 0
    ).astype(int)

    df["Has2ndFloor"] = (
        df["2ndFlrSF"].fillna(0) > 0
    ).astype(int)

    df["HasMasVnr"] = (
        df["MasVnrArea"].fillna(0) > 0
    ).astype(int)

    # --------------------------------------------------------
    # 핵심 Interaction
    # --------------------------------------------------------

    df["Qual_GrLivArea"] = (
        df["OverallQual"]
        * df["GrLivArea"]
    )

    df["Qual_TotalSF"] = (
        df["OverallQual"]
        * df["TotalSF"]
    )

    df["Qual_TotalBsmtSF"] = (
        df["OverallQual"]
        * df["TotalBsmtSF"]
    )

    df["Qual_GarageArea"] = (
        df["OverallQual"]
        * df["GarageArea"]
    )

    df["Qual_OverallCond"] = (
        df["OverallQual"]
        * df["OverallCond"]
    )

    df["GarageCars_Area"] = (
        df["GarageCars"]
        * df["GarageArea"]
    )

    df["Bath_GrLivArea"] = (
        df["TotalBath"]
        * df["GrLivArea"]
    )

    # --------------------------------------------------------
    # Quality × 주요 면적
    # --------------------------------------------------------

    df["Qual_1stFlr"] = (
        df["OverallQual"]
        * df["1stFlrSF"]
    )

    df["Qual_2ndFlr"] = (
        df["OverallQual"]
        * df["2ndFlrSF"]
    )

    df["Qual_BsmtFin"] = (
        df["OverallQual"]
        * df["BsmtFinSF1"]
    )

    # --------------------------------------------------------
    # 집 크기 / 방 관련
    # --------------------------------------------------------

    df["TotalRooms"] = (
        df["TotRmsAbvGrd"]
        + df["FullBath"]
        + df["HalfBath"]
    )

    df["AvgRoomArea"] = (
        df["GrLivArea"]
        / (df["TotRmsAbvGrd"] + 1)
    )

    df["GarageScore"] = (
        df["GarageCars"].fillna(0)
        * df["GarageArea"].fillna(0)
    )

    # --------------------------------------------------------
    # 품질 종합
    # --------------------------------------------------------

    df["OverallScore"] = (
        df["OverallQual"]
        * df["OverallCond"]
    )

    return df


train_fe = feature_engineering(train)
test_fe = feature_engineering(test)


# ============================================================
# 4. X / y 분리
# ============================================================

X = train_fe.drop(
    ["Id", "SalePrice"],
    axis=1
)

X_test = test_fe.drop(
    ["Id"],
    axis=1
)

y = np.log1p(
    train_fe["SalePrice"]
)


# ============================================================
# 5. Skewness 분석
# ============================================================
#
# 주의:
# 원래 컬럼을 log로 덮어쓰지 않는다.
#
# 대신:
#
# GrLivArea
#      ↓
# Log_GrLivArea
#
# 형태로 추가한다.
#
# 이렇게 하면:
# - 원본 정보 유지
# - log 정보 추가
# - 트리 모델이 필요한 표현을 선택 가능
#
# 음수가 존재하거나 binary 성격이 강한 변수는 제외.
# ============================================================

numeric_candidates = X.select_dtypes(
    include=["number"]
).columns.tolist()

skew_info = {}

for col in numeric_candidates:

    values = X[col].dropna()

    if len(values) < 3:
        continue

    # log1p가 가능해야 함
    if values.min() < 0:
        continue

    # 거의 상수인 변수 제외
    if values.nunique() <= 2:
        continue

    try:
        skew_value = skew(values)

        if np.isfinite(skew_value):
            skew_info[col] = skew_value

    except Exception:
        pass


skew_series = (
    pd.Series(skew_info)
    .sort_values(ascending=False)
)

skewed_features = (
    skew_series[
        skew_series > 0.75
    ]
    .index
    .tolist()
)

print()
print("=" * 70)
print("SKEWNESS ANALYSIS")
print("=" * 70)

print("Skew > 0.75 변수:", len(skewed_features))

print()
print(
    skew_series[
        skew_series > 0.75
    ].head(40)
)


# ============================================================
# 6. Log Feature 추가
# ============================================================

for col in skewed_features:

    new_col = "Log_" + col

    X[new_col] = np.log1p(
        X[col].clip(lower=0)
    )

    X_test[new_col] = np.log1p(
        X_test[col].clip(lower=0)
    )


print()
print("Skew 처리 후 컬럼 수:", X.shape[1])


# ============================================================
# 7. 컬럼 구분
# ============================================================

num_cols = X.select_dtypes(
    include=["number"]
).columns.tolist()

cat_cols = X.select_dtypes(
    include=["object", "string"]
).columns.tolist()

print()
print("Numerical columns:", len(num_cols))
print("Categorical columns:", len(cat_cols))


# ============================================================
# 8. 전처리 함수
# ============================================================

def create_preprocessor():

    num_pipe = SimpleImputer(
        strategy="median"
    )

    cat_pipe = make_pipeline(
        SimpleImputer(
            strategy="most_frequent"
        ),
        OneHotEncoder(
            handle_unknown="ignore"
        )
    )

    return ColumnTransformer(
        [
            (
                "num",
                num_pipe,
                num_cols
            ),
            (
                "cat",
                cat_pipe,
                cat_cols
            )
        ]
    )


# ============================================================
# 9. 모델 생성 함수
# ============================================================

def create_xgb():

    return make_pipeline(

        create_preprocessor(),

        XGBRegressor(

            n_estimators=1500,

            learning_rate=0.02,

            max_depth=3,

            min_child_weight=2,

            subsample=0.8,

            colsample_bytree=0.8,

            reg_alpha=0.01,

            reg_lambda=1.0,

            objective="reg:squarederror",

            random_state=RANDOM_STATE,

            n_jobs=-1
        )
    )


def create_gbr():

    return make_pipeline(

        create_preprocessor(),

        GradientBoostingRegressor(

            n_estimators=1500,

            learning_rate=0.03,

            max_depth=3,

            min_samples_leaf=10,

            min_samples_split=10,

            max_features="sqrt",

            loss="huber",

            random_state=RANDOM_STATE
        )
    )


def create_ridge():

    return make_pipeline(

        create_preprocessor(),

        StandardScaler(
            with_mean=False
        ),

        Ridge(
            alpha=12.0
        )
    )


def create_cat():

    return CatBoostRegressor(

        iterations=3000,

        learning_rate=0.03,

        depth=6,

        loss_function="RMSE",

        l2_leaf_reg=4,

        random_seed=RANDOM_STATE,

        random_strength=0.5,

        verbose=False,

        thread_count=-1
    )


# ============================================================
# 10. CatBoost 데이터 준비
# ============================================================

X_cat = X.copy()
X_test_cat = X_test.copy()

for col in cat_cols:

    X_cat[col] = (
        X_cat[col]
        .fillna("Missing")
        .astype(str)
    )

    X_test_cat[col] = (
        X_test_cat[col]
        .fillna("Missing")
        .astype(str)
    )


# ============================================================
# 11. OOF 준비
# ============================================================

kf = KFold(
    n_splits=N_SPLITS,
    shuffle=True,
    random_state=RANDOM_STATE
)

model_names = [
    "XGB",
    "CatBoost",
    "GBR",
    "Ridge"
]

oof = {
    name: np.zeros(len(X))
    for name in model_names
}


# ============================================================
# 12. OOF 학습
# ============================================================

print()
print("=" * 70)
print("5-FOLD OOF 학습 시작")
print("=" * 70)


for fold, (train_idx, valid_idx) in enumerate(
    kf.split(X),
    start=1
):

    print()
    print("=" * 70)
    print(f"FOLD {fold}/{N_SPLITS}")
    print("=" * 70)

    X_tr = X.iloc[train_idx]
    X_val = X.iloc[valid_idx]

    y_tr = y.iloc[train_idx]
    y_val = y.iloc[valid_idx]

    # --------------------------------------------------------
    # CatBoost 데이터
    # --------------------------------------------------------

    X_cat_tr = X_cat.iloc[train_idx]
    X_cat_val = X_cat.iloc[valid_idx]

    # --------------------------------------------------------
    # XGB
    # --------------------------------------------------------

    print("\n[1/4] XGBoost")

    xgb_model = create_xgb()

    xgb_model.fit(
        X_tr,
        y_tr
    )

    pred = xgb_model.predict(
        X_val
    )

    oof["XGB"][valid_idx] = pred

    score = np.sqrt(
        mean_squared_error(
            y_val,
            pred
        )
    )

    print(
        f"XGB Fold {fold}: {score:.5f}"
    )

    # --------------------------------------------------------
    # CatBoost
    # --------------------------------------------------------

    print("\n[2/4] CatBoost")

    cat_model = create_cat()

    cat_model.fit(
        X_cat_tr,
        y_tr,
        cat_features=cat_cols
    )

    pred = cat_model.predict(
        X_cat_val
    )

    oof["CatBoost"][valid_idx] = pred

    score = np.sqrt(
        mean_squared_error(
            y_val,
            pred
        )
    )

    print(
        f"CatBoost Fold {fold}: {score:.5f}"
    )

    # --------------------------------------------------------
    # GBR
    # --------------------------------------------------------

    print("\n[3/4] GradientBoosting")

    gbr_model = create_gbr()

    gbr_model.fit(
        X_tr,
        y_tr
    )

    pred = gbr_model.predict(
        X_val
    )

    oof["GBR"][valid_idx] = pred

    score = np.sqrt(
        mean_squared_error(
            y_val,
            pred
        )
    )

    print(
        f"GBR Fold {fold}: {score:.5f}"
    )

    # --------------------------------------------------------
    # Ridge
    # --------------------------------------------------------

    print("\n[4/4] Ridge")

    ridge_model = create_ridge()

    ridge_model.fit(
        X_tr,
        y_tr
    )

    pred = ridge_model.predict(
        X_val
    )

    oof["Ridge"][valid_idx] = pred

    score = np.sqrt(
        mean_squared_error(
            y_val,
            pred
        )
    )

    print(
        f"Ridge Fold {fold}: {score:.5f}"
    )


# ============================================================
# 13. 모델별 OOF 전체 성능
# ============================================================

print()
print("=" * 70)
print("OOF 전체 모델 성능")
print("=" * 70)

model_scores = {}

for name in model_names:

    score = np.sqrt(
        mean_squared_error(
            y,
            oof[name]
        )
    )

    model_scores[name] = score

    print(
        f"{name:<10}: {score:.5f}"
    )


# ============================================================
# 14. OOF Prediction 상관관계
# ============================================================

oof_df = pd.DataFrame(oof)

print()
print("=" * 70)
print("OOF Prediction 상관관계")
print("=" * 70)

print(
    oof_df.corr().round(4)
)


# ============================================================
# 15. 여러 블렌딩 후보
# ============================================================

candidates = {

    # v9 그대로
    "v9_original":
        [0.55, 0.25, 0.10, 0.10],

    # XGB 중심
    "xgb_cat":
        [0.60, 0.40, 0.00, 0.00],

    "xgb_cat_gbr":
        [0.50, 0.30, 0.20, 0.00],

    # CatBoost 중심
    "xgb_cat_gbr2":
        [0.40, 0.35, 0.25, 0.00],

    # GBR 강화
    "xgb_cat_gbr3":
        [0.40, 0.25, 0.35, 0.00],

    # Ridge 소량
    "xgb_cat_gbr_ridge":
        [0.45, 0.30, 0.20, 0.05],

    # 균형
    "balanced":
        [0.35, 0.30, 0.25, 0.10],

    # Cat + GBR 중심
    "cat_gbr":
        [0.20, 0.40, 0.40, 0.00],

    # Ridge 방어
    "ridge_defense":
        [0.40, 0.25, 0.20, 0.15],
}


# ============================================================
# 16. 블렌딩 평가
# ============================================================

print()
print("=" * 70)
print("고정 블렌딩 후보 비교")
print("=" * 70)

blend_results = []

for name, weights in candidates.items():

    pred = np.zeros(len(X))

    for i, model_name in enumerate(model_names):

        pred += (
            oof[model_name]
            * weights[i]
        )

    score = np.sqrt(
        mean_squared_error(
            y,
            pred
        )
    )

    blend_results.append(
        {
            "name": name,
            "score": score,
            "weights": weights
        }
    )

    print(
        f"{name:<22}: "
        f"{score:.5f}   "
        f"{weights}"
    )


# ============================================================
# 17. OOF 최적 가중치 자동 탐색
# ============================================================
#
# 조건:
# 모든 weight >= 0
# weight 합 = 1
#
# 목적:
# OOF RMSE 최소화
# ============================================================

oof_matrix = np.column_stack(
    [
        oof["XGB"],
        oof["CatBoost"],
        oof["GBR"],
        oof["Ridge"]
    ]
)


def ensemble_objective(weights):

    pred = (
        oof_matrix
        @ weights
    )

    return np.sqrt(
        mean_squared_error(
            y,
            pred
        )
    )


initial_weights = np.array(
    [0.55, 0.25, 0.10, 0.10]
)


constraints = [
    {
        "type": "eq",
        "fun": lambda w: np.sum(w) - 1
    }
]

bounds = [
    (0.0, 1.0),
    (0.0, 1.0),
    (0.0, 1.0),
    (0.0, 1.0)
]


print()
print("=" * 70)
print("OOF 최적 가중치 탐색")
print("=" * 70)

result = minimize(

    ensemble_objective,

    initial_weights,

    method="SLSQP",

    bounds=bounds,

    constraints=constraints,

    options={
        "maxiter": 1000,
        "ftol": 1e-10
    }
)


if result.success:

    optimized_weights = result.x

else:

    print(
        "최적화 실패 → v9 가중치 사용"
    )

    optimized_weights = initial_weights


optimized_weights = np.maximum(
    optimized_weights,
    0
)

optimized_weights = (
    optimized_weights
    / optimized_weights.sum()
)


optimized_score = ensemble_objective(
    optimized_weights
)


print()

for name, weight in zip(
    model_names,
    optimized_weights
):

    print(
        f"{name:<10}: {weight:.4f}"
    )

print(
    f"\nOOF Optimized Ensemble: "
    f"{optimized_score:.5f}"
)


# ============================================================
# 18. 고정 후보 + 최적화 결과 중 최고 선택
# ============================================================

best_fixed = min(
    blend_results,
    key=lambda x: x["score"]
)


if optimized_score < best_fixed["score"]:

    final_weights = optimized_weights

    final_weight_source = (
        "OOF OPTIMIZED"
    )

    final_oof_score = optimized_score

else:

    final_weights = np.array(
        best_fixed["weights"]
    )

    final_weight_source = (
        "FIXED: " + best_fixed["name"]
    )

    final_oof_score = best_fixed["score"]


print()
print("=" * 70)
print("최종 OOF 선택")
print("=" * 70)

print(
    "선택 방식:",
    final_weight_source
)

print(
    f"OOF Score: {final_oof_score:.5f}"
)

print()

for name, weight in zip(
    model_names,
    final_weights
):

    print(
        f"{name:<10}: {weight:.4f}"
    )


# ============================================================
# 19. 전체 데이터 최종 학습
# ============================================================

print()
print("=" * 70)
print("전체 데이터 최종 학습")
print("=" * 70)


# ------------------------------------------------------------
# XGB
# ------------------------------------------------------------

print("\n[1/4] XGBoost")

xgb_final = create_xgb()

xgb_final.fit(
    X,
    y
)


# ------------------------------------------------------------
# CatBoost
# ------------------------------------------------------------

print("\n[2/4] CatBoost")

cat_final = create_cat()

cat_final.fit(
    X_cat,
    y,
    cat_features=cat_cols
)


# ------------------------------------------------------------
# GBR
# ------------------------------------------------------------

print("\n[3/4] GradientBoosting")

gbr_final = create_gbr()

gbr_final.fit(
    X,
    y
)


# ------------------------------------------------------------
# Ridge
# ------------------------------------------------------------

print("\n[4/4] Ridge")

ridge_final = create_ridge()

ridge_final.fit(
    X,
    y
)


# ============================================================
# 20. Test 예측
# ============================================================

print()
print("=" * 70)
print("Test 예측")
print("=" * 70)


xgb_test = xgb_final.predict(
    X_test
)

cat_test = cat_final.predict(
    X_test_cat
)

gbr_test = gbr_final.predict(
    X_test
)

ridge_test = ridge_final.predict(
    X_test
)


# ============================================================
# 21. 최종 로그 블렌딩
# ============================================================

final_log = (

    xgb_test
    * final_weights[0]

    + cat_test
    * final_weights[1]

    + gbr_test
    * final_weights[2]

    + ridge_test
    * final_weights[3]
)


# ============================================================
# 22. 가격 복원
# ============================================================

final_preds = np.expm1(
    final_log
)

final_preds = np.maximum(
    final_preds,
    0
)


# ============================================================
# 23. 제출 파일
# ============================================================

submission = pd.DataFrame(
    {
        "Id": test["Id"],
        "SalePrice": final_preds
    }
)


submission.to_csv(
    "submission_v12_final.csv",
    index=False
)


# ============================================================
# 24. OOF 저장
# ============================================================

oof_output = pd.DataFrame(
    {
        "Id": train["Id"],
        "ActualLog": y,
        "XGB": oof["XGB"],
        "CatBoost": oof["CatBoost"],
        "GBR": oof["GBR"],
        "Ridge": oof["Ridge"]
    }
)

oof_output["Ensemble"] = (
    oof_output["XGB"]
    * final_weights[0]

    + oof_output["CatBoost"]
    * final_weights[1]

    + oof_output["GBR"]
    * final_weights[2]

    + oof_output["Ridge"]
    * final_weights[3]
)


oof_output.to_csv(
    "oof_predictions_v12.csv",
    index=False
)


# ============================================================
# 25. 결과 출력
# ============================================================

print()
print("=" * 70)
print("V12 FINAL")
print("=" * 70)

print()
print("제출 파일:")
print("submission_v12_final.csv")

print()
print("OOF 파일:")
print("oof_predictions_v12.csv")

print()
print("최종 가중치:")

for name, weight in zip(
    model_names,
    final_weights
):

    print(
        f"{name:<10}: "
        f"{weight * 100:.2f}%"
    )

print()
print(
    f"OOF Ensemble Score: "
    f"{final_oof_score:.5f}"
)

print()
print("예측 가격 통계:")
print(
    pd.Series(final_preds).describe()
)

print()
print("=" * 70)
print("✅ V12 완료")
print("=" * 70)