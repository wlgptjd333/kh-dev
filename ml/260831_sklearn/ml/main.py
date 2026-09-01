import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

# 1. 데이터 로드
digits = load_digits()

X = digits.data    # 64개의 픽셀 명암 수치 (0~16)
y = digits.target  # 실제 숫자 정답 (0~9)

# 픽셀 이미지 확인
plt.figure(figsize=(3, 3))
plt.imshow(digits.images[0], cmap='gray_r')
plt.title(f"Label: {digits.target[0]}")
plt.axis('off')
plt.show()


# 2. 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# 3. K값에 따른 정확도 비교
results = []

for k in range(1, 11):

    pipe = make_pipeline(
        MinMaxScaler(),
        KNeighborsClassifier(n_neighbors=k)
    )

    # 학습
    pipe.fit(X_train, y_train)

    # 예측
    y_pred = pipe.predict(X_test)

    # 정확도
    acc = accuracy_score(y_test, y_pred)

    results.append(acc)

    print(f"K={k:2d} → 정확도: {acc:.4f} ({acc * 100:.2f}%)")


# 4. 가장 높은 정확도 확인
best_index = np.argmax(results)
best_k = best_index + 1
best_acc = results[best_index]

print("\n==============================")
print(f"최적 K값: {best_k}")
print(f"최고 정확도: {best_acc:.4f} ({best_acc * 100:.2f}%)")
print("==============================")


# 5. K값에 따른 정확도 그래프
plt.figure(figsize=(8, 5))

plt.plot(
    range(1, 11),
    results,
    marker='o'
)

plt.scatter(
    best_k,
    best_acc,
    s=100
)


plt.xlabel("K (n_neighbors)")
plt.ylabel("Accuracy")
plt.title("KNN")
plt.xticks(range(1, 11))
plt.grid(alpha=0.3)
plt.legend()

plt.show()