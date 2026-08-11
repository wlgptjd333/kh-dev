import numpy as np
import pandas as pd

# # 파이썬 순수 리스트
# x = [10,20,30]
#
#
# # numpy 리스트
# y = np.array(x)
#
#
#
# # 시리즈 리스트
# z = pd.Series(x)
#
#
# a = pd.Series([10, 20, 30], index=["math", "kor", "eng"])
# b = pd.Series([40, 50, 60], index=["math", "kor", "eng"])
#
# print(a["math"])
# print(b.iloc[0])
# print(a+b)

# sr01 = pd.Series(["가영", "나영", "다영"],
#                  index=["첫번째학생", "두번째학생", "세번째학생"])
# sr02 = pd.Series([100, 90, 80],
#                  index=["첫번째학생", "두번째학생", "세번째학생"])
# sr03 = pd.Series(["홍길동", "김철수"],
#                  index=["네번째학생", "다섯번째학생"])
# sr04 = pd.Series([50, 60],
#                  index=["네번째학생", "열번째학생"])
#
# sr_names = pd.concat([sr01,sr03])
# sr_scores = pd.concat([sr02,sr04])
#
# df = pd.DataFrame({
#     "이름": sr_names,
#     "성적": sr_scores,
# })
#
# print(df.loc["첫번째학생"])

df = pd.read_csv("data/people.csv")

# print(df.iloc[0:3])

df = df.dropna()
df = df.drop_duplicates()

print(df.head())