import numpy as np

'''
슬라이싱
인덱싱 [위치]
arr[행,열]
arr[행:열]
arr[[bool,bool,bool, ...]]
arr[[위치1,위치2,위치3, ...]]

sqrt
sum
max
min
log

'''


x = np.array([
    [10, 20, 30, 40, 50],
])
bool_arr = [[1, 0, 0, 0, 1]]
print(x[bool_arr])