# 지도학습

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

X = np.linspace(1,100,10)
y = X * 3 + 2
print(y)
print(X)
X = X.reshape(-1, 1)
print(X)
m = LinearRegression()
m.fit(X,y)

print("m.coef: " , m.coef_)
print("Intercept: ", m.intercept_)