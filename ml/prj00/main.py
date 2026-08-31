import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.datasets import data, fetch_california_housing
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression

data = fetch_california_housing()

X = data.data
y = data.target

X = pd.DataFrame(X, columns=data.feature_names)
y = pd.DataFrame(y, columns=["target"])
df = X
df["target"] = y
# df.to_csv("california_hosuingdesc.csv", index=False)
print(df.isna().sum())

df.hist(figsize=(10, 10), grid=False, bins=50)
plt.show()

sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.show()

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
pipeline = make_pipeline(StandardScaler(), LinearRegression())
pipeline.fit(X_train, y_train)
# scaler = StandardScaler()
# X_train = scaler.fit_transform(X_train)
# X_test = scaler.transform(X_test)
# m = LinearRegression()
# m.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
