from pathlib import Path
from ultralytics import YOLO

# model 학습 데이터 불러오기
# m = YOLO("yolov8n.pt")
m = YOLO("runs/detect/train/weights/best.pt")

# 학습: best.pt 생성
# m.train(data="./hello/data.yaml", epochs=100, imgsz=640)

# 예측
m("./aaa.png", save=True)
