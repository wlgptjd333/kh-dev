import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd

from scipy.stats import skew

from sklearn.model_selection import KFold
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import (
    OneHotEncoder,
    StandardScaler
)
from sklearn.linear_model import (
    Ridge,
    Lasso,
    ElasticNet
)
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor


# ============================================================
# 설정
# ============================================================

RANDOM_STATE = 42
N_SPLITS = 5

TRAIN_PATH = "train.csv"
TEST_PATH = "test.csv"

SUBMISSION_PATH = "submission_v13_stack.csv"


# ============================================================
# 1. 데이터 로드
# ============================================================

train_raw = pd.read_csv(TRAIN_PATH)
test_raw = pd.read_csv(TEST_PATH)

print("=" * 70)
print("House Prices V13 STACK")
print("=" * 70)

print(f"Train : {train_raw.shape}")
print(f"Test  : {test_raw.shape}")


# ============================================================
# 2. Feature Engineering
# ============================================================

def feature_engineering(df):

    df = df.copy()

    # --------------------------------------------------------
    # 면적
    # --------------------------------------------------------

    df["TotalSF"] = (
        df["TotalBsmtSF"].fillna(0)
        + df["1stFlrSF"].fillna(0)
        + df["2ndFlrSF"].fillna(0)
    )

    df["TotalLivingSF"] = (
        df["GrLivArea"].fillna(0)
        + df["TotalBsmtSF"].fillna(0)
    )

    df["TotalBsmtFinSF_calc"] = (
        df["BsmtFinSF1"].fillna(0)
        + df["BsmtFinSF2"].fillna(0)
    )

    df["TotalPorchSF"] = (
        df["OpenPorchSF"].fillna(0)
        + df["3SsnPorch"].fillna(0)
        + df["EnclosedPorch"].fillna(0)
        + df["ScreenPorch"].fillna(0)
        + df["WoodDeckSF"].fillna(0)
    )

    df["TotalOutdoorSF"] = (
        df["TotalPorchSF"]
        + df["PoolArea"].fillna(0)
    )

    # --------------------------------------------------------
    # 욕실
    # --------------------------------------------------------

    df["TotalBath"] = (
        df["FullBath"].fillna(0)
        + 0.5 * df["HalfBath"].fillna(0)
        + df["BsmtFullBath"].fillna(0)
        + 0.5 * df["BsmtHalfBath"].fillna(0)
    )

    # --------------------------------------------------------
    # 집의 연식
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

    # 비정상 음수 방지
    df["HouseAge"] = df["HouseAge"].clip(lower=0)
    df["RemodAge"] = df["RemodAge"].clip(lower=0)
    df["GarageAge"] = df["GarageAge"].clip(lower=0)

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
        df["OverallQual"].fillna(0)
        * df["GrLivArea"].fillna(0)
    )

    df["Qual_TotalSF"] = (
        df["OverallQual"].fillna(0)
        * df["TotalSF"]
    )

    df["Qual_TotalBsmtSF"] = (
        df["OverallQual"].fillna(0)
        * df["TotalBsmtSF"].fillna(0)
    )

    df["Qual_GarageArea"] = (
        df["OverallQual"].fillna(0)
        * df["GarageArea"].fillna(0)
    )

    df["Qual_OverallCond"] = (
        df["OverallQual"].fillna(0)
        * df["OverallCond"].fillna(0)
    )

    df["GarageCars_Area"] = (
        df["GarageCars"].fillna(0)
        * df["GarageArea"].fillna(0)
    )

    df["Bath_GrLivArea"] = (
        df["TotalBath"]
        * df["GrLivArea"].fillna(0)
    )

    # --------------------------------------------------------
    # 추가 강한 Interaction
    # --------------------------------------------------------

    df["Qual_Age"] = (
        df["OverallQual"].fillna(0)
        * df["HouseAge"]
    )

    df["Qual_RemodAge"] = (
        df["OverallQual"].fillna(0)
        * df["RemodAge"]
    )

    df["Qual_YearBuilt"] = (
        df["OverallQual"].fillna(0)
        * df["YearBuilt"]
    )

    df["Qual_YearRemod"] = (
        df["OverallQual"].fillna(0)
        * df["YearRemodAdd"]
    )

    df["Qual_1stFlrSF"] = (
        df["OverallQual"].fillna(0)
        * df["1stFlrSF"].fillna(0)
    )

    df["Qual_2ndFlrSF"] = (
        df["OverallQual"].fillna(0)
        * df["2ndFlrSF"].fillna(0)
    )

    df["Qual_BsmtFinSF"] = (
        df["OverallQual"].fillna(0)
        * df["TotalBsmtFinSF_calc"]
    )

    # --------------------------------------------------------
    # 총 방 개념
    # --------------------------------------------------------

    df["TotalRooms"] = (
        df["TotRmsAbvGrd"].fillna(0)
        + df["FullBath"].fillna(0)
        + df["HalfBath"].fillna(0)
    )

    # --------------------------------------------------------
    # 총 면적 / 품질 비율
    # --------------------------------------------------------

    df["Qual_per_SF"] = (
        df["OverallQual"].fillna(0)
        / (df["GrLivArea"].fillna(1) + 1)
    )

    df["Age_per_Qual"] = (
        df["HouseAge"]
        / (df["OverallQual"].fillna(1) + 1)
    )

    return df


