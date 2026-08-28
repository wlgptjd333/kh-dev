import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer

df = pd.DataFrame({
    "age": [20, 30, np.nan, 40, 50],
    "score": [100, np.nan, 80, 70, np.nan]
})

# df["age"] = df["age"].fillna(df["age"].mean())
# df["score"] = df["score"].fillna(df["score"].mean())

imputer = SimpleImputer(strategy="median")
result = imputer.fit_transform(df)
print(result)