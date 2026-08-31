import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
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


# ============================================================
# 1. 데이터 로드
# ============================================================

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

print("Train:", train.shape)
print("Test :", test.shape)


# ============================================================
# 2. Feature Engineering
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

y = np.log1p(
    train_fe["SalePrice"]
)


# ============================================================
# 4. 컬럼 구분
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
# 5. XGB / GBR / Ridge용 전처리
# ============================================================

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

preprocessor = ColumnTransformer(
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
# 6. XGBoost
# ============================================================

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

        random_state=RANDOM_STATE,

        n_jobs=-1
    )
)


# ============================================================
# 7. GradientBoosting
# ============================================================

gbr = make_pipeline(

    preprocessor,

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


# ============================================================
# 8. Ridge
# ============================================================

ridge = make_pipeline(

    preprocessor,

    StandardScaler(
        with_mean=False
    ),

    Ridge(
        alpha=12.0
    )
)


# ============================================================
# 9. CatBoost용 데이터
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
# 10. CatBoost
# ============================================================

cat = CatBoostRegressor(

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
# 11. 전체 데이터 학습
# ============================================================

print()
print("=" * 60)
print("전체 모델 학습")
print("=" * 60)

print("\n[1/4] XGBoost")
xgb.fit(X, y)

print("\n[2/4] GradientBoosting")
gbr.fit(X, y)

print("\n[3/4] Ridge")
ridge.fit(X, y)

print("\n[4/4] CatBoost")
cat.fit(
    X_cat,
    y,
    cat_features=cat_cols
)


# ============================================================
# 12. Test 예측
# ============================================================

print()
print("=" * 60)
print("Test 예측")
print("=" * 60)

xgb_test = xgb.predict(X_test)

gbr_test = gbr.predict(X_test)

ridge_test = ridge.predict(X_test)

cat_test = cat.predict(X_test_cat)


# ============================================================
# 13. 기본 앙상블
# ============================================================

# 공개 솔루션에서 확인된 XGB + CatBoost 조합을 참고하되
# 현재 v8에서 GBR이 실제로 도움이 되었기 때문에 포함.
#
# 기본 가중치:
#
# XGB 55%
# Cat 25%
# GBR 10%
# Ridge 10%

final_log = (

    xgb_test * 0.55

    + cat_test * 0.25

    + gbr_test * 0.10

    + ridge_test * 0.10
)


# ============================================================
# 14. 가격 복원
# ============================================================

final_preds = np.expm1(
    final_log
)

final_preds = np.maximum(
    final_preds,
    0
)


# ============================================================
# 15. 제출 파일
# ============================================================

submission = pd.DataFrame({

    "Id": test["Id"],

    "SalePrice": final_preds

})

submission.to_csv(
    "submission_v9_final.csv",
    index=False
)


# ============================================================
# 16. 완료
# ============================================================

print()
print("=" * 60)
print("✅ v9 최종 제출 파일 생성 완료")
print("=" * 60)

print()
print("파일:")
print("submission_v9_final.csv")

print()
print("모델:")
print("XGB       : 55%")
print("CatBoost  : 25%")
print("GBR       : 10%")
print("Ridge     : 10%")

print()
print("예측 가격 통계")
print(pd.Series(final_preds).describe())