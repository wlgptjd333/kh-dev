
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error


# ============================================================
# main14_blend.py
#
# 목적:
#   V9 / V13 예측을 0~100% 자동 비교
#   + OOF가 있으면 실제 RMSE로 최적 비율 탐색
#   + 최적 비율로 Test submission 생성
#
# 필요한 파일:
#
#   train.csv
#   submission_v9_final.csv
#   submission_v13_stack.csv
#
#   가능하면:
#   oof_predictions_v13.csv
#
# ============================================================


# ============================================================
# 1. 파일 경로
# ============================================================

TRAIN_FILE = "train.csv"

V9_FILE = "submission_v9_final.csv"
V13_FILE = "submission_v13_stack.csv"

# V13에서 생성한 OOF 파일 이름
# 실제 파일명이 다르면 여기만 수정
V13_OOF_FILE = "oof_predictions_v12.csv"


# ============================================================
# 2. 데이터 로드
# ============================================================

print("=" * 70)
print("V9 / V13 BLENDING SEARCH")
print("=" * 70)

train = pd.read_csv(TRAIN_FILE)

v9 = pd.read_csv(V9_FILE)
v13 = pd.read_csv(V13_FILE)

print()
print("Train :", train.shape)
print("V9    :", v9.shape)
print("V13   :", v13.shape)


# ============================================================
# 3. 기본 검증
# ============================================================

assert len(v9) == len(v13), "V9와 V13 행 개수가 다릅니다."

assert np.array_equal(
    v9["Id"].values,
    v13["Id"].values
), "V9와 V13의 Id 순서가 다릅니다."

print()
print("✅ V9 / V13 Id 및 행 순서 확인 완료")


# ============================================================
# 4. OOF 파일 확인
# ============================================================

try:

    oof = pd.read_csv(V13_OOF_FILE)

    print()
    print("OOF 파일 발견:")
    print(oof.shape)
    print(oof.columns.tolist())

except FileNotFoundError:

    oof = None

    print()
    print("⚠️ V13 OOF 파일을 찾지 못했습니다.")
    print("OOF 기반 최적화는 건너뜁니다.")


# ============================================================
# 5. OOF 컬럼 자동 탐색
# ============================================================

oof_pred_col = None

if oof is not None:

    possible_columns = [
        "prediction",
        "pred",
        "oof_prediction",
        "OOF",
        "SalePrice",
        "Predicted",
        "predicted",
        "y_pred"
    ]

    for col in possible_columns:

        if col in oof.columns:
            oof_pred_col = col
            break

    # 혹시 위 이름이 아니면 숫자 컬럼 탐색
    if oof_pred_col is None:

        numeric_cols = oof.select_dtypes(
            include=[np.number]
        ).columns.tolist()

        numeric_cols = [
            c for c in numeric_cols
            if c not in ["Id", "SalePrice"]
        ]

        if len(numeric_cols) == 1:
            oof_pred_col = numeric_cols[0]

    if oof_pred_col is not None:

        print()
        print("OOF prediction column:")
        print(oof_pred_col)

    else:

        print()
        print("⚠️ OOF prediction 컬럼을 자동으로 찾지 못했습니다.")


# ============================================================
# 6. OOF에 V13 + V9 예측이 모두 있는 경우
#
# 가장 좋은 상황:
#
# Id | y_true | v9 | v13
#
# 이런 파일이 있으면 정확한 최적 blending 가능
# ============================================================

has_full_oof = False

if oof is not None:

    required_v9 = ["v9", "V9", "v9_pred", "V9_pred"]
    required_v13 = ["v13", "V13", "v13_pred", "V13_pred"]

    v9_oof_col = None
    v13_oof_col = None

    for col in required_v9:
        if col in oof.columns:
            v9_oof_col = col
            break

    for col in required_v13:
        if col in oof.columns:
            v13_oof_col = col
            break

    if v9_oof_col is not None and v13_oof_col is not None:
        has_full_oof = True


# ============================================================
# 7. 가장 좋은 경우
#
# OOF에 V9 / V13 예측이 모두 있는 경우
# ============================================================

