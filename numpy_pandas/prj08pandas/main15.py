# 데이터 준비
import pandas as pd

df01 = pd.DataFrame({
    'name':  ['김철수', '이영희', '박민수'],
    'kor':   [85, 92, 78],
    'eng':   [90, 88, 95],
    'math':  [75, 100, 82]
})

df02 = pd.DataFrame({
    'name':  ['최지우', '배용준', '한소희'],
    'kor':   [88, 70, 95],
    'eng':   [79, 85, 91],
    'math':  [93, 68, 87]
})

result = pd.concat([df01,df02], ignore_index=True)

print(result)