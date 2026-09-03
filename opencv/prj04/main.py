import cv2

img = cv2.imread("./images/53.png" , cv2.IMREAD_GRAYSCALE)

roi = img[570:900,490:820]
img[0:330 , 0:330] = roi

cv2.imshow("roi",roi)
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
