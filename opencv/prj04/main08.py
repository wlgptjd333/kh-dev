# 경계, 엣지

import cv2
import numpy as np

img = cv2.imread("./images/26.png", cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (600,800))
img_g = cv2.GaussianBlur(img, (5,5), 0)

# Sobel
# sobel_x = cv2.Sobel(img_g, cv2.CV_64F, 1, 0, ksize = 3)
# sobel_y = cv2.Sobel(img_g, cv2.CV_64F, 0, 1, ksize = 3)
#
# sobel_x = cv2.convertScaleAbs(sobel_x)
# sobel_y = cv2.convertScaleAbs(sobel_y)
#
# sobel_xy = cv2.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0)
#
# cv2.imshow("img", img)
# cv2.imshow("sobel_x", sobel_x)
# cv2.imshow("sobel_y", sobel_y)
# cv2.imshow("sobel_xy", sobel_xy)
# cv2.waitKey(0)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# === Laplacian ===
# img = cv2.imread("./images/26.png", cv2.IMREAD_GRAYSCALE)
# img = cv2.resize(img, (600,800))
# img_r = cv2.GaussianBlur(img, (5,5), 0)
#
# result = cv2.Laplacian(img, cv2.CV_64F)
# result = cv2.convertScaleAbs(result)
#
# cv2.imshow("img", img)
# cv2.imshow("result", result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# === Canny ===
img = cv2.imread("./images/26.png", cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (600,800))
img_r = cv2.GaussianBlur(img, (5,5), 0)

result = cv2.Canny(img_r, 100, 200)

cv2.imshow("img", img)
cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()