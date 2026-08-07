import numpy as np

exam = np.array([95, 82, 60, 45, 88, 73, 100])

# 1. 60점 이상 "합격", 미만 "불합격"
result1 = np.where(exam >= 60, "합격", "불합격")
print(result1)

# 2. 90점 이상이면 True, 아니면 False
result2 = np.where(exam >= 90, True, False)
print(result2)

# 3. 합격자 수
result3 = len(*np.where(exam >= 60))
print(result3)

# 4. (도전) 90↑ "A", 70~89 "B", 그 외` "C"
result4 = np.where(
    exam >= 90,
    "A",
    np.where(
        exam >= 70,
        "B", "C"
    )
)
print(result4)
