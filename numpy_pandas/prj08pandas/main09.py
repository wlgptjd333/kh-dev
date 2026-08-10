# Boolean Indexing
import pandas as pd

df = pd.read_csv("data/people.csv")

# print(df[(df["나이"] >= 30) & (df["나이"] < 40)])
# print(df[df["도시"].isin(["서울","부산" ])])
print(df[df["나이"].between(30,39)])
