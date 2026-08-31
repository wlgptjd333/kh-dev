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

# (선택) 픽셀이 이미지로 어떻게 보이는지 확인 (발표 자료 캡처용)
plt.figure(figsize=(3, 3))
plt.imshow(digits.images[0], cmap='gray_r')
plt.title(f"Label: {digits.target[0]}")
plt.axis('off')
plt.show()

# 2. 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. 전처리 및 모델 파이프라인
# 이미지 데이터(0~16)는 비율을 맞추는 MinMaxScaler가 가장 효과적입니다.
pipe = make_pipeline(
    MinMaxScaler(),
    KNeighborsClassifier(n_neighbors=5)
)

# 4. 학습 및 예측 (파이프라인 자동화)
pipe.fit(X_train, y_train)
y_pred = pipe.predict(X_test)

# 5. 최종 평가
acc = accuracy_score(y_test, y_pred)
print(f"최종 정확도: {acc:.4f}")