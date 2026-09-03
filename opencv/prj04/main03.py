# 산술 , 논리 , 마스킹
import cv2
import numpy as np

# === 산술 ===
# 이미지 준비
# a = np.uint8([[250]])
# b = np.uint8([[10]])
# result = cv2.add(a,b)
#
# print(a)
# print(b)
# print(result)

# cv2.imshow("a",a)
# cv2.imshow("b",b)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# === 블렌딩 ===
# a = cv2.imread("images/19.jpg", cv2.IMREAD_COLOR)
# b = cv2.imread("images/20.jpg" , cv2.IMREAD_GRAYSCALE)
# a = cv2.resize(a,(800,500))
# b = cv2.resize(b,(800,500))
#
# result = cv2.addWeighted(a,0.7,b,0.9,0)
#
# cv2.imshow("a",a)
# cv2.imshow("b",b)
# cv2.imshow("result",result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# === 비트연산 ===
# result_and = cv2.bitwise_not(a)
# cv2.imshow("and",result_and)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# === 마스킹 ===
# 흑백 마스크 : 값이 0 또는 255 인 흑백이미지
# mask = np.zeros((500,800) , dtype="uint8")
# cv2.circle(mask,(400,250),250,255,-1)
# cv2.rectangle(mask,(100,100),(700,400),255,-1)
# result = cv2.bitwise_and(a,a,mask=mask)
# cv2.imshow("a",a)
# cv2.imshow("mask",mask)
# cv2.imshow("result",result)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 색(HSV) 마스크
# img_bgr = cv2.imread("images/31.jpg")
# img_bgr = cv2.resize(img_bgr, (500, 500))
# img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
# lower = np.array([91,37,79])
# upper = np.array([108,144,208])
# mask = cv2.inRange(img_hsv, lower, upper)
# mask_inv = cv2.bitwise_not(mask)
# result = cv2.bitwise_and(img_bgr, img_bgr, mask=mask)
#
# cv2.imshow("img_bgr and img_bgr",result)
# cv2.imshow("mask",mask)
# cv2.imshow("mask_inv",mask_inv)
# cv2.imshow("img_hsv",img_hsv)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 연습
img_bgr = cv2.imread("./images/31.jpg")
red = cv2.imread("./images/red.png")
img_bgr = cv2.resize(img_bgr, (800, 500))
red = cv2.resize(red, (800, 500))
h, w = img_bgr.shape[:2]

img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(img_hsv, (91, 36, 0), (111, 255, 255))
mask_inv = cv2.bitwise_not(mask)

result = cv2.bitwise_and(img_hsv, img_hsv, mask=mask_inv)
result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

red_hair = cv2.bitwise_and(red, red, mask=mask)
img_red_hair = cv2.bitwise_or(result, red_hair)

cv2.imshow("img_bgr", img_bgr)
cv2.imshow("red", red)
cv2.imshow("mask", mask)
cv2.imshow("mask_inv", mask_inv)
cv2.imshow("result", result)
cv2.imshow("red_hair", red_hair)
cv2.imshow("img_red_hair", img_red_hair)

cv2.waitKey(0)
cv2.destroyAllWindows()