train = feature_engineering(train_raw)
test = feature_engineering(test_raw)


# ============================================================
# 3. X / y
# ============================================================

X = train.drop(
    ["Id", "SalePrice"],
    axis=1
)

X_test = test.drop(
    ["Id"],
    axis=1
)

y = np.log1p(
    train["SalePrice"]
)

print()
print(f"Feature count: {X.shape[1]}")


# ============================================================
# 4. 의미 기반 결측치 처리
# ============================================================

# NaN 자체가 "시설 없음"을 의미하는 컬럼
none_cols = [
    "PoolQC",
    "MiscFeature",
    "Alley",
    "Fence",
    "FireplaceQu",

    "GarageType",
    "GarageFinish",
    "GarageQual",
    "GarageCond",

    "BsmtQual",
    "BsmtCond",
    "BsmtExposure",
    "BsmtFinType1",
    "BsmtFinType2",

    "MasVnrType"
]

for col in none_cols:

    if col in X.columns:
        X[col] = X[col].fillna("None")

    if col in X_test.columns:
        X_test[col] = X_test[col].fillna("None")


# ------------------------------------------------------------
# 시설이 없을 때 0이 더 적절한 숫자 컬럼
# ------------------------------------------------------------

zero_cols = [
    "GarageYrBlt",
    "GarageArea",
    "GarageCars",

    "BsmtFinSF1",
    "BsmtFinSF2",
    "BsmtUnfSF",
    "TotalBsmtSF",

    "BsmtFullBath",
    "BsmtHalfBath",

    "MasVnrArea",

    "PoolArea",

    "2ndFlrSF"
]

for col in zero_cols:

    if col in X.columns:
        X[col] = X[col].fillna(0)

    if col in X_test.columns:
        X_test[col] = X_test[col].fillna(0)


# ============================================================
# 5. LotFrontage = Neighborhood median
# ============================================================

if "LotFrontage" in X.columns:

    temp = pd.DataFrame({
        "LotFrontage": X["LotFrontage"],
        "Neighborhood": X["Neighborhood"]
    })

    medians = (
        temp.groupby("Neighborhood")["LotFrontage"]
        .median()
    )

    global_median = X["LotFrontage"].median()

    X["LotFrontage"] = (
        X["LotFrontage"]
        .fillna(X["Neighborhood"].map(medians))
        .fillna(global_median)
    )

    X_test["LotFrontage"] = (
        X_test["LotFrontage"]
        .fillna(X_test["Neighborhood"].map(medians))
        .fillna(global_median)
    )


# ============================================================
# 6. Column 분리
# ============================================================

num_cols = X.select_dtypes(
    include=[np.number]
).columns.tolist()

cat_cols = X.select_dtypes(
    include=["object", "string"]
).columns.tolist()

print()
print(f"Numerical columns  : {len(num_cols)}")
print(f"Categorical columns: {len(cat_cols)}")


# ============================================================
# 7. Tree 전처리
# ============================================================

tree_num_pipe = SimpleImputer(
    strategy="median"
)

tree_cat_pipe = make_pipeline(

    SimpleImputer(
        strategy="most_frequent"
    ),

    OneHotEncoder(
        handle_unknown="ignore"
    )
)

