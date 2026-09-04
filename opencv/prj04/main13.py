# 허프 변환
import cv2

img = cv2.imread("images/38.png",cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img, (500,500))

edges = cv2.Canny(img, 200, 250)

lines = cv2.HoughLinesP(
    edges,
    1,
    3.14158/180,
    threshold=100,
    minLineLength=50,
    maxLineGap=20
)

img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

if lines is not None:
    for x1,y1,x2,y2 in lines:
        cv2.line(img,(x1,y1),(x2,y2),(100,100,100),3)

cv2.imshow("edges", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()

