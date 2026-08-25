import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# data
df = sns.load_dataset("tips")
print(df.head())

# 누가 팁을 많이 줄까?
# plt.figure(figsize=(10, 5))
# sns.scatterplot(data=df, x="total_bill", y="tip")
# plt.show()

num_cols = ['total_bill', 'tip']
corr_matrix = df[num_cols].corr()
print(corr_matrix)