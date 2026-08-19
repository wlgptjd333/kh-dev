import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family']= "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

fig,axes= plt.subplots(2,2,figsize=(10,5))

fig.suptitle("4개 그래프 ㅋㅋ")

x = np.linspace(0,10,100)

axes[0][0].plot(x, np.sin(x))
axes[0][0].set_title("sin 그래프")
axes[0][1].plot(x, np.cos(x))
axes[0][1].set_title("cos 그래프")
axes[1][0].plot(x, x**2)
axes[1][0].set_title("x**2 그래프")
axes[1][1].plot(x, np.sqrt(x))
axes[1][1].set_title("sqrt 그래프")
plt.show()