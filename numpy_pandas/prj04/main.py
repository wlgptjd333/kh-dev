import numpy as np

x = np.arange(1, 13)
x = x.reshape(3,-1)
x = x.flatten()

print(x)
print