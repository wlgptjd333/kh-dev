import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

from scipy.optimize import minimize


# ============================================================
# 0. 설정
# ============================================================

RANDOM_STATE = 42
N_SPLITS = 5


# ============================================================
# 1. 데이터 로드
# ============================================================

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

print("Train:", train.shape)
print("Test :", test.shape)


# ============================================================
# 2. Feature Engineering
#    main09.py와 동일
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
# 3. X / y
# ============================================================

X = train_fe.drop(
    ["Id", "SalePrice"],
    axis=1
)

X_test = test_fe.drop(
    ["Id"],
    axis=1
)

# 로그 가격
y = np.log1p(
    train_fe["SalePrice"]
)


# ============================================================
# 4. 숫자 / 문자 컬럼
# ============================================================

num_cols = X.select_dtypes(
    exclude=["object", "string"]
).columns.tolist()

cat_cols = X.select_dtypes(
    include=["object", "string"]
).columns.tolist()


print()
print("Numerical columns:", len(num_cols))
print("Categorical columns:", len(cat_cols))


# ============================================================
# 5. 전처리 생성 함수
#
#    중요:
#    모델마다 별도의 preprocessor를 사용
# ============================================================

def make_preprocessor():

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
# 6. 모델 생성 함수
# ============================================================

def make_xgb():

    return make_pipeline(

        make_preprocessor(),

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


def make_lgbm():

    return make_pipeline(

        make_preprocessor(),

        LGBMRegressor(

            n_estimators=1500,

            learning_rate=0.02,

            num_leaves=20,

            min_child_samples=15,

            subsample=0.8,

            colsample_bytree=0.8,

            reg_alpha=0.05,

            reg_lambda=0.5,

            random_state=RANDOM_STATE,

            verbose=-1,

            n_jobs=-1
        )
    )


def make_gbr():

    return make_pipeline(

        make_preprocessor(),

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


def make_ridge():

    return make_pipeline(

        make_preprocessor(),

        StandardScaler(
            with_mean=False
        ),

        Ridge(
            alpha=12.0
        )
    )


def make_catboost():

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
# 7. CatBoost 데이터 준비
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
# 8. OOF 배열
# ============================================================

oof_xgb = np.zeros(len(X))
oof_lgbm = np.zeros(len(X))
oof_cat = np.zeros(len(X))
oof_gbr = np.zeros(len(X))
oof_ridge = np.zeros(len(X))


# ============================================================
# 9. K-Fold
# ============================================================

kf = KFold(

    n_splits=N_SPLITS,

    shuffle=True,

    random_state=RANDOM_STATE
)


# ============================================================
# 10. OOF 학습
# ============================================================

print()
print("=" * 70)
print("5-Fold OOF 학습 시작")
print("=" * 70)

for fold, (train_idx, valid_idx) in enumerate(
    kf.split(X),
    start=1
):

    print()
    print("=" * 70)
    print(f"FOLD {fold}/{N_SPLITS}")
    print("=" * 70)

    X_train = X.iloc[train_idx]
    X_valid = X.iloc[valid_idx]

    y_train = y.iloc[train_idx]
    y_valid = y.iloc[valid_idx]


    # --------------------------------------------------------
    # XGBoost
    # --------------------------------------------------------

    print()
    print("[1/5] XGBoost 학습")

    model_xgb = make_xgb()

    model_xgb.fit(
        X_train,
        y_train
    )

    oof_xgb[valid_idx] = model_xgb.predict(
        X_valid
    )

    score_xgb = np.sqrt(
        mean_squared_error(
            y_valid,
            oof_xgb[valid_idx]
        )
    )

    print(
        f"XGB Fold {fold}: {score_xgb:.5f}"
    )


    # --------------------------------------------------------
    # LightGBM
    # --------------------------------------------------------

    print()
    print("[2/5] LightGBM 학습")

    model_lgbm = make_lgbm()

    model_lgbm.fit(
        X_train,
        y_train
    )

    oof_lgbm[valid_idx] = model_lgbm.predict(
        X_valid
    )

    score_lgbm = np.sqrt(
        mean_squared_error(
            y_valid,
            oof_lgbm[valid_idx]
        )
    )

    print(
        f"LGBM Fold {fold}: {score_lgbm:.5f}"
    )


    # --------------------------------------------------------
    # CatBoost
    # --------------------------------------------------------

    print()
    print("[3/5] CatBoost 학습")

    X_train_cat = X_cat.iloc[train_idx]
    X_valid_cat = X_cat.iloc[valid_idx]

    model_cat = make_catboost()

    model_cat.fit(

        X_train_cat,

        y_train,

        cat_features=cat_cols
    )

    oof_cat[valid_idx] = model_cat.predict(
        X_valid_cat
    )

    score_cat = np.sqrt(
        mean_squared_error(
            y_valid,
            oof_cat[valid_idx]
        )
    )

    print(
        f"CatBoost Fold {fold}: {score_cat:.5f}"
    )


    # --------------------------------------------------------
    # GradientBoosting
    # --------------------------------------------------------

    print()
    print("[4/5] GradientBoosting 학습")

    model_gbr = make_gbr()

    model_gbr.fit(
        X_train,
        y_train
    )

    oof_gbr[valid_idx] = model_gbr.predict(
        X_valid
    )

    score_gbr = np.sqrt(
        mean_squared_error(
            y_valid,
            oof_gbr[valid_idx]
        )
    )

    print(
        f"GBR Fold {fold}: {score_gbr:.5f}"
    )


    # --------------------------------------------------------
    # Ridge
    # --------------------------------------------------------

    print()
    print("[5/5] Ridge 학습")

    model_ridge = make_ridge()

    model_ridge.fit(
        X_train,
        y_train
    )

    oof_ridge[valid_idx] = model_ridge.predict(
        X_valid
    )

    score_ridge = np.sqrt(
        mean_squared_error(
            y_valid,
            oof_ridge[valid_idx]
        )
    )

    print(
        f"Ridge Fold {fold}: {score_ridge:.5f}"
    )


# ============================================================
# 11. OOF 전체 성능
# ============================================================

print()
print("=" * 70)
print("OOF 전체 모델 성능")
print("=" * 70)


oof_scores = {

    "XGB": np.sqrt(
        mean_squared_error(
            y,
            oof_xgb
        )
    ),

    "LGBM": np.sqrt(
        mean_squared_error(
            y,
            oof_lgbm
        )
    ),

    "CatBoost": np.sqrt(
        mean_squared_error(
            y,
            oof_cat
        )
    ),

    "GBR": np.sqrt(
        mean_squared_error(
            y,
            oof_gbr
        )
    ),

    "Ridge": np.sqrt(
        mean_squared_error(
            y,
            oof_ridge
        )
    )
}


for name, score in oof_scores.items():

    print(
        f"{name:<10}: {score:.5f}"
    )


# ============================================================
# 12. OOF Prediction Matrix
# ============================================================

oof_matrix = np.column_stack(

    [
        oof_xgb,
        oof_lgbm,
        oof_cat,
        oof_gbr,
        oof_ridge
    ]
)


model_names = [

    "XGB",
    "LGBM",
    "CatBoost",
    "GBR",
    "Ridge"
]


# ============================================================
# 13. OOF 기반 최적 가중치 찾기
#
#     목적:
#
#     y ≈
#       XGB*w1
#       + LGBM*w2
#       + Cat*w3
#       + GBR*w4
#       + Ridge*w5
#
#     조건:
#       모든 weight >= 0
#       weight 합 = 1
# ============================================================

print()
print("=" * 70)
print("OOF 최적 가중치 계산")
print("=" * 70)


def objective(weights):

    prediction = (
        oof_matrix @ weights
    )

    return mean_squared_error(
        y,
        prediction
    )


constraints = [

    {
        "type": "eq",
        "fun": lambda w: np.sum(w) - 1.0
    }

]


bounds = [

    (0.0, 1.0)

    for _ in range(
        len(model_names)
    )

]


# 처음에는 균등 가중치
initial_weights = np.ones(
    len(model_names)
) / len(model_names)


result = minimize(

    objective,

    initial_weights,

    method="SLSQP",

    bounds=bounds,

    constraints=constraints,

    options={
        "maxiter": 1000,
        "ftol": 1e-12
    }
)


if result.success:

    weights = result.x

else:

    print()
    print(
        "⚠️ 최적화 실패."
    )

    print(
        "균등 가중치를 사용합니다."
    )

    weights = initial_weights


# 작은 음수 방지
weights = np.maximum(
    weights,
    0
)

# 합을 1로 정규화
weights = weights / np.sum(
    weights
)


# ============================================================
# 14. 최적 가중치 출력
# ============================================================

print()

for name, weight in zip(
    model_names,
    weights
):

    print(
        f"{name:<10}: {weight:.4f}"
    )


# ============================================================
# 15. OOF 앙상블 성능
# ============================================================

oof_blend = (
    oof_matrix @ weights
)


oof_blend_score = np.sqrt(

    mean_squared_error(
        y,
        oof_blend
    )

)


print()
print(
    f"OOF Ensemble: {oof_blend_score:.5f}"
)


# ============================================================
# 16. 수동 v9 방식과 비교
# ============================================================

manual_weights = np.array(

    [
        0.55,  # XGB
        0.00,  # LGBM
        0.25,  # CatBoost
        0.10,  # GBR
        0.10   # Ridge
    ]

)


manual_oof = (
    oof_matrix @ manual_weights
)


manual_score = np.sqrt(

    mean_squared_error(
        y,
        manual_oof
    )

)


print()
print(
    f"기존 v9 방식 OOF: {manual_score:.5f}"
)

print(
    f"OOF 최적 방식   : {oof_blend_score:.5f}"
)


# ============================================================
# 17. OOF 결과 저장
# ============================================================

oof_result = pd.DataFrame({

    "SalePriceLog": y,

    "XGB": oof_xgb,

    "LGBM": oof_lgbm,

    "CatBoost": oof_cat,

    "GBR": oof_gbr,

    "Ridge": oof_ridge,

    "Ensemble": oof_blend

})


oof_result.to_csv(
    "oof_predictions_v10.csv",
    index=False
)


# ============================================================
# 18. 전체 데이터로 최종 모델 학습
# ============================================================

print()
print("=" * 70)
print("전체 데이터 최종 학습")
print("=" * 70)


# ------------------------------------------------------------
# XGBoost
# ------------------------------------------------------------

print()
print("[1/5] XGBoost 최종 학습")

final_xgb = make_xgb()

final_xgb.fit(
    X,
    y
)


# ------------------------------------------------------------
# LightGBM
# ------------------------------------------------------------

print()
print("[2/5] LightGBM 최종 학습")

final_lgbm = make_lgbm()

final_lgbm.fit(
    X,
    y
)


# ------------------------------------------------------------
# CatBoost
# ------------------------------------------------------------

print()
print("[3/5] CatBoost 최종 학습")

final_cat = make_catboost()

final_cat.fit(

    X_cat,

    y,

    cat_features=cat_cols
)


# ------------------------------------------------------------
# GradientBoosting
# ------------------------------------------------------------

print()
print("[4/5] GradientBoosting 최종 학습")

final_gbr = make_gbr()

final_gbr.fit(
    X,
    y
)


# ------------------------------------------------------------
# Ridge
# ------------------------------------------------------------

print()
print("[5/5] Ridge 최종 학습")

final_ridge = make_ridge()

final_ridge.fit(
    X,
    y
)


# ============================================================
# 19. Test 예측
# ============================================================

print()
print("=" * 70)
print("Test 예측")
print("=" * 70)


test_xgb = final_xgb.predict(
    X_test
)

test_lgbm = final_lgbm.predict(
    X_test
)

test_cat = final_cat.predict(
    X_test_cat
)

test_gbr = final_gbr.predict(
    X_test
)

test_ridge = final_ridge.predict(
    X_test
)


test_matrix = np.column_stack(

    [
        test_xgb,
        test_lgbm,
        test_cat,
        test_gbr,
        test_ridge
    ]

)


# ============================================================
# 20. 최종 로그 가격 앙상블
# ============================================================

final_log = (
    test_matrix @ weights
)


# ============================================================
# 21. 원래 가격으로 복원
# ============================================================

final_preds = np.expm1(
    final_log
)


# 음수 방지
final_preds = np.maximum(
    final_preds,
    0
)


# ============================================================
# 22. 제출 파일
# ============================================================

submission = pd.DataFrame({

    "Id": test["Id"],

    "SalePrice": final_preds

})


submission.to_csv(

    "submission_v10_oof_final.csv",

    index=False

)


# ============================================================
# 23. 최종 결과 출력
# ============================================================

print()
print("=" * 70)
print("✅ V10 OOF 최종 제출 파일 생성 완료")
print("=" * 70)

print()
print(
    "파일: submission_v10_oof_final.csv"
)

print()
print("최종 가중치:")

for name, weight in zip(
    model_names,
    weights
):

    print(
        f"{name:<10}: {weight:.4f}"
    )


print()
print(
    f"OOF Ensemble Score: {oof_blend_score:.5f}"
)


print()
print("예측 가격 통계")

print(
    pd.Series(
        final_preds
    ).describe()
)


print()
print("생성 파일:")
print("- submission_v10_oof_final.csv")
print("- oof_predictions_v10.csv")