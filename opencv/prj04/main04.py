# 그리기, 주석

import cv2
import numpy as np

img = cv2.imread('./images/rgb.png')
img = cv2.resize(img, (800, 500))
# 선 : cv2.line(이미지, 시작, 끝, 색, 두께)
# cv2.line(img,(100,100),(100,500),(0,0,255),5)
# 사각형 : cv2.rectangle(이미지, 좌측상단, 우측하단, 색상, 두께)
# cv2.rectangle(img, (100, 100, 300, 200), (255, 0, 0), -1)
# 원 : cv2.circle(이미지, 중심점, 반지름, 색상, 두께)
# cv2.circle(img, (100, 100), 55, (255, 0, 0), 5)
# 다각형 : cv2.polylines(이미지, 점들, 닫힘여부, 색상, 두께)
pts = np.array([
    [0, 0],
    [200, 50],
    [400, 300],
    [100, 150],
    [50, 70]
])
pts.reshape(-1, 1, 2)
# cv2.polylines(img, [pts], isClosed=True, color=(255, 0, 0), thickness=10)
# cv2.fillPoly(img, [pts], (0, 0, 0))

# 텍스트 : cv2.putText(이미지, 텍스트, 위치, 폰트, 크기, 색, 굵기)
cv2.putText(img, "Malgun Gothic", (100,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
cv2.imshow("img", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
