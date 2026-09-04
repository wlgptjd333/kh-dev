# 특징점 검출 및 매칭
# 특징점 : 주변과 구별되는 위치
# 디스크립터 : 특징점 주변 모양 요약 (숫자벡터)
import cv2

img_gray = cv2.imread("images/59.png", cv2.IMREAD_GRAYSCALE)
template = cv2.imread("images/60.png", cv2.IMREAD_GRAYSCALE)

# 코너 검출
# result = cv2.cornerHarris(img_gray, 2,3,0.04)
# print("img_gray.shape : ", img_gray.shape)
# print(result.shape)

# 특징점, 디스크립터
# sift = cv2.SIFT_create()
# kp, des = sift.detectAndCompute(img_gray, None)

orb = cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img_gray, None)
kp2, des2 = orb.detectAndCompute(template, None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING)
matches = bf.knnMatch(des1,des2,k=2)

good = []
for pair in matches:
    if len(pair) != 2 : continue
    a,b = pair
    if a.distance < b.distance * 0.75:
        good.append(a)


# result = cv2.drawKeypoints(img_gray, kp1, None)
result = cv2.drawMatches(img_gray, kp1, template, kp2, good, None, flags = 2)

cv2.imshow("result", result)
cv2.waitKey(0)
cv2.destroyAllWindows()