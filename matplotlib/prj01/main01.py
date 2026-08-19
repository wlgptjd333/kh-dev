import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(6, 7))

arr = np.linspace(0, 10, 10)

ax.plot(arr, arr, marker="^", label= "y=x", linestyle="--")
ax.plot(arr, arr*2, marker="o", label= "y=2x", linestyle=":")
ax.plot(arr, arr*3, marker="s", label= "y=3x", linestyle="")
ax.legend()
ax.grid(alpha=0.3)

ax.set_xlabel("x")
ax.set_ylabel("y")

plt.savefig("test.png")
plt.show()

print("end ~~~~~~~~~")
