import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

from xgboost import XGBRegressor


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

    # -------------------------
    # 면적
    # -------------------------

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

    # -------------------------
    # 욕실
    # -------------------------

    df["TotalBath"] = (
        df["FullBath"]
        + 0.5 * df["HalfBath"]
        + df["BsmtFullBath"]
        + 0.5 * df["BsmtHalfBath"]
    )

    # -------------------------
    # 연식
    # -------------------------

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

    # -------------------------
    # 시설 존재 여부
    # -------------------------

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

    # -------------------------
    # 핵심 Interaction
    # -------------------------

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

y = np.log1p(train["SalePrice"])


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

preprocessor = ColumnTransformer([

    (
        "num",
        SimpleImputer(strategy="median"),
        num_cols
    ),

    (
        "cat",
        make_pipeline(
            SimpleImputer(strategy="most_frequent"),
            OneHotEncoder(
                handle_unknown="ignore"
            )
        ),
        cat_cols
    )
])


# =========================================================
# 6. XGB
# =========================================================

model = make_pipeline(

    preprocessor,

    XGBRegressor(

        n_estimators=2500,

        learning_rate=0.015,

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


# =========================================================
# 7. 학습
# =========================================================

print("XGBoost 학습 중...")

model.fit(X, y)


# =========================================================
# 8. 예측
# =========================================================

pred_log = model.predict(X_test)

pred = np.expm1(pred_log)

pred = np.maximum(pred, 0)


# =========================================================
# 9. 제출
# =========================================================

submission = pd.DataFrame({
    "Id": test["Id"],
    "SalePrice": pred
})

submission.to_csv(
    "submission_v6_xgb_tuned.csv",
    index=False
)

print("✅ v6 생성 완료")