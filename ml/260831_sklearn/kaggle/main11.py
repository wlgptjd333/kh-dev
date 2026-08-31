import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import skew

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Lasso, ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, RobustScaler

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor


# ============================================================
# FINAL ATTACK V11
# ============================================================
# 1. GrLivArea > 4000 & SalePrice < 300000 이상치 제거
# 2. 검증된 Feature Engineering
# 3. Tree: XGB / LGBM / GBR / CatBoost
# 4. Linear: Lasso / ElasticNet
# 5. Linear branch에 skewed numeric log1p + RobustScaler
# 6. 5-Fold OOF
# 7. OOF non-negative optimal blending
# 8. 전체 train 재학습
# 9. log-space ensemble -> expm1
#
# 마지막 제출용 공격 버전입니다.
# ============================================================

RANDOM_STATE = 42
N_SPLITS = 5

TRAIN_PATH = "train.csv"
TEST_PATH = "test.csv"

SUBMISSION_PATH = "submission_v11_final_v2.csv"
OOF_PATH = "oof_v11_final_attack.csv"


# ============================================================
# 1. Load
# ============================================================

train_raw = pd.read_csv(TRAIN_PATH)
test_raw = pd.read_csv(TEST_PATH)

print("Train original:", train_raw.shape)
print("Test           :", test_raw.shape)


# ============================================================
# 2. Known Ames outliers
# ============================================================

outlier_mask = (
    (train_raw["GrLivArea"] > 4000)
    & (train_raw["SalePrice"] < 300000)
)

print()
print("Known outliers removed:", int(outlier_mask.sum()))

train = train_raw.loc[~outlier_mask].copy()
test = test_raw.copy()

print("Train after outlier removal:", train.shape)


# ============================================================
# 3. Feature Engineering
# ============================================================

