import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# data
df = sns.load_dataset("flights")
df.to_csv("data/flights.csv")

x = df["year"].astype(str) + "-" + df["month"].astype(str)
df["date"] = pd.to_datetime(x, format="%Y-%b")

df.sort_values("date").reset_index(drop=True)

# plt.figure(figsize=(15, 5))
# plt.plot('date', 'passengers', data=df)
# plt.show()

plt.figure(figsize = (10,10))
sns.barplot(x="month", y="passengers", data=df, )
plt.show()