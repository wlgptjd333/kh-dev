import numpy as np
import pandas as pd

from sklearn.model_selection import KFold
from sklearn.metrics import mean_squared_error
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder

from xgboost import XGBRegressor
from lightgbm import LGBMRegressor


# ============================================================
# 데이터
# ============================================================

train = pd.read_csv("train.csv")


# ============================================================
# Feature Engineering
# ============================================================

def feature_engineering(df):

    df = df.copy()

    df["TotalSF"] = (
        df["TotalBsmtSF"]
        + df["1stFlrSF"]
        + df["2ndFlrSF"]
    )

    df["TotalBath"] = (
        df["FullBath"]
        + 0.5 * df["HalfBath"]
        + df["BsmtFullBath"]
        + 0.5 * df["BsmtHalfBath"]
    )

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

    df["TotalPorchSF"] = (
        df["OpenPorchSF"]
        + df["3SsnPorch"]
        + df["EnclosedPorch"]
        + df["ScreenPorch"]
        + df["WoodDeckSF"]
    )

    df["TotalBsmtFinSF_calc"] = (
        df["BsmtFinSF1"]
        + df["BsmtFinSF2"]
    )

    df["TotalLivingSF"] = (
        df["GrLivArea"]
        + df["TotalBsmtSF"]
    )

    # Interaction

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

    return df


X = feature_engineering(
    train.drop(
        ["Id", "SalePrice"],
        axis=1
    )
)

y = np.log1p(
    train["SalePrice"]
)


# ============================================================
# 전처리
# ============================================================

num_cols = X.select_dtypes(
    exclude=["object"]
).columns

cat_cols = X.select_dtypes(
    include=["object"]
).columns


preprocessor = ColumnTransformer([

    (
        "num",

        SimpleImputer(
            strategy="median"
        ),

        num_cols
    ),

    (
        "cat",

        make_pipeline(

            SimpleImputer(
                strategy="most_frequent"
            ),

            OneHotEncoder(
                handle_unknown="ignore"
            )

        ),

        cat_cols
    )

])


# ============================================================
# 모델 정의
# ============================================================

models = {

    "XGB": XGBRegressor(

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
    ),


    "LGBM": LGBMRegressor(

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
}


# ============================================================
# 5-Fold CV
# ============================================================

kf = KFold(

    n_splits=5,

    shuffle=True,

    random_state=42
)


results = {}


for name, model in models.items():

    scores = []

    print("\n======================")
    print(name)
    print("======================")

    for fold, (train_idx, valid_idx) in enumerate(
        kf.split(X),
        start=1
    ):

        X_train = X.iloc[train_idx]
        X_valid = X.iloc[valid_idx]

        y_train = y.iloc[train_idx]
        y_valid = y.iloc[valid_idx]


        pipe = make_pipeline(

            preprocessor,

            model
        )


        pipe.fit(
            X_train,
            y_train
        )


        pred = pipe.predict(
            X_valid
        )


        score = np.sqrt(
            mean_squared_error(
                y_valid,
                pred
            )
        )


        scores.append(score)


        print(
            f"Fold {fold}: {score:.5f}"
        )


    mean_score = np.mean(scores)

    std_score = np.std(scores)

    results[name] = mean_score


    print(
        f"\n{name} 평균: {mean_score:.5f}"
    )

    print(
        f"{name} 표준편차: {std_score:.5f}"
    )


# ============================================================
# 최종 결과
# ============================================================

print("\n\n======================")
print("최종 비교")
print("======================")

for name, score in sorted(
    results.items(),
    key=lambda x: x[1]
):

    print(
        f"{name:10s} : {score:.5f}"
    )