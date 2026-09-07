# 비지도학습 (군집화, 차원축소)
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

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
