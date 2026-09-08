# 비지도학습 (군집화, 차원축소)
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

import matplotlib.pyplot as plt
plt.rcParams['font.family'] = ['Malgun Gothic']
plt.rcParams['axes.unicode_minus'] = False
# === K means ===
# iris = load_iris()
# X = iris.data
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)
#
# m =KMeans(n_clusters=3, n_init=10, random_state=42)
# m.fit(X_scaled)
# y_pred = m.predict(X_scaled)
#
# print(y_pred)
# print(m.cluster_centers_.shape)
# print(m.inertia_)

# === K Means + elbow ===
iris = load_iris()
X = iris.data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

for k in range(2,9):
    m = KMeans(n_clusters=k, n_init=10, random_state=42)
    m.fit(X_scaled)
    y_pred = m.predict(X_scaled)
    sil_score = silhouette_score(X_scaled, y_pred)
    print(f"{k}응집도: {m.inertia_} , 실루엣 : {sil_score}")

# 차원축소 + 주성분 분석(PCA)
# === PCA ===
# X = load_iris().data
# scaler = StandardScaler()
# scaler.fit_transform(X)
# X_scaled = scaler.fit_transform(X)
#
# m = PCA(n_components=2)
# m.fit(X_scaled)
# X_2d = m.transform(X_scaled)
#
# print(X.shape)
# print(X_2d.shape)
#
# print(X)
# print(X_2d)

# === PCA + K-Means ===
# X = load_iris().data
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)
#
# model_km = KMeans(n_clusters=3, n_init=10, random_state=42)
# model_km.fit(X_scaled)
# labels = model_km.predict(X_scaled)
#
# model_pca = PCA(n_components=2)
# model_pca.fit(X_scaled)
# X_2d = model_pca.transform(X_scaled)
# print(X_2d.shape)
#
# plt.figure(figsize=(8,6))
# x_data = X_2d[:,0]
# y_data = X_2d[:,1]
# plt.scatter(x_data, y_data, c=labels, s=30, cmap="viridis")
# plt.show()

