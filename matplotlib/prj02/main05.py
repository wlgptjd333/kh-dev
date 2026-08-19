import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(8, 6))

# data
labels = ["공부시간", "출석", "수면", "성적"]
data = np.array([[ 1.00,  0.65, -0.30,  0.80],
                 [ 0.65,  1.00, -0.10,  0.55],
                 [-0.30, -0.10,  1.00,  0.20],
                 [ 0.80,  0.55,  0.20,  1.00]])

ax.imshow(data, cmap="coolwarm", vmax=1, vmin=0)
ax.set_xticks(range(4))
ax.set_xticklabels(labels)
ax.set_yticks(range(4))
ax.set_yticklabels(labels)

for i in range(4):
    for j in range(4):
        ax.text(i,j,f"{data[i,j]}", ha="center", va="center",
                fontsize=15, fontweight="bold", color="white" if data[i,j] > 0.6 else "black")


plt.show()