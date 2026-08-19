import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

df = sns.load_dataset("tips")

fig, axes = plt.subplots(3, 3, figsize=(12, 8))

# histplot
sns.histplot(data=df, bins=20, kde=True, ax=axes[0, 0])

# boxplot
sns.boxplot(data=df, x="total_bill", y="tip", ax=axes[0, 1])

# scatterplot
sns.scatterplot(data=df, x="total_bill", y="tip", hue="day", ax=axes[1, 0])

# heatmap
c = df[["total_bill", "tip", "size"]].corr()
sns.heatmap(data=c, annot=True, fmt=".2f", ax=axes[1, 1])

# countplot
sns.countplot(data=df, x="day", hue="sex", ax=axes[0][2])


# pairplot : 변수 쌍 전체 화면에
sns.pairplot(data=df)
savefig('result.svg')

# 결과 확인
plt.show()
