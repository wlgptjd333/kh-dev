# 모폴로지(침식, 팽창)

import cv2
import numpy as np

# 이미지 준비
img = np.zeros((300,300), np.uint8)
cv2.rectangle(img, (70,70), (230,230), (255,255,255), -1)
cv2.circle(img, (150,150), 5, (0,0,0), -1)
cv2.circle(img, (250,250), 5, (255,255,255), -1)

# 모폴로지
kn = np.ones((5,5), np.uint8)

# result_e = cv2.erode(img, kn, iterations=1)
# result_d = cv2.dilate(img, kn, iterations=3)

img_open = cv2.morphologyEx(img, cv2.MORPH_OPEN, kn)
img_close = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kn)
img_gradient = cv2.morphologyEx(img, cv2.MORPH_GRADIENT, kn)

cv2.imshow("img", img)
# cv2.imshow("result_e", result_e)
# cv2.imshow("result_d", result_d)
cv2.imshow("img_open", img_open)
cv2.imshow("img_close", img_close)
cv2.imshow("img_gradient", img_gradient)
cv2.waitKey(0)
cv2.destroyAllWindows()