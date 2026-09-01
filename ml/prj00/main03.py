# 지도학습
from compression.zstd import Strategy

import numpy as np
from sklearn.datasets import load_breast_cancer, load_iris, load_wine
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# === 로지스틱 회귀 ===
# X, y = load_breast_cancer(return_X_y=True)
# X, y = load_iris(return_X_y=True)
#
# X_train, X_test, y_train, y_test = train_test_split(
#     X, y, test_size=0.2, random_state=42)
#
# scaler = StandardScaler()
# X_train_s = scaler.fit_transform(X_train)
# X_test_s = scaler.transform(X_test)
#
# m = LogisticRegression(max_iter=500)
# m.fit(X_train_s, y_train)
# y_pred = m.predict(X_test_s)
#
# acc_score = accuracy_score(y_test, y_pred)
# print("acc_score: ", acc_score)
#
# proba = m.predict_proba(X_test_s)
# print("proba : ", np.round(proba,3))
# print("proba : ", type(proba))

# === KNN ===
# X, y = load_wine(return_X_y=True)
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# sclaer = StandardScaler()
# X_train = sclaer.fit_transform(X_train)
# X_test = sclaer.transform(X_test)
#
# m = KNeighborsClassifier()
# m.fit(X_train, y_train)
# y_pred = m.predict(X_test)
#
# acc_score = accuracy_score(y_test, y_pred)
# print(acc_score)
#
# proba = m.predict_proba(X_test)
# print(np.round(proba,3))

# === SVM ===
# X, y = load_wine(return_X_y=True)
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
# # 스케일러
# scaler = StandardScaler()
# X_train_s=scaler.fit_transform(X_train)
# X_test_s=scaler.transform(X_test)
#
# m = SVC(probability=True)
# m.fit(X_train_s, y_train)
# y_pred = m.predict(X_test_s)
#
# print(accuracy_score(y_test, y_pred))
# proba = m.predict_proba(X_test_s)
# print(np.round(proba, 3))

# 모델별 성능 비교
# X, y = load_iris(return_X_y=True)
X, y = load_breast_cancer(return_X_y=True)
# 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

models = {"LogisticRegression" : make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
"KNeighborsClassifier" : make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
"SVM" : make_pipeline(StandardScaler(), SVC())}

for model_name, model_pipeline in models.items():
    model_pipeline.fit(X_train, y_train)
    y_pred = model_pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(model_name +" acc_score: ", acc)