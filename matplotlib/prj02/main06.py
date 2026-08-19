import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# data
rng = np.random.default_rng(42)
classA = rng.normal(60, 15, 100)
classB = rng.normal(70, 10, 100)
classC = rng.normal(80, 5, 100)

fig, ax = plt.subplots(figsize=(8, 6))
ax.violinplot([classA, classB, classC], showmeans=True, showmedians=True, linecolor="g")
ax.set_xticks([1, 2, 3], )
ax.set_xticklabels(["A", "B", "C"])
ax.set_ylabel("점수")

plt.show()
