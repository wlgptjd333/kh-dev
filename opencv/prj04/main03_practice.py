import cv2
import numpy as np

img_fm = cv2.imread("./images/flamingos.jpg")
red = cv2.imread("./images/red.png")
img_fm = cv2.resize(img_fm, (800, 500))
red = cv2.resize(red, (800, 500))

img_hsv = cv2.cvtColor(img_fm, cv2.COLOR_BGR2HSV)

mask = cv2.inRange(img_hsv, (0,60,149), (13,255,255))
mask_inv = cv2.bitwise_not(mask)

result = cv2.bitwise_and(img_hsv, img_hsv, mask=mask)
result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)

red_hair = cv2.bitwise_and(red, red, mask=mask)
img_red_hair = cv2.bitwise_or(result, red_hair)


cv2.imshow("img_fm", img_fm)
cv2.imshow("red", red)
cv2.imshow("mask", mask)
cv2.imshow("mask_inv", mask_inv)
cv2.imshow("result", result)
cv2.imshow("img_red_hair", img_red_hair)
cv2.waitKey(0)
cv2.destroyAllWindows()