if has_full_oof:

    print()
    print("=" * 70)
    print("FULL OOF BLENDING SEARCH")
    print("=" * 70)

    y_true = np.log1p(train["SalePrice"].values)

    v9_oof = oof[v9_oof_col].values
    v13_oof = oof[v13_oof_col].values

    results = []

    for v13_weight in np.arange(
        0.00,
        1.001,
        0.01
    ):

        v9_weight = 1.0 - v13_weight

        blend = (
            v9_oof * v9_weight
            + v13_oof * v13_weight
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_true,
                blend
            )
        )

        results.append({
            "V9_weight": v9_weight,
            "V13_weight": v13_weight,
            "RMSE": rmse
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "RMSE"
    ).reset_index(drop=True)

    print()
    print("상위 15개 조합")
    print()

    print(
        results_df.head(15).to_string(
            index=False
        )
    )

    best = results_df.iloc[0]

    best_v9 = best["V9_weight"]
    best_v13 = best["V13_weight"]
    best_rmse = best["RMSE"]

else:

    print()
    print("=" * 70)
    print("V9 / V13 OOF 직접 비교 불가")
    print("=" * 70)

    print()
    print(
        "V9와 V13의 OOF 예측이 동시에 존재하지 않습니다."
    )

    print(
        "현재는 Kaggle 점수를 기준으로 V13을 우선 사용합니다."
    )

    # Kaggle 실전 점수 기준으로 안전하게 V13 우선
    best_v13 = 0.75
    best_v9 = 0.25
    best_rmse = np.nan


# ============================================================
# 8. 현재 V9 / V13 Kaggle 결과 참고
# ============================================================

print()
print("=" * 70)
print("KNOWN KAGGLE SCORES")
print("=" * 70)

print()
print("V9  : 0.12226")
print("V13 : 0.12148")


# ============================================================
# 9. 후보 비율 전체 출력
# ============================================================

print()
print("=" * 70)
print("0~100% BLENDING CANDIDATES")
print("=" * 70)

candidate_weights = np.arange(
    0.00,
    1.001,
    0.05
)

candidate_table = []

for v13_weight in candidate_weights:

    v9_weight = 1.0 - v13_weight

    candidate_table.append({

        "V9": f"{v9_weight * 100:.0f}%",

        "V13": f"{v13_weight * 100:.0f}%"

    })

candidate_df = pd.DataFrame(
    candidate_table
)

print()
print(candidate_df.to_string(index=False))


# ============================================================
# 10. 최종 weight
# ============================================================

print()
print("=" * 70)
print("FINAL WEIGHT")
print("=" * 70)

print()
print(
    f"V9  : {best_v9 * 100:.2f}%"
)

print(
    f"V13 : {best_v13 * 100:.2f}%"
)

if not np.isnan(best_rmse):

    print(
        f"OOF RMSE : {best_rmse:.5f}"
    )


# ============================================================
# 11. Test 예측
# ============================================================

v9_pred = v9["SalePrice"].values
v13_pred = v13["SalePrice"].values

final_pred = (
    v9_pred * best_v9
    + v13_pred * best_v13
)

final_pred = np.maximum(
    final_pred,
    0
)


# ============================================================
# 12. 최종 submission
# ============================================================

submission = pd.DataFrame({

    "Id": v13["Id"],

    "SalePrice": final_pred

})


output_file = (
    "submission_v14_v9_v13_blend.csv"
)

submission.to_csv(
    output_file,
    index=False
)


# ============================================================
# 13. 추가 후보 파일 생성
#
# 제출 기회가 있다면 여러 후보를 만들어 놓고
# 하나씩 테스트 가능
# ============================================================

print()
print("=" * 70)
print("추가 후보 submission 생성")
print("=" * 70)

candidate_submission_weights = [

    (0.00, 1.00),  # V13 100%
    (0.10, 0.90),  # V9 10 / V13 90
    (0.20, 0.80),  # V9 20 / V13 80
    (0.25, 0.75),  # V9 25 / V13 75
    (0.30, 0.70),  # V9 30 / V13 70
    (0.40, 0.60),  # V9 40 / V13 60
    (0.50, 0.50),  # 50 / 50

]

for v9_w, v13_w in candidate_submission_weights:

    pred = (
        v9_pred * v9_w
        + v13_pred * v13_w
    )

    pred = np.maximum(
        pred,
        0
    )

    filename = (
        f"submission_v14_v9_{int(v9_w*100)}"
        f"_v13_{int(v13_w*100)}.csv"
    )

    pd.DataFrame({

        "Id": v13["Id"],

        "SalePrice": pred

    }).to_csv(
        filename,
        index=False
    )

    print(
        f"생성: {filename}"
    )


# ============================================================
# 14. 최종 통계
# ============================================================

print()
print("=" * 70)
print("FINAL PREDICTION STATISTICS")
print("=" * 70)

print()

print(
    pd.Series(final_pred).describe()
)


# ============================================================
# 15. 완료
# ============================================================

print()
print("=" * 70)
print("✅ MAIN14 COMPLETE")
print("=" * 70)

print()
print(
    f"최종 파일: {output_file}"
)

print()
print(
    f"V9  weight : {best_v9:.4f}"
)

print(
    f"V13 weight : {best_v13:.4f}"
)

if not np.isnan(best_rmse):

    print(
        f"OOF RMSE   : {best_rmse:.5f}"
    )

print()
print("Kaggle에 먼저 제출할 추천 순서:")
print()
print("1. V13 100%")
print("2. V13 90% + V9 10%")
print("3. V13 80% + V9 20%")
print("4. V13 75% + V9 25%")
print("5. V13 70% + V9 30%")

print()
print("⚠️ OOF 기반 최적 비율이 있으면 그 비율을 최우선으로 사용하세요.")
