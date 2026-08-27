import seaborn as sns
from matplotlib import pyplot as plt

df = sns.load_dataset("mpg")
# df.to_csv("data/mpg.csv")

# 결측치 처리
df["horsepower"] = df["horsepower"].fillna(df["horsepower"].median())


# 단변량
# fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(10, 10))
# sns.histplot(df["horsepower"], ax=axes[0, 0])
# sns.histplot(df["mpg"], ax=axes[0, 1])
# sns.histplot(df["weight"], ax=axes[1, 0])
# plt.show()

# 이변량
# fig, axes = plt.subplots(1,2, figsize=(15,5))
# sns.lineplot(x="horsepower", y="mpg", data=df, ax=axes[0])
# sns.scatterplot(data=df, x="weight", y="mpg", ax=axes[1])
# plt.show()

#
num_cols = ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight',
       'acceleration', 'model_year']
cor = df[num_cols].corr()
plt.figure(figsize=(15,10))
sns.heatmap(cor, annot=True, fmt=".2f")
plt.show()

print(df.columns)


