# 밝기, 대비
import cv2
import matplotlib.pyplot as plt
import numpy as np

# img = cv2.imread("./images/53.png")
# img_gray = cv2.imread("./images/53.png", cv2.IMREAD_GRAYSCALE)
# img_resized = cv2.resize(img, None, fx=0.5, fy=0.5)
# img_gray_resized = cv2.resize(img_gray, None, fx=0.5, fy=0.5)
#
# result = cv2.convertScaleAbs(img_resized, alpha =1.4, beta=-80)
# img_gray_resized_eq = cv2.equalizeHist(img_gray_resized)
#
# hist = cv2.calcHist([img_gray_resized_eq], [0], None, [256], [0, 256])
# plt.plot(hist)
# plt.show()
#
#
# cv2.imshow("img_resized", img_resized)
# cv2.imshow("result", result)
# cv2.imshow("img_gray_resized", img_gray_resized)
# cv2.imshow("img_gray_resized_eq", img_gray_resized_eq)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 컬러 이미지 밝기 조절
# img = cv2.imread("./images/53.png")
#
# img_ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
# img_ycrcb[:,:,0] = cv2.equalizeHist(img_ycrcb[:,:,0])
# result = cv2.cvtColor(img_ycrcb, cv2.COLOR_YCrCb2BGR)
#
# cv2.imshow("result", result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# CLAHE

gray = np.random.randint(90,160, (300,300), dtype=np.uint8)
gray[:, 0:150] = gray[:, 150:] * 0.5

clahe = cv2.createCLAHE(clipLimit=6.0, tileGridSize=(8,8))
result = clahe.apply(gray)

gray_eq = cv2.equalizeHist(gray)

cv2.imshow("result", result)
cv2.imshow("gray", gray)
cv2.imshow("gray_eq", gray_eq)
cv2.waitKey(0)
cv2.destroyAllWindows()