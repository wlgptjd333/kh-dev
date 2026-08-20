# 판다스에서 알아야 할 2가지 : 시리즈(label이 붙은 것), df(여러 개의 시리즈 묶음)
import pandas as pd

# Series: 넘파이 + 라벨 (이름표 인덱스가 있는 1차원 배열)

# DataFrame: Series * N (이름표 인덱스가 있는 2차원 배열: 엑셀

# index / column

# 1. Series 생성: 인덱스(이름표)가 있는 1차원 데이터
s = pd.Series([90, 80, 100], index=['국어', '영어', '수학'])
print("--- Series ---")
print(s)

# 2. DataFrame 생성: Series가 모인 2차원 데이터
data = {
    '국어': [90, 85],
    '영어': [80, 95],
    '수학': [100, 90]
}
# 인덱스(Index)와 컬럼(Column)이 모두 존재
df = pd.DataFrame(data, index=['학생A', '학생B'])
print("\n--- DataFrame ---")
print(df)