tree_preprocessor = ColumnTransformer(

    transformers=[

        (
            "num",
            tree_num_pipe,
            num_cols
        ),

        (
            "cat",
            tree_cat_pipe,
            cat_cols
        )
    ]
)


# ============================================================
# 8. Linear 전처리
# ============================================================

# 선형 모델은 skew 처리
X_linear = X.copy()
X_test_linear = X_test.copy()


skewed_feats = (
    X_linear[num_cols]
    .apply(
        lambda x: skew(
            x.dropna()
        )
        if x.dropna().nunique() > 1
        else 0
    )
)

high_skew = (
    skewed_feats[
        skewed_feats > 0.75
    ]
    .index
)


for col in high_skew:

    # 음수가 있을 가능성이 있는 변수는 제외
    if (
        X_linear[col].dropna().min() >= 0
        and X_test_linear[col].dropna().min() >= 0
    ):

        X_linear[col] = np.log1p(
            X_linear[col]
        )

        X_test_linear[col] = np.log1p(
            X_test_linear[col]
        )


print()
print(
    f"Skew transformed features: "
    f"{len(high_skew)}"
)


linear_num_pipe = make_pipeline(

    SimpleImputer(
        strategy="median"
    ),

    StandardScaler()
)


linear_cat_pipe = make_pipeline(

    SimpleImputer(
        strategy="most_frequent"
    ),

    OneHotEncoder(
        handle_unknown="ignore"
    )
)


linear_preprocessor = ColumnTransformer(

    transformers=[

        (
            "num",
            linear_num_pipe,
            num_cols
        ),

        (
            "cat",
            linear_cat_pipe,
            cat_cols
        )
    ]
)


# ============================================================
# 9. 모델 정의
# ============================================================

def make_models():

    models = {}

    # --------------------------------------------------------
    # XGBoost
    # --------------------------------------------------------

    models["XGB"] = make_pipeline(

        tree_preprocessor,

        XGBRegressor(

            n_estimators=2000,

            learning_rate=0.02,

            max_depth=3,

            min_child_weight=1,

            subsample=0.80,

            colsample_bytree=0.80,

            reg_alpha=0.01,

            reg_lambda=1.0,

            objective="reg:squarederror",

            random_state=RANDOM_STATE,

            n_jobs=-1
        )
    )

    # --------------------------------------------------------
    # LightGBM
    # --------------------------------------------------------

    models["LGBM"] = make_pipeline(

        tree_preprocessor,

        LGBMRegressor(

            n_estimators=2000,

            learning_rate=0.02,

            num_leaves=20,

            max_depth=3,

            min_child_samples=15,

            subsample=0.80,

            colsample_bytree=0.80,

            reg_alpha=0.05,

            reg_lambda=0.50,

            random_state=RANDOM_STATE,

            verbose=-1,

            n_jobs=-1
        )
    )

    # --------------------------------------------------------
    # CatBoost
    # --------------------------------------------------------

    models["CatBoost"] = make_pipeline(

        tree_preprocessor,

        CatBoostRegressor(

            iterations=2000,

            learning_rate=0.03,

            depth=5,

            loss_function="RMSE",

            l2_leaf_reg=4,

            random_seed=RANDOM_STATE,

            verbose=False,

            thread_count=-1
        )
    )

    # --------------------------------------------------------
    # Gradient Boosting
    # --------------------------------------------------------

    models["GBR"] = make_pipeline(

        tree_preprocessor,

        GradientBoostingRegressor(

            n_estimators=1500,

            learning_rate=0.025,

            max_depth=3,

            min_samples_leaf=10,

            min_samples_split=10,

            max_features=None,

            loss="huber",

            random_state=RANDOM_STATE
        )
    )

    # --------------------------------------------------------
    # Lasso
    # --------------------------------------------------------

    models["Lasso"] = make_pipeline(

        linear_preprocessor,

        Lasso(

            alpha=0.0004,

            max_iter=30000,

            random_state=RANDOM_STATE
        )
    )

    # --------------------------------------------------------
    # ElasticNet
    # --------------------------------------------------------

    models["ElasticNet"] = make_pipeline(

        linear_preprocessor,

        ElasticNet(

            alpha=0.0005,

            l1_ratio=0.9,

            max_iter=30000,

            random_state=RANDOM_STATE
        )
    )

    return models


# ============================================================
# 10. OOF
# ============================================================

