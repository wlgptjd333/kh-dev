import numpy as np

A = np.array([[2, 1],
              [1, 3]])
B = np.array([[1, 0],
              [2, 1]])

# 1. 요소별 곱  A * B
result1 = A * B
print(result1)

# 2. 행렬곱    A @ B
result2 = A @ B
print(result2)

# 3. A의 역행렬
result3 = np.linalg.inv(A)
print(result3)

# 4. (도전) 연립방정식 풀기
#    2x + y = 5
#     x + 3y = 10
C = np.array([[5], [10]])

result4 = np.linalg.inv(A) @ C
clean_result = np.squeeze(result4)
x, y = clean_result
print(f"x :{round(x)}, y : {round(y)}")