def feature_engineering(df):

    df = df.copy()

    # ---- Area ----
    df["TotalSF"] = (
        df["TotalBsmtSF"].fillna(0)
        + df["1stFlrSF"].fillna(0)
        + df["2ndFlrSF"].fillna(0)
    )

    df["TotalLivingSF"] = (
        df["GrLivArea"].fillna(0)
        + df["TotalBsmtSF"].fillna(0)
    )

    df["TotalFinishedBsmtSF"] = (
        df["BsmtFinSF1"].fillna(0)
        + df["BsmtFinSF2"].fillna(0)
    )

    df["TotalFinishedSF"] = (
        df["GrLivArea"].fillna(0)
        + df["BsmtFinSF1"].fillna(0)
        + df["BsmtFinSF2"].fillna(0)
    )

    df["TotalHouseSF"] = (
        df["GrLivArea"].fillna(0)
        + df["TotalBsmtSF"].fillna(0)
        + df["GarageArea"].fillna(0)
        + df["WoodDeckSF"].fillna(0)
        + df["OpenPorchSF"].fillna(0)
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

    # ---- Bath ----
    df["TotalBath"] = (
        df["FullBath"].fillna(0)
        + 0.5 * df["HalfBath"].fillna(0)
        + df["BsmtFullBath"].fillna(0)
        + 0.5 * df["BsmtHalfBath"].fillna(0)
    )

    # ---- Age ----
    df["HouseAge"] = df["YrSold"] - df["YearBuilt"]
    df["RemodAge"] = df["YrSold"] - df["YearRemodAdd"]
    df["GarageAge"] = df["YrSold"] - df["GarageYrBlt"]

    # ---- Presence ----
    df["HasGarage"] = (df["GarageArea"].fillna(0) > 0).astype(int)
    df["HasBsmt"] = (df["TotalBsmtSF"].fillna(0) > 0).astype(int)
    df["HasFireplace"] = (df["Fireplaces"].fillna(0) > 0).astype(int)
    df["HasPool"] = (df["PoolArea"].fillna(0) > 0).astype(int)
    df["Has2ndFloor"] = (df["2ndFlrSF"].fillna(0) > 0).astype(int)
    df["HasMasVnr"] = (df["MasVnrArea"].fillna(0) > 0).astype(int)

    # ---- Quality interactions ----
    df["Qual_GrLivArea"] = df["OverallQual"] * df["GrLivArea"]
    df["Qual_TotalSF"] = df["OverallQual"] * df["TotalSF"]
    df["Qual_TotalBsmtSF"] = df["OverallQual"] * df["TotalBsmtSF"]
    df["Qual_GarageArea"] = df["OverallQual"] * df["GarageArea"]
    df["Qual_1stFlrSF"] = df["OverallQual"] * df["1stFlrSF"]
    df["Qual_2ndFlrSF"] = df["OverallQual"] * df["2ndFlrSF"]
    df["Qual_BsmtFinSF"] = df["OverallQual"] * df["BsmtFinSF1"]
    df["Qual_OverallCond"] = df["OverallQual"] * df["OverallCond"]

    # ---- Other interactions / ratios ----
    df["GarageCars_Area"] = df["GarageCars"] * df["GarageArea"]
    df["Bath_GrLivArea"] = df["TotalBath"] * df["GrLivArea"]

    df["AvgRoomArea"] = (
        df["GrLivArea"].fillna(0)
        / (df["TotRmsAbvGrd"].fillna(0) + 1)
    )

    df["GarageAreaPerCar"] = (
        df["GarageArea"].fillna(0)
        / (df["GarageCars"].fillna(0) + 1)
    )

    df["BsmtFinRatio"] = (
        df["TotalFinishedBsmtSF"]
        / (df["TotalBsmtSF"].fillna(0) + 1)
    )

    df["LivingToLotRatio"] = (
        df["GrLivArea"].fillna(0)
        / (df["LotArea"].fillna(0) + 1)
    )

    df["OverallScore"] = df["OverallQual"] * df["OverallCond"]

    df["TotalRooms"] = (
        df["TotRmsAbvGrd"].fillna(0)
        + df["FullBath"].fillna(0)
        + df["HalfBath"].fillna(0)
    )

    return df


train_fe = feature_engineering(train)
test_fe = feature_engineering(test)


# ============================================================
# 4. X / y
# ============================================================

X = train_fe.drop(["Id", "SalePrice"], axis=1)
X_test = test_fe.drop(["Id"], axis=1)

y = np.log1p(train_fe["SalePrice"]).values


# ============================================================
# 5. Columns
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
# 6. Skewed features
#    Linear models get log1p; tree models keep raw values.
# ============================================================

skew_values = X[num_cols].apply(
    lambda c: skew(c.dropna())
    if c.dropna().nunique() > 1 else 0
)

skewed_cols = skew_values[
    skew_values > 0.75
].index.tolist()

print("Skewed numeric features:", len(skewed_cols))


def apply_log_skew(df):

    df = df.copy()

    for col in skewed_cols:
        df[col] = np.log1p(
            df[col].clip(lower=0)
        )

    return df


X_linear = apply_log_skew(X)
X_test_linear = apply_log_skew(X_test)


# ============================================================
# 7. Preprocessors
# ============================================================

def make_tree_preprocessor():

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
            ("num", num_pipe, num_cols),
            ("cat", cat_pipe, cat_cols)
        ]
    )


def make_linear_preprocessor():

    num_pipe = make_pipeline(
        SimpleImputer(
            strategy="median"
        ),
        RobustScaler()
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
            ("num", num_pipe, num_cols),
            ("cat", cat_pipe, cat_cols)
        ]
    )


# ============================================================
# 8. Models
# ============================================================

def make_xgb():

    return make_pipeline(
        make_tree_preprocessor(),
        XGBRegressor(
            n_estimators=1800,
            learning_rate=0.018,
            max_depth=3,
            min_child_weight=2,
            subsample=0.80,
            colsample_bytree=0.85,
            reg_alpha=0.01,
            reg_lambda=1.0,
            objective="reg:squarederror",
            random_state=RANDOM_STATE,
            n_jobs=-1
        )
    )


def make_lgbm():

    return make_pipeline(
        make_tree_preprocessor(),
        LGBMRegressor(
            n_estimators=1800,
            learning_rate=0.018,
            num_leaves=20,
            min_child_samples=15,
            subsample=0.80,
            colsample_bytree=0.85,
            reg_alpha=0.05,
            reg_lambda=0.5,
            random_state=RANDOM_STATE,
            verbose=-1,
            n_jobs=-1
        )
    )


def make_gbr():

    return make_pipeline(
        make_linear_preprocessor(),
        GradientBoostingRegressor(
            n_estimators=1800,
            learning_rate=0.02,
            max_depth=3,
            min_samples_leaf=10,
            min_samples_split=10,
            loss="huber",
            random_state=RANDOM_STATE
        )
    )


