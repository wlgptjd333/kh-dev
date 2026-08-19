import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# 박스플롯
# data
rng = np.random.default_rng(42)
classA = rng.normal(60,5,100)
classB = rng.normal(70,5,100)
classC = rng.normal(80,5,100)

fig, ax = plt.subplots(figsize=(8, 6))
ax.boxplot([classA, classB, classC], tick_labels=["A", "B", "C"])

plt.show()