import seaborn as sns
from matplotlib import pyplot as plt

titanic = sns.load_dataset("titanic")

print(titanic.head())

fig, axes = plt.subplots(2,2,figsize=(12,10))

result = titanic[["pclass","survived","fare"]].corr()
sns.pairplot(data=titanic)

plt.show()