def make_lasso():

    return make_pipeline(
        make_linear_preprocessor(),
        Lasso(
            alpha=0.0005,
            max_iter=20000
        )
    )


def make_elastic():

    return make_pipeline(
        make_linear_preprocessor(),
        ElasticNet(
            alpha=0.0005,
            l1_ratio=0.9,
            max_iter=30000,
            random_state=RANDOM_STATE
        )
    )


def make_catboost():

    return CatBoostRegressor(
        iterations=2500,
        learning_rate=0.025,
        depth=6,
        loss_function="RMSE",
        l2_leaf_reg=4,
        random_strength=0.5,
        random_seed=RANDOM_STATE,
        verbose=False,
        thread_count=-1,
        allow_writing_files=False
    )


# ============================================================
# 9. CatBoost categorical values
# ============================================================

X_cat = X.copy()
X_test_cat = X_test.copy()

for col in cat_cols:
    X_cat[col] = (
        X_cat[col].fillna("Missing").astype(str)
    )
    X_test_cat[col] = (
        X_test_cat[col].fillna("Missing").astype(str)
    )


# ============================================================
# 10. OOF
# ============================================================

model_names = [
    "XGB",
    "LGBM",
    "GBR",
    "Lasso",
    "ElasticNet",
    "CatBoost"
]

oof = np.zeros(
    (len(X), len(model_names))
)

kf = KFold(
    n_splits=N_SPLITS,
    shuffle=True,
    random_state=RANDOM_STATE
)


# ============================================================
# 11. OOF training
# ============================================================

print()
print("=" * 70)
print("FINAL ATTACK - 5 FOLD OOF")
print("=" * 70)

for fold, (tr_idx, va_idx) in enumerate(
    kf.split(X),
    1
):

    print()
    print("=" * 70)
    print(f"FOLD {fold}/{N_SPLITS}")
    print("=" * 70)

    Xtr = X.iloc[tr_idx]
    Xva = X.iloc[va_idx]

    Xtr_lin = X_linear.iloc[tr_idx]
    Xva_lin = X_linear.iloc[va_idx]

    Xtr_cat = X_cat.iloc[tr_idx]
    Xva_cat = X_cat.iloc[va_idx]

    ytr = y[tr_idx]
    yva = y[va_idx]

    models = [
        make_xgb(),
        make_lgbm(),
        make_gbr(),
        make_lasso(),
        make_elastic(),
        make_catboost()
    ]

    # XGB
    print("[1/6] XGB")
    models[0].fit(Xtr, ytr)
    oof[va_idx, 0] = models[0].predict(Xva)
    print(
        f"score = {np.sqrt(mean_squared_error(yva, oof[va_idx,0])):.5f}"
    )

    # LGBM
    print("[2/6] LGBM")
    models[1].fit(Xtr, ytr)
    oof[va_idx, 1] = models[1].predict(Xva)
    print(
        f"score = {np.sqrt(mean_squared_error(yva, oof[va_idx,1])):.5f}"
    )

    # GBR
    print("[3/6] GBR")
    models[2].fit(Xtr_lin, ytr)
    oof[va_idx, 2] = models[2].predict(Xva_lin)
    print(
        f"score = {np.sqrt(mean_squared_error(yva, oof[va_idx,2])):.5f}"
    )

    # Lasso
    print("[4/6] Lasso")
    models[3].fit(Xtr_lin, ytr)
    oof[va_idx, 3] = models[3].predict(Xva_lin)
    print(
        f"score = {np.sqrt(mean_squared_error(yva, oof[va_idx,3])):.5f}"
    )

    # ElasticNet
    print("[5/6] ElasticNet")
    models[4].fit(Xtr_lin, ytr)
    oof[va_idx, 4] = models[4].predict(Xva_lin)
    print(
        f"score = {np.sqrt(mean_squared_error(yva, oof[va_idx,4])):.5f}"
    )

    # CatBoost
    print("[6/6] CatBoost")
    models[5].fit(
        Xtr_cat,
        ytr,
        cat_features=cat_cols
    )
    oof[va_idx, 5] = models[5].predict(Xva_cat)
    print(
        f"score = {np.sqrt(mean_squared_error(yva, oof[va_idx,5])):.5f}"
    )


