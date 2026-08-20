import pandas as pd

train = pd.read_csv('data/train.csv')
test = pd.read_csv('data/test.csv')

# print(train.isna().sum())
# print(test.isna().sum())

result =  train.groupby("Pclass")["Age","median"]
print(result)