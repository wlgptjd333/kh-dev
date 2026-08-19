import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

fig, ax = plt.subplots(figsize=(8, 6))

# data
month = ["1월", "2월", "3월","4월", "5월", "6월"]
temp = [10,20,30,40,50,60]
rain = [120,100,80,60,40,20]

ax.plot(month, temp, label = "기온", color = "r")
ax.set_xlabel("Month")
ax.set_ylabel("Temperature")
ax2 = ax.twinx()
ax2.bar(month, rain, label="강수량", color = "b")
ax2.set_xlabel("Month")
ax2.set_ylabel("Rainfall")

ax.legend()
ax2.legend()
plt.show()