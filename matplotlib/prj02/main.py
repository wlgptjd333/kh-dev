import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = ['Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(8, 6))
fig.suptitle("오늘은 금요일")
x = np.linspace(0, 1, 100)
y1 = x * 1
y2 = x ** 1.5
y3 = x ** 2

ax.plot(y1, marker='o', markersize=10, linestyle='-', color='red',
        linewidth=2, label='레모네이드판매량')
ax.plot(y2, marker='s', markersize=10, linestyle='-', color='blue',
        linewidth=2, label='기온')
ax.plot(y3, marker='^', markersize=10, linestyle='-', color='green',
        linewidth=2, label='강수량')

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('현재 그래프 제목~~')

ax.legend()
plt.savefig("test.png")
plt.show()
