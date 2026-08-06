# bool 인덱싱
import numpy as np

scores = np.array([100,50,70,30])

print(scores[scores < 70])

scores[(scores < 60) | (scores < 100)] = 0

print(scores)