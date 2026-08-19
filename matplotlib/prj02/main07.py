import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.family'] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# data
ratio = [50,10,10,10,20]
lang = ["python", "c", "cpp", "java", "rust"]

fig, ax = plt.subplots(figsize=(8,6))

# 파이차트
ax.pie(ratio, labels=lang, autopct="%1.1f%%")
ax.set_title("pie chart")

plt.show()