import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False

# data
df= sns.load_dataset("tips")
df.to_csv("data/tips.csv")

# 누가 팁을 많이 줄까?
# plt.figure(figsize=(10,10))
# sns.scatterplot(data=df, x="total_bill", y="tip")
# plt.title("total_bill - tip 상관관계")
# plt.show()

num_cols = ['total_bill', 'tip', 'size']
x = df[num_cols].corr()
print(x)