kf = KFold(

    n_splits=N_SPLITS,

    shuffle=True,

    random_state=RANDOM_STATE
)


model_names = [
    "XGB",
    "LGBM",
    "CatBoost",
    "GBR",
    "Lasso",
    "ElasticNet"
]


oof = np.zeros(
    (
        len(X),
        len(model_names)
    )
)

test_predictions = np.zeros(
    (
        len(X_test),
        len(model_names)
    )
)


print()
print("=" * 70)
print("5-FOLD OOF")
print("=" * 70)


for fold, (train_idx, valid_idx) in enumerate(
    kf.split(X),
    start=1
):

    print()
    print("=" * 70)
    print(f"FOLD {fold}/{N_SPLITS}")
    print("=" * 70)

    X_tr_tree = X.iloc[train_idx]
    X_va_tree = X.iloc[valid_idx]

    X_tr_linear = X_linear.iloc[train_idx]
    X_va_linear = X_linear.iloc[valid_idx]

    y_tr = y.iloc[train_idx]
    y_va = y.iloc[valid_idx]

    models = make_models()

    for model_idx, name in enumerate(model_names):

        print(
            f"\n[{model_idx + 1}/{len(model_names)}] "
            f"{name}"
        )

        model = models[name]

        if name in [
            "Lasso",
            "ElasticNet"
        ]:

            model.fit(
                X_tr_linear,
                y_tr
            )

            pred = model.predict(
                X_va_linear
            )

            test_pred = model.predict(
                X_test_linear
            )

        else:

            model.fit(
                X_tr_tree,
                y_tr
            )

            pred = model.predict(
                X_va_tree
            )

            test_pred = model.predict(
                X_test
            )

        oof[
            valid_idx,
            model_idx
        ] = pred

        test_predictions[
            :,
            model_idx
        ] += (
            test_pred / N_SPLITS
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_va,
                pred
            )
        )

        print(
            f"{name} Fold {fold}: "
            f"{rmse:.5f}"
        )


# ============================================================
# 11. 모델별 OOF 성능
# ============================================================

print()
print("=" * 70)
print("모델별 OOF RMSE")
print("=" * 70)

model_scores = {}

for i, name in enumerate(model_names):

    score = np.sqrt(
        mean_squared_error(
            y,
            oof[:, i]
        )
    )

    model_scores[name] = score

    print(
        f"{name:<12}: {score:.5f}"
    )


# ============================================================
# 12. OOF 블렌딩 후보
# ============================================================

print()
print("=" * 70)
print("블렌딩 후보 비교")
print("=" * 70)


blend_candidates = {

    # v9 계열
    "v9_style": {
        "XGB": 0.55,
        "CatBoost": 0.25,
        "GBR": 0.10,
        "Lasso": 0.05,
        "ElasticNet": 0.05
    },

    # 트리 중심
    "tree_heavy": {
        "XGB": 0.35,
        "CatBoost": 0.30,
        "GBR": 0.25,
        "LGBM": 0.10
    },

    # 선형 + 트리
    "balanced": {
        "XGB": 0.25,
        "CatBoost": 0.20,
        "GBR": 0.20,
        "Lasso": 0.20,
        "ElasticNet": 0.15
    },

    # 선형 강화
    "linear_heavy": {
        "XGB": 0.20,
        "CatBoost": 0.15,
        "GBR": 0.15,
        "Lasso": 0.30,
        "ElasticNet": 0.20
    },

    # GBR 강화
    "gbr_heavy": {
        "XGB": 0.15,
        "CatBoost": 0.20,
        "GBR": 0.40,
        "Lasso": 0.15,
        "ElasticNet": 0.10
    },

    # CatBoost 강화
    "cat_heavy": {
        "XGB": 0.15,
        "CatBoost": 0.40,
        "GBR": 0.20,
        "Lasso": 0.15,
        "ElasticNet": 0.10
    }
}


blend_scores = {}


for name, weights in blend_candidates.items():

    pred = np.zeros(
        len(X)
    )

    for model_name, weight in weights.items():

        idx = model_names.index(
            model_name
        )

        pred += (
            oof[:, idx]
            * weight
        )

    score = np.sqrt(
        mean_squared_error(
            y,
            pred
        )
    )

    blend_scores[name] = score

    print(
        f"{name:<15}: "
        f"{score:.5f}"
    )


