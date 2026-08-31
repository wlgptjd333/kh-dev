import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor


# =========================================================
# 1. 데이터
# =========================================================

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")


# =========================================================
# 2. Feature Engineering
# =========================================================

def feature_engineering(df):

    df = df.copy()

    # -----------------------------------------------------
    # 면적
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # 욕실
    # -----------------------------------------------------

    df["TotalBath"] = (
        df["FullBath"]
        + 0.5 * df["HalfBath"]
        + df["BsmtFullBath"]
        + 0.5 * df["BsmtHalfBath"]
    )


    # -----------------------------------------------------
    # 연식
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # 존재 여부
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # Interaction
    # -----------------------------------------------------

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


    # =====================================================
    # ★ 핵심: "없음"을 의미하는 범주형 결측
    # =====================================================

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

        if col in df.columns:
            df[col] = df[col].fillna("None")


    # =====================================================
    # ★ 시설이 없는 경우 0
    # =====================================================

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

        "MasVnrArea"
    ]

    for col in zero_cols:

        if col in df.columns:
            df[col] = df[col].fillna(0)


    return df


train = feature_engineering(train)
test = feature_engineering(test)


# =========================================================
# 3. X / y
# =========================================================

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


# =========================================================
# 4. 컬럼
# =========================================================

num_cols = X.select_dtypes(
    exclude=["object", "string"]
).columns

cat_cols = X.select_dtypes(
    include=["object", "string"]
).columns


# =========================================================
# 5. 전처리
# =========================================================

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

preprocessor = ColumnTransformer([

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
])


# =========================================================
# 6. ★ v5와 동일한 모델
# =========================================================

xgb = make_pipeline(

    preprocessor,

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

        random_state=42,

        n_jobs=-1
    )
)


lgbm = make_pipeline(

    preprocessor,

    LGBMRegressor(

        n_estimators=1500,

        learning_rate=0.02,

        num_leaves=20,

        min_child_samples=15,

        subsample=0.8,

        colsample_bytree=0.8,

        reg_alpha=0.05,

        reg_lambda=0.5,

        random_state=42,

        verbose=-1,

        n_jobs=-1
    )
)


# =========================================================
# 7. 학습
# =========================================================

print("XGBoost 학습 중...")
xgb.fit(X, y)

print("LightGBM 학습 중...")
lgbm.fit(X, y)


# =========================================================
# 8. 로그 예측
# =========================================================

xgb_log = xgb.predict(X_test)

lgbm_log = lgbm.predict(X_test)


# =========================================================
# 9. ★ v5와 동일하게 5:5
# =========================================================

final_log = (
    xgb_log * 0.5
    + lgbm_log * 0.5
)


# =========================================================
# 10. 복원
# =========================================================

final_preds = np.expm1(
    final_log
)

final_preds = np.maximum(
    final_preds,
    0
)


# =========================================================
# 11. 제출
# =========================================================

submission = pd.DataFrame({

    "Id": test["Id"],

    "SalePrice": final_preds

})

submission.to_csv(
    "submission_v7_none_handling.csv",
    index=False
)

print("✅ v7 생성 완료!")