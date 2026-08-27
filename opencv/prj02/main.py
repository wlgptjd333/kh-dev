import cv2
import numpy as np

# x = cv2.imread("images/abc.png")
#
# matrix = np.full((300,300,3), (0,255,0), dtype=np.uint8)
#
# cv2.rectangle(matrix,(100,200),(200,300),(0,0,0),-1)
#
# x = np.array(matrix, dtype=np.uint8)
#
# cv2.imwrite("images/result.png", x)
#
# cv2.imshow("Original", matrix)
# result = cv2.waitKey(0)
# if result == ord('q'):
#     cv2.destroyAllWindows()

img = cv2.imread("images/24.png")
img = cv2.resize(img, (500, 500))

cv2.circle(img, (350, 280), 30, (0, 0, 255), 5)
cv2.circle(img, (350, 280), 35, (0, 255, 0), 5)
cv2.circle(img, (350, 280), 40, (255, 0, 0), 5)

cut_img = img[0:150,280:480]

cv2.imshow("Original", img)
cv2.imshow("Cut", cut_img)
cv2.waitKey(0)
cv2.destroyAllWindows()
