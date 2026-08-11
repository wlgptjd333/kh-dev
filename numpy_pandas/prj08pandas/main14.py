import pandas as pd

def check_grade(x):
    print("f01 called ~", x)
    if x > 6000:
        return "고소득자"
    else:
        return "일반"
# 데이터 준비
df = pd.read_csv("data/people.csv")

result = df["연봉"].map(check_grade)

print(type(result))
print("result: \n", result)

