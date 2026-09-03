import cv2

# img = cv2.imread("images/flamingos.jpg")

# # 창을 자유롭게 조절할 수 있도록 설정
# cv2.namedWindow("flamingos", cv2.WINDOW_NORMAL)
# # 화면에 맞게 창 크기 강제 지정 (가로 800, 세로 600)
# cv2.resizeWindow("flamingos", 800, 600)
# cv2.imshow("flamingos", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite("images/result.jpg", img)

# === 비디오 파일 다루기 ===
cap = cv2.VideoCapture("videos/0.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("videos/result.mp4", fourcc, fps, (w,h))

delay = int(1000/fps)
print(delay)
while True:
    is_read, frame = cap.read()
    if not is_read: break

    # 영상으로 저장
    out.write(frame)

    cv2.imshow("frame",frame)
    cv2.waitKey(delay)

out.release()
cap.release()
cv2.destroyAllWindows()