# ============================================================
# 13. OOF 기반 Ridge Stacking
# ============================================================

print()
print("=" * 70)
print("Ridge STACKING")
print("=" * 70)


# 각 모델의 예측을 다시 표준화하지 않고
# Ridge meta model이 직접 가중치를 학습
meta_model = Ridge(
    alpha=10.0
)

meta_model.fit(
    oof,
    y
)

meta_oof = meta_model.predict(
    oof
)

meta_rmse = np.sqrt(
    mean_squared_error(
        y,
        meta_oof
    )
)

print(
    f"Ridge Stack OOF: "
    f"{meta_rmse:.5f}"
)


print()
print("Meta coefficients:")

for name, coef in zip(
    model_names,
    meta_model.coef_
):

    print(
        f"{name:<12}: "
        f"{coef:.5f}"
    )


# ============================================================
# 14. 최종 전략 결정
# ============================================================

best_blend_name = min(
    blend_scores,
    key=blend_scores.get
)

best_blend_score = blend_scores[
    best_blend_name
]


print()
print("=" * 70)
print("최종 전략 비교")
print("=" * 70)

print(
    f"Best manual blend : "
    f"{best_blend_name} "
    f"({best_blend_score:.5f})"
)

print(
    f"Ridge stacking    : "
    f"{meta_rmse:.5f}"
)


# ------------------------------------------------------------
# 중요:
# OOF meta-model은 학습 데이터 자체의 OOF 예측을 사용한다.
# 너무 공격적인 stacking으로 과적합될 수 있으므로
# manual blend와 비교해서 선택한다.
# ------------------------------------------------------------

if meta_rmse < best_blend_score:

    use_stacking = True

    print(
        "\n>>> 최종 모델: Ridge STACKING"
    )

else:

    use_stacking = False

    print(
        f"\n>>> 최종 모델: "
        f"{best_blend_name}"
    )


# ============================================================
# 15. 전체 데이터 재학습
# ============================================================

print()
print("=" * 70)
print("전체 데이터 최종 학습")
print("=" * 70)


final_models = make_models()


for i, name in enumerate(model_names):

    print(
        f"\n[{i + 1}/{len(model_names)}] "
        f"{name}"
    )

    model = final_models[name]

    if name in [
        "Lasso",
        "ElasticNet"
    ]:

        model.fit(
            X_linear,
            y
        )

        test_pred = model.predict(
            X_test_linear
        )

    else:

        model.fit(
            X,
            y
        )

        test_pred = model.predict(
            X_test
        )

    test_predictions[
        :,
        i
    ] = test_pred


# ============================================================
# 16. Test 최종 예측
# ============================================================

print()
print("=" * 70)
print("Test 예측")
print("=" * 70)


if use_stacking:

    final_log = meta_model.predict(
        test_predictions
    )

else:

    weights = blend_candidates[
        best_blend_name
    ]

    final_log = np.zeros(
        len(X_test)
    )

    for model_name, weight in weights.items():

        idx = model_names.index(
            model_name
        )

        final_log += (
            test_predictions[:, idx]
            * weight
        )


# ============================================================
# 17. 로그 → 실제 가격
# ============================================================

final_preds = np.expm1(
    final_log
)

final_preds = np.maximum(
    final_preds,
    0
)


# ============================================================
# 18. 제출 파일
# ============================================================

submission = pd.DataFrame({

    "Id": test_raw["Id"],

    "SalePrice": final_preds

})


submission.to_csv(
    SUBMISSION_PATH,
    index=False
)


# ============================================================
# 19. 결과
# ============================================================

print()
print("=" * 70)
print("✅ V13 FINAL COMPLETE")
print("=" * 70)

print()
print(f"파일: {SUBMISSION_PATH}")

print()
print("모델별 OOF:")

for name in model_names:

    print(
        f"{name:<12}: "
        f"{model_scores[name]:.5f}"
    )

print()
print(
    f"Best manual blend: "
    f"{best_blend_name}"
)

print(
    f"Best manual RMSE: "
    f"{best_blend_score:.5f}"
)

print(
    f"Stacking RMSE: "
    f"{meta_rmse:.5f}"
)

print()
print("예측 가격 통계")
print(
    pd.Series(final_preds).describe()
)

print()
print("=" * 70)
print("제출 준비 완료")
print("=" * 70)