# 기하학 변환
import cv2
import numpy as np

# 사진 준비
img = cv2.imread("images/53.png")

# 크기조절 : cv2.resize
img = cv2.resize(img, (800,500) , fx=0.5 , fy=0.5)

# 뒤집기
img = cv2.flip(img,1)

# 이동 : warpAffine + 이동행렬
# x = 50
# y = 50
# M = np.float32([[1,0,x] , [0,1,y]])
# img = cv2.warpAffine(img,M,(800,500))

# 회전 : 90도 단위
# img = cv2.rotate(img , cv2.ROTATE_180)

# 회전 : 자유롭게
w = img.shape[1]
h = img.shape[0]
c = (w//2, h//2)
M = cv2.getRotationMatrix2D(c , 30 , 1)
img = cv2.warpAffine(img, M , (w,h))


# 사진 보여주기
cv2.imshow("img",img)
cv2.waitKey(0)
cv2.destroyAllWindows()


