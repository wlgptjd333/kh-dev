import pandas as pd

df = pd.read_csv("data/people.csv")

print(df["연봉"].mean())
print(df["연봉"].max())
print(df["도시"].value_counts())