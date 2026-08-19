import pandas as pd

df = pd.read_csv('data/sales.csv')

df["날짜"] = pd.to_datetime(df["날짜"])

df = df.set_index("날짜")

result = df["매출"].resample("YE").sum()
print(result)