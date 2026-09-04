# 외곽선(컨투어)

import cv2
import numpy as np

# numpy로 이미지 만들기
img = np.zeros((500, 500), np.uint8)
cv2.rectangle(img, (100, 100), (200, 200), (255, 255, 255), -1)
cv2.circle(img, (250, 250), 50, (255, 255, 255), -1)
pts = np.array([[300, 300], [350, 350], [300, 350]], np.int32)
cv2.fillPoly(img, pts=[pts], color=(255, 255, 255))
cv2.circle(img, (400, 150), 5, (255, 255, 255), -1)
concave_pts = np.array([
    [40, 320],   # 좌측 상단
    [100, 320],  # 우측 상단
    [100, 440],  # 우측 하단
    [40, 440],   # 좌측 하단
    [70, 380]    # 파인곳
], np.int32)
cv2.fillPoly(img, [concave_pts], 255)

contours, hierarchy = cv2.findContours(
    img,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

cv2.drawContours(img, contours, -1, (100, 255, 255), 11)

# 컨투어 분석
컨투어 = contours[0]
논리값 = True
면적 = cv2.contourArea(컨투어)
둘레 =  cv2.arcLength(컨투어, 논리값)
esp = 둘레 * 0.02
바운딩박스 = cv2.boundingRect(컨투어)
회전된사각형 = cv2.minAreaRect(컨투어)
다각형근사 = cv2.approxPolyDP(컨투어, esp, 논리값)
볼록껍질 = cv2.convexHull(컨투어)
무게중심 = cv2.moments(컨투어)
print(다각형근사)
# 회전된사각형 그리기
# cv2.drawContours()

# 이미지 보여주기
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