# ============================================================
# 12. Single model OOF scores
# ============================================================

print()
print("=" * 70)
print("OOF SINGLE MODEL SCORES")
print("=" * 70)

for i, name in enumerate(model_names):

    score = np.sqrt(
        mean_squared_error(
            y,
            oof[:, i]
        )
    )

    print(f"{name:<12}: {score:.5f}")


# ============================================================
# 13. OOF non-negative blending
# ============================================================

def loss(w):
    return mean_squared_error(
        y,
        oof @ w
    )


constraints = [
    {
        "type": "eq",
        "fun": lambda w: np.sum(w) - 1.0
    }
]

bounds = [
    (0.0, 1.0)
    for _ in model_names
]

initial = np.ones(
    len(model_names)
) / len(model_names)

result = minimize(
    loss,
    initial,
    method="SLSQP",
    bounds=bounds,
    constraints=constraints,
    options={
        "maxiter": 2000,
        "ftol": 1e-12
    }
)

if result.success:
    weights = result.x
else:
    print("WARNING: optimizer failed; using equal weights.")
    weights = initial

weights = np.maximum(weights, 0)
weights = weights / weights.sum()

oof_ensemble = oof @ weights

oof_score = np.sqrt(
    mean_squared_error(
        y,
        oof_ensemble
    )
)

print()
print("=" * 70)
print("OPTIMAL OOF WEIGHTS")
print("=" * 70)

for name, w in zip(model_names, weights):
    print(f"{name:<12}: {w:.4f}")

print()
print(f"OOF Ensemble: {oof_score:.5f}")


# ============================================================
# 14. Save OOF
# ============================================================

oof_df = pd.DataFrame(
    oof,
    columns=model_names
)

oof_df["TargetLog"] = y
oof_df["Ensemble"] = oof_ensemble

oof_df.to_csv(
    OOF_PATH,
    index=False
)


# ============================================================
# 15. Full-data final training
# ============================================================

print()
print("=" * 70)
print("FULL DATA FINAL TRAINING")
print("=" * 70)

print("[1/6] XGB")
final_xgb = make_xgb()
final_xgb.fit(X, y)

print("[2/6] LGBM")
final_lgbm = make_lgbm()
final_lgbm.fit(X, y)

print("[3/6] GBR")
final_gbr = make_gbr()
final_gbr.fit(X_linear, y)

print("[4/6] Lasso")
final_lasso = make_lasso()
final_lasso.fit(X_linear, y)

print("[5/6] ElasticNet")
final_elastic = make_elastic()
final_elastic.fit(X_linear, y)

print("[6/6] CatBoost")
final_cat = make_catboost()
final_cat.fit(
    X_cat,
    y,
    cat_features=cat_cols
)


# ============================================================
# 16. Test predictions
# ============================================================

print()
print("=" * 70)
print("TEST PREDICTION")
print("=" * 70)

test_matrix = np.column_stack(
    [
        final_xgb.predict(X_test),
        final_lgbm.predict(X_test),
        final_gbr.predict(X_test_linear),
        final_lasso.predict(X_test_linear),
        final_elastic.predict(X_test_linear),
        final_cat.predict(X_test_cat)
    ]
)


# ============================================================
# 17. Log-space blend
# ============================================================

final_log = test_matrix @ weights

final_preds = np.expm1(
    final_log
)

final_preds = np.maximum(
    final_preds,
    0
)


# ============================================================
# 18. Submission
# ============================================================

submission = pd.DataFrame(
    {
        "Id": test["Id"],
        "SalePrice": final_preds
    }
)

submission.to_csv(
    SUBMISSION_PATH,
    index=False
)


# ============================================================
# 19. Final report
# ============================================================

print()
print("=" * 70)
print("V11 FINAL ATTACK COMPLETE")
print("=" * 70)

print()
print("Submission:")
print(SUBMISSION_PATH)

print()
print("OOF:")
print(OOF_PATH)

print()
print(f"OOF Ensemble: {oof_score:.5f}")

print()
print("Weights:")
for name, w in zip(model_names, weights):
    print(f"{name:<12}: {w:.4f}")

print()
print("Prediction statistics:")
print(pd.Series(final_preds).describe())

print()
print("DONE.")
