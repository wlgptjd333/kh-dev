import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

df = sns.load_dataset("penguins")
df.to_csv("data/penguins.csv")
df = df.dropna().reset_index(drop=True)

# train, test
features = ["bill_length_mm", "bill_depth_mm", "body_mass_g", "flipper_length_mm"]
X = df[features]
y = df["species"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# 학습
# m = RandomForestClassifier(n_estimators=100,max_depth=3,random_state=42)
m = LogisticRegression(max_iter=5000)
m.fit(X_train, y_train)
# 예측
y_pred = m.predict(X_test)

# 결과
acc = accuracy_score(y_test, y_pred)
print(acc)

# 혼동행렬
lbs = ["Gentoo", "Chinstrap", "Adelie"]
cm = confusion_matrix(y_test, y_pred, labels=["Gentoo", "Chinstrap", "Adelie"])
fig, axes = plt.subplots(1, 1, figsize=(10, 6))
sns.heatmap(cm, annot=True, fmt="d", ax=axes, xticklabels=lbs, yticklabels=lbs, cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.tight_layout()
plt.show()

result = classification_report(y_test, y_pred, labels=lbs)
print(result)
