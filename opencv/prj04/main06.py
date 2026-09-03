# 이진화, 임계처리

import cv2

# === 전역 임계처리 ===
# img = cv2.imread("./images/19.png", cv2.IMREAD_GRAYSCALE)
# img_resized = cv2.resize(img, (500,500))
# # a, b = cv2.threshold(img_resized, 127, 255, cv2.THRESH_BINARY_INV)
# a, b = cv2.threshold(img_resized, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# cv2.imshow("img_resized", img_resized)
# cv2.imshow("b", b)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# === 적응형 임계처리 ===
img = cv2.imread("./images/19.png", cv2.IMREAD_GRAYSCALE)
img_resized = cv2.resize(img, (500, 500))

result = cv2.adaptiveThreshold(
    img_resized,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    11,
    0,
)

cv2.imshow("img_resized", img_resized